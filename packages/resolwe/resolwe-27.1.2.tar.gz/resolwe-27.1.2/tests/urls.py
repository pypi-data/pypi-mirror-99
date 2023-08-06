from django.urls import include, path


urlpatterns = [
    path('', include('resolwe.api_urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
