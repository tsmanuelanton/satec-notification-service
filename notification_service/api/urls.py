from django.urls import path
from .views import SuscriptionsListApiView, SuscriptionsDetailsApiView

urlpatterns = [
    path("subscriptions", SuscriptionsListApiView.as_view()),
    path("subscriptions/<int:subscription_id>",
         SuscriptionsDetailsApiView.as_view())
]
