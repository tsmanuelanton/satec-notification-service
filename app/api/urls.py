from django.urls import path
from .views.conectors import ConectorsList, ConectorDetails
from .views.notifications import NotificationDetails
from .views.services import ServiceDetails, ServicesList
from .views.subscriptions import SubscriptionsList, SubscriptionDetails
from .views.subscription_groups import SubscriptionGroupsList, SubscriptionGroupDetails
from django.views.generic import TemplateView

urlpatterns = [
    path("", ServicesList.as_view()),
    path("subscriptions", SubscriptionsList.as_view(), name="subscriptions"),
    path("subscriptions/<int:subscription_id>",
         SubscriptionDetails.as_view()),
    path("groups", SubscriptionGroupsList.as_view(), name="groups"),
    path("groups/<int:group_id>",
         SubscriptionGroupDetails.as_view()),
    path("services", ServicesList.as_view(), name="services"),
    path("services/<int:service_id>", ServiceDetails.as_view()),
    path("conectors", ConectorsList.as_view(), name="conectors"),
    path("conectors/<int:conector_id>", ConectorDetails.as_view()),
    path("notifications", NotificationDetails.as_view(), name="notifications"),
    path('schema/', TemplateView.as_view(
        template_name='api/swagger-ui.html',
    ), name='schema'),
    
]
