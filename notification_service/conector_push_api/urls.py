from django.contrib import admin
from django.urls import path, include
from api import urls as api_urls
from . import views

urlpatterns = [
    path('notify', views.notify)
]
