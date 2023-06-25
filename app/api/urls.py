from django.urls import path
from .views.conectors import ConectorsList, ConectorDetails
from .views.notifications import NotificationDetails
from .views.services import ServiceDetails, ServicesList
from .views.subscriptions import SubscriptionsList, SubscriptionDetails
from .views.subscription_groups import SubscriptionGroupsList, SubscriptionGroupDetails

urlpatterns = [
    path("subscriptions", SubscriptionsList.as_view()),
    path("subscriptions/<int:subscription_id>",
         SubscriptionDetails.as_view()),
    path("groups", SubscriptionGroupsList.as_view()),
    path("groups/<int:group_id>",
         SubscriptionGroupDetails.as_view()),
    path("services", ServicesList.as_view()),
    path("services/<int:service_id>", ServiceDetails.as_view()),
    path("conectors", ConectorsList.as_view()),
    path("conectors/<int:conector_id>", ConectorDetails.as_view()),
    path("notifications", NotificationDetails.as_view()),

]
