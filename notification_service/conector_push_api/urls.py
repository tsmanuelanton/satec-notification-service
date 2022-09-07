from django.urls import path
from .views import NotificationApiView

urlpatterns = [
    path('notify', NotificationApiView.as_view()),
]
