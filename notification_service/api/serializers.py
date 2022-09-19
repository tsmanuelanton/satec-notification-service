from rest_framework import serializers
from .models import Conector, Subscription, Service


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "service_id", "conector_id",
                  "subscription_data", "token"]


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "service_name", "token"]


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
    token = serializers.CharField(max_length=45)


class DeleteSubsciptionSerilizer(serializers.Serializer):
    '''
    Valida que el cuerpo del DELETE de la suscipción
    '''

    field_name = serializers.CharField(max_length=45)
    field_value = serializers.CharField(max_length=None)
    service_name = serializers.CharField(max_length=60)
    token = serializers.CharField(max_length=45)
