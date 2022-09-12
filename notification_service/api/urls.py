from django.urls import path
from .views import ConectorsApiView, ServicesDetailsApiView, SuscriptionsListApiView, SuscriptionsDetailsApiView, ServicesListApiView, MessagesApiView

urlpatterns = [
    path("subscriptions", SuscriptionsListApiView.as_view()),
    path("subscriptions/<int:subscription_id>",
         SuscriptionsDetailsApiView.as_view()),
    path("services", ServicesListApiView.as_view()),
    path("services/<int:service_id>", ServicesDetailsApiView.as_view()),
    path("conectors", ConectorsApiView.as_view()),
    path("notify", MessagesApiView.as_view()),

]
