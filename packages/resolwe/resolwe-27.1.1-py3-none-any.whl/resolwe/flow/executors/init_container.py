"""Kubernetes init container initialization script.

1. Fix permission (make genialis user owner) on subdirectories on the EBS
   volume used for local processing.
2. Transfer missing data to the input EBS volume.
"""

import asyncio
import logging
import os
import shutil
import sys
from collections import defaultdict
from contextlib import suppress
from distutils.util import strtobool
from pathlib import Path

import zmq
import zmq.asyncio
from executors.connectors import Transfer, connectors
from executors.connectors.baseconnector import BaseStorageConnector
from executors.connectors.exceptions import DataTransferError
from executors.connectors.utils import paralelize
from executors.socket_utils import BaseCommunicator, BaseProtocol, Message, PeerIdentity
from executors.zeromq_utils import ZMQCommunicator

from .transfer import transfer_data

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


LISTENER_IP = os.getenv("LISTENER_IP", "127.0.0.1")
LISTENER_PORT = os.getenv("LISTENER_PORT", "53893")
LISTENER_PROTOCOL = os.getenv("LISTENER_PROTOCOL", "tcp")

DATA_ID = int(os.getenv("DATA_ID", "-1"))

DATA_LOCAL_VOLUME = Path(os.environ.get("DATA_LOCAL_VOLUME", "/data_local"))
INPUTS_VOLUME = Path(os.environ.get("INPUTS_VOLUME", "/inputs"))

GENIALIS_UID = int(os.environ.get("GENIALIS_UID", 0))
GENIALIS_GID = int(os.environ.get("GENIALIS_GID", 0))

LOCATION_SUBPATH = Path(os.environ["LOCATION_SUBPATH"])  # No sensible default.

DOWNLOAD_WAITING_TIMEOUT = 60  # in seconds
RETRIES = 5

DATA_ALL_VOLUME_SHARED = bool(
    strtobool(os.environ.get("DATA_ALL_VOLUME_SHARED", "False"))
)
SET_PERMISSIONS = bool(strtobool(os.environ.get("INIT_SET_PERMISSIONS", "False")))


async def transfer_inputs(communicator: BaseCommunicator):
    """Transfer missing input data.

    :raises DataTransferError: on failure.
    """
    inputs_connector = connectors["local"].duplicate()
    inputs_connector.path = INPUTS_VOLUME
    inputs_connector.name = "inputs"
    inputs_connector.config["path"] = INPUTS_VOLUME

    logger.debug("Transfering missing data.")
    response = await communicator.send_command(
        Message.command("get_inputs_no_shared_storage", "")
    )

    # Group files by connectors. So we can transfer files from single connector
    # in parallel. We could also transfer files belonging to different
    # connectors in parallel but this could produce huge number of threads,
    # since S3 uses multiple threads to transfer single file.
    objects_to_transfer: dict[str, list[dict[str, str]]] = defaultdict(list)
    for base_url, (connector_name, files) in response.message_data.items():
        for file in files:
            file.update({"from_base_url": base_url, "to_base_url": base_url})
        objects_to_transfer[connector_name] += files

    try:
        for connector_name in objects_to_transfer:
            await download_to_location(
                objects_to_transfer[connector_name],
                connectors[connector_name],
                inputs_connector,
            )
    except:
        error_message = (
            f"Preparing inputs {objects_to_transfer[connector_name]} from "
            f"connector {connector_name} failed."
        )
        await communicator.send_command(
            Message.command("process_log", {"error": error_message})
        )
        await communicator.send_command(Message.command("finish", {}))
        raise DataTransferError(error_message)


async def download_to_location(
    files: list[dict[str, str]],
    from_connector: BaseStorageConnector,
    to_connector: BaseStorageConnector,
    max_threads: int = 5,
):
    """Download missing paths.

    :raises DataTransferError: on failure.
    """
    logger.info(f"Transfering data {from_connector} --> {to_connector}.")
    transfer = Transfer(from_connector, to_connector)
    # Start futures and evaluate their results. If exception occured it will
    # be re-raised.
    for future in paralelize(
        objects=files,
        worker=lambda objects: transfer.transfer_chunk(None, objects),
        max_threads=max_threads,
    ):
        future.result()


def set_permissions():
    """Set permissions."""
    logger.debug("Setting permissions.")
    local_directory = DATA_LOCAL_VOLUME / LOCATION_SUBPATH
    local_directory.mkdir()
    shutil.chown(local_directory, GENIALIS_UID, GENIALIS_GID)


def _get_communicator() -> ZMQCommunicator:
    """Connect to the listener."""
    zmq_context = zmq.asyncio.Context.instance()
    zmq_socket = zmq_context.socket(zmq.DEALER)
    zmq_socket.setsockopt(zmq.IDENTITY, str(DATA_ID).encode())
    connect_string = f"{LISTENER_PROTOCOL}://{LISTENER_IP}:{LISTENER_PORT}"
    logger.debug("Opening connection to %s", connect_string)
    zmq_socket.connect(connect_string)
    return ZMQCommunicator(zmq_socket, "init_container <-> listener", logger)


class InitProtocol(BaseProtocol):
    """Protocol class."""

    async def post_terminate(self, message: Message, identity: PeerIdentity):
        """Handle post-terminate command."""
        logger.debug("Init container received terminate request, terminating.")
        await error("Init container received terminating request.", self.communicator)
        for task in asyncio.all_tasks():
            task.cancel()

    async def transfer_missing_data(self):
        """Transfer missing data.

        :raises DataTransferError: when data transfer error occurs.
        """
        await self.communicator.send_command(Message.command("update_status", "PP"))
        if DATA_ALL_VOLUME_SHARED:
            transfering_coroutine = transfer_data(self.communicator)
        else:
            transfering_coroutine = transfer_inputs(self.communicator)
        await transfering_coroutine


async def error(error_message: str, communicator: BaseCommunicator):
    """Error occured inside container.

    Send the error and terminate the process.
    """
    with suppress(Exception):
        await communicator.send_command(
            Message.command("process_log", {"error": error_message})
        )
    with suppress(Exception):
        await communicator.send_command(Message.command("finish", {}))


async def main():
    """Start the main program.

    :raises RuntimeError: when runtime error occurs.
    :raises asyncio.exceptions.CancelledError: when task is terminated.
    """
    if SET_PERMISSIONS:
        set_permissions()
    protocol = InitProtocol(_get_communicator(), logger)
    communicate_task = asyncio.ensure_future(protocol.communicate())
    try:
        await protocol.transfer_missing_data()
    except DataTransferError as error:
        error(
            f"Data transfer error in init container: {str(error)}",
            protocol.communicator,
        )
    protocol.stop_communicate()
    with suppress(asyncio.TimeoutError):
        await asyncio.wait_for(communicate_task, timeout=10)


if __name__ == "__main__":
    logger.debug("Starting the main program.")
    try:
        asyncio.run(main())
    except:
        logger.debug("Exception in init container.")
        sys.exit(1)
