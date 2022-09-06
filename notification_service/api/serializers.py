from rest_framework import serializers
from .models import Subscriptions


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ["service_id", "subscription_data", "id"]
