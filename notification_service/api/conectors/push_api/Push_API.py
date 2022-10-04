from api.models import Subscription
from .serializers import NotificationSerializer, SubscriptionDataSerializer
from pywebpush import webpush, WebPushException
from os import environ
from rest_framework import serializers

# Comprobamos que hay una variabla con la clave privada
try:
    environ["PUSH_API_PRIVATE_KEY"]
except KeyError as e:
    raise EnvironmentError(
        "Conector PUSH_API: No está definida la variable con la clave PRIVADA VAPID")


def notify(data):
    '''
    Envía notificaciones a los navegadores de los suscriptores
    '''
    serializer = NotificationSerializer(data=data)

    if not serializer.is_valid():
        raise serializers.ValidationError(serializer.errors)

    try:
        webpush(
            subscription_info=data['subscription_data'],
            data=data['message'],
            vapid_private_key=environ.get("PUSH_API_PRIVATE_KEY"),
            vapid_claims={
                'sub': 'mailto:manuel.anton@satec.es'
            }
        )

    except WebPushException as e:
        # Si el Push Service lanza un error Gone 410 es que el usuario ya no está suscrito
        # Si el Push Service lanza un error Gone 401 es que no coinciden la key pública y la privada del servidor
        if e.response.status_code == 410 or e.response.status_code == 401:
            # Borramos la suscripción de nuestra BD
            subscription = Subscription.objects.get(
                id=data['subscription_id'])
            subscription.delete()
        else:
            raise e


def get_subscription_serializer():
    return SubscriptionDataSerializer
