from django.urls import path
from .views.conectors_views import ConectorsListApiView, ConectorsDetailsApiView
from .views.notifications_views import NotificationsApiView
from .views.services_views import ServicesDetailsApiView, ServicesListApiView
from .views.subscription_views import SubscriptionsListApiView, SubscriptionsDetailsApiView
from .views.subscription_group_views import SubscriptionGroupListApiView, SubscriptionsGroupDetailsApiView

urlpatterns = [
    path("subscriptions", SubscriptionsListApiView.as_view()),
    path("subscriptions/<int:subscription_id>",
         SubscriptionsDetailsApiView.as_view()),
    path("groups", SubscriptionGroupListApiView.as_view()),
    path("groups/<int:group_id>",
         SubscriptionsGroupDetailsApiView.as_view()),
    path("services", ServicesListApiView.as_view()),
    path("services/<int:service_id>", ServicesDetailsApiView.as_view()),
    path("conectors", ConectorsListApiView.as_view()),
    path("conectors/<int:conector_id>", ConectorsDetailsApiView.as_view()),
    path("notifications", NotificationsApiView.as_view()),

]
