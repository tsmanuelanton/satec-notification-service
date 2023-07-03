from datetime import datetime
from rest_framework import serializers
from .models import Conector, Subscription, Service, SubscriptionGroup
from api.util import import_conectors
from api.models import Conector

class SubscriptionsSerializer(serializers.ModelSerializer):
    # Cuando se crea la suscripción, se registra la fecha de creación
    created_at = serializers.CreateOnlyDefault(datetime.now)
    class Meta:
        model = Subscription
        fields = "__all__"
    
    def is_valid(self, raise_exception=False):
        valid = super().is_valid(raise_exception=raise_exception)
        if valid:
            user = self.context["request"].user
            service = getattr(self.instance, "service", None) or self.validated_data.get("service")
            # Comprobamos que el servicio pertenece al usuario
            if service and service.owner != user:
                self._errors["owner"] = ["El servicio no existe o no pertenece al usuario"]
                valid = False
            
            # Comprobamos que el grupo pertenece al servicio
            group = self.validated_data.get("group")
            if group and group.service.owner != user:
                self._errors["group"] = ["El grupo no existe o no pertenece al servicio"]
                valid = False

            # Comprobamos que el servicio del grupo coincide con el del servicio de la suscripción
            group = self.validated_data.get("group")
            if group and group.service != service:
                self._errors["group"] = ["No coincide el servicio del grupo con el de la suscripción"]
                valid = False

            # Comprobamos con el serializador específico del conector si los datos de la suscripción son válidos
            subscription_data = self.validated_data.get("subscription_data")
            conector = self.validated_data.get("conector") or getattr(self.instance, "conector", None)
            if conector and subscription_data:
                valid_sub, errors_sub = is_good_subscription_data(subscription_data, conector)
                if not valid_sub:
                    self._errors["subscription_data"] = [errors_sub]
                    valid = False

        return valid
    
    def update(self, instance, validated_data):
        # No se puede modificar el servicio ni el conector
        validated_data.pop("service", None)
        validated_data.pop("conector", None)
        return super().update(instance, validated_data)

    def to_representation(self,instance):
        representation = super().to_representation(instance)

        if not self.context.get("show_details"):
            representation.pop("meta")
            representation.pop("subscription_data")
            representation.pop("created_at")
            representation.pop("group")
        return representation

class SubscriptionGroupsSerializer(serializers.ModelSerializer):
    # Cuando se crea el grupo, se registra la fecha de creación
    created_at = serializers.CreateOnlyDefault(datetime.now)
    class Meta:
        model = SubscriptionGroup
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        '''Comprobamos que el servicio del grupo pertenece al usuario'''
        valid = super().is_valid(raise_exception=raise_exception)
        if valid:
            user = self.context["request"].user
            service = self.validated_data.get("service")
            if service and service.owner != user:
                self._errors["service"] = ["El servicio no existe o no pertenece al usuario"]
                valid = False
        return valid
    
    def to_representation(self,instance):
        representation = super().to_representation(instance)

        if self.context.get("show_details"):
            subscriptions_in_group = Subscription.objects.filter(group=instance.id)
            representation["subscriptions"] = SubscriptionsSerializer(subscriptions_in_group, many=True).data
        else:
            representation.pop("meta")
            representation.pop("created_at")
        return representation
    
    def update(self, instance, validated_data):
        # No se puede modificar el servicio
        validated_data.pop("service", None)
        return super().update(instance, validated_data)

class ServicesSerializer(serializers.ModelSerializer):
    # Cuando se crea el servicio, se registra la fecha de creación
    created_at = serializers.CreateOnlyDefault(datetime.now)
    class Meta:
        model = Service
        fields = "__all__"
    
    def is_valid(self, raise_exception=False):
        '''Añade el usuario al servicio'''
        user = self.context["request"].user

        self.initial_data["owner"] = user.id
        valid = super().is_valid(raise_exception=raise_exception)
        return valid
    
    def update(self, instance, validated_data):
        # No se puede modificar el dueño
        validated_data.pop("owner", None)
        return super().update(instance, validated_data)
    
    def to_representation(self,instance):
        representation = super().to_representation(instance)

        if not self.context.get("show_details"):
            representation.pop("meta")
            representation.pop("created_at")
        return representation
    


class ConectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conector
        fields = ["id", "name", "description", "meta"]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context.get("show_details"):
            # Añadimos el contrato del conector para las suscripciones
            serializer = get_subscription_data_serializer(instance)
            if not serializer:
                raise ValueError(f"Conector {instance.name} no tiene definido un serializador para los datos de suscripción")
            
            representation["interface"] = get_serializer_fields(serializer)
        else:
            representation.pop("meta")
            
        return representation
    


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
    restricted_to_groups = serializers.ListSerializer(required=False, child=serializers.IntegerField(), default=[])

    async def is_valid(self, raise_exception=False):
        # Validamos que si está restringido a grupos, los grupos existan en el servicio
        valid = super().is_valid(raise_exception=raise_exception)
        restricted_to_groups = self.validated_data.get('restricted_to_groups')

        service = self.validated_data.get('service')
        fails = []
        if restricted_to_groups:
            for group_id in restricted_to_groups:
                if not await SubscriptionGroup.objects.filter(id=group_id, service_id=service).aexists():
                    fails.append(f"El grupo con {group_id} no existe")
                    valid = False
        if len(fails) > 0:
            self._errors["restricted_to_groups"] = fails
        return valid
    

def get_subscription_data_serializer(conector: Conector):
    '''
    Devuelve el serializador del subscription_data del conector
    '''
    available_conectors = import_conectors("api/conectors")
    for available_con in available_conectors:
        if conector.name == available_con.getDetails().get("name"):
            return available_con.get_subscription_serializer()

def is_good_subscription_data(subscription_data, conector):
    # Comprobamos con el serializador específico del conector si los datos de la suscripción son válidos
    subscription_serializer = get_subscription_data_serializer(conector)
    if subscription_serializer and subscription_data:
        serializer = subscription_serializer(data=subscription_data)
        valid = serializer.is_valid()
        if not valid:
            return False, serializer.errors
    
    return True, None

def get_serializer_fields(serializer):
    '''Devuelve información sobre los campos del serializador'''
    declared_fields = serializer.__dict__["_declared_fields"]
    field_pairs = {key:value for key, value in declared_fields.items()}
    return str(field_pairs)