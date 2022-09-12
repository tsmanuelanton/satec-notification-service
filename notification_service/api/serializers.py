from dataclasses import fields
from rest_framework import serializers
from .models import Conector, Subscription, Service


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "service_id", "conector_id", "subscription_data"]


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "service_name"]


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
