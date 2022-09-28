from django.urls import path
from .views.conectors_views import ConectorsApiView
from .views.notifications_views import NotificationsApiView
from .views.services_views import ServicesDetailsApiView, ServicesListApiView
from .views.subscription_views import SuscriptionsListApiView, SuscriptionsDetailsApiView

urlpatterns = [
    path("subscriptions", SuscriptionsListApiView.as_view()),
    path("subscriptions/<int:subscription_id>",
         SuscriptionsDetailsApiView.as_view()),
    path("services", ServicesListApiView.as_view()),
    path("services/<int:service_id>", ServicesDetailsApiView.as_view()),
    path("conectors", ConectorsApiView.as_view()),
    path("notifications", NotificationsApiView.as_view()),

]
