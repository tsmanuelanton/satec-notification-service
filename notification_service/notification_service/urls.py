from django.contrib import admin
from django.urls import path, include
from api import urls as api_urls
from conector_push_api import urls as conector_push_api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/', include(api_urls)),
    path('v1/conectors/push-api/', include(conector_push_api_urls))
]
