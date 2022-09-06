from django.urls import path
from .views import ServicesDetailsApiView, SuscriptionsListApiView, SuscriptionsDetailsApiView, ServicesListApiView, NotifyApiView

urlpatterns = [
    path("subscriptions", SuscriptionsListApiView.as_view()),
    path("subscriptions/<int:subscription_id>",
         SuscriptionsDetailsApiView.as_view()),
    path("services", ServicesListApiView.as_view()),
    path("services/<int:service_id>", ServicesDetailsApiView.as_view()),
    path("notify", NotifyApiView.as_view()),

]
