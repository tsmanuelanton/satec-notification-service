from rest_framework import serializers
from .models import Conector, Subscription, Service


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "service", "conector",
                  "subscription_data"]

        extra_kwargs = {
            "conector": {
                "error_messages": {
                    "does_not_exist": "Unknown conector"
                }
            }, "service": {"error_messages": {
                "does_not_exist": "Unknown service"}}}


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "owner"]


class ConectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conector
        fields = ["id", "name", "description", "meta"]


class MessageFieldsSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()


class MessageSerializer(serializers.Serializer):
    '''
    Valida que el cuerpo del mensaje POST esté bien formado
    '''
    service = serializers.IntegerField()
    message = MessageFieldsSerializer()
    meta = serializers.JSONField(required=False)
