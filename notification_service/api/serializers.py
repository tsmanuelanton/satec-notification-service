from rest_framework import serializers
from .models import Conector, Subscription, Service


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "service_id", "conector_id",
                  "subscription_data"]

        extra_kwargs = {
            "conector_id": {
                "error_messages": {
                    "does_not_exist": "Unknown conector"
                }
            }, "service_id": {"error_messages": {
                "does_not_exist": "Unknown service"}}}


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "service_name", "service_owner"]


class ConectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conector
        fields = ["id", "name", "description", "meta"]


class MessageSerializer(serializers.Serializer):
    '''
    Valida que el cuerpo del mensaje POST esté bien formado
    '''
    service_id = serializers.IntegerField()
    message = serializers.JSONField()
