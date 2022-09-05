from django.urls import path
from .views import SuscriptionsApiView

urlpatterns = [
    path("subscriptions", SuscriptionsApiView.as_view())
]
