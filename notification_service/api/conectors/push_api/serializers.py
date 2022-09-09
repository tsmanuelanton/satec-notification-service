
from rest_framework import serializers


class SubscriptionDataKeysSerializer(serializers.Serializer):
    '''
    Valida el campo keys del SubscriptionData
    '''
    p256dh = serializers.CharField(max_length=128)
    auth = serializers.CharField(max_length=45)


class SubscriptionDataSerializer(serializers.Serializer):
    '''
    Valida que el campo subscription data tenga el formato esperado
    '''
    endpoint = serializers.CharField(max_length=None)
    keys = SubscriptionDataKeysSerializer(required=True)


class NotificationSerializer(serializers.Serializer):
    '''
    Valida que el cuerpo de la notificación POST esté bien formado
    '''
    subscription_data = SubscriptionDataSerializer(many=True)
    message = serializers.JSONField()
