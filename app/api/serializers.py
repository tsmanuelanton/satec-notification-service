from datetime import datetime
from rest_framework import serializers
from .models import Conector, Subscription, Service, SubscriptionGroup


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        extra_kwargs = {
            "conector": {
                "error_messages": {
                    "does_not_exist": "Unknown conector"
                }
            }, "service": {"error_messages": {
                "does_not_exist": "Unknown service"}}}
        
    # Cuando se crea la subscripción, se añade el campo created_at al meta
    def create(self, validated_data):
        validated_data = add_createat_field(validated_data)
        return super().create(validated_data)

class SubscriptionGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionGroup
        fields = "__all__"
        
    # Cuando se crea el grupo, se añade el campo created_at al meta
    def create(self, validated_data):
        validated_data = add_createat_field(validated_data)
        return super().create(validated_data)
    
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation["subscriptions"] = SubscriptionsSerializer(Subscription.objects.filter(group=instance.id), many=True).data
        return representation

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
    
    # Cuando se crea el servicio, se añade el campo created_at al meta
    def create(self, validated_data):
        validated_data = add_createat_field(validated_data)
        return super().create(validated_data)


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
    options = serializers.JSONField(required=False, default={})
    restricted_to = serializers.ListField(required=False, default=list)

def add_createat_field(validated_data):
    created__at = {"created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    if validated_data.get("meta") and type(validated_data.get("meta")) == dict: # Si ya existe el campo meta añadir created_at
        validated_data["meta"].update(created__at)
    else: # Si no existe el campo meta, crearlo con created_at
        validated_data["meta"] = created__at
    return validated_data