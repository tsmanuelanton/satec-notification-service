from django.contrib import admin
from django.urls import path, include
from api import urls as api_urls
from frontend import urls as frontend_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(api_urls)),
    path('', include(frontend_urls)),
]
