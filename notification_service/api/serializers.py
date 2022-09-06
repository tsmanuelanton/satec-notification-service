from rest_framework import serializers
from .models import Subscription, Service


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "service_id", "subscription_data"]


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "service_name"]


class NotificationSerializer(serializers.Serializer):
    '''
    Valida que el cuerpo de la notificación POST esté bien formado
    '''
    service_id = serializers.IntegerField()
    message = serializers.JSONField()
