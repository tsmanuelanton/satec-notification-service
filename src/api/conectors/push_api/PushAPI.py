import json
from api.conectors.IConector import IConector
from .serializers import NotificationSerializer, SubscriptionDataSerializer
from pywebpush import webpush, WebPushException
from os import environ
from rest_framework import serializers


class PushAPIConector(IConector):

    # Dict que asigna a errores de HTTP una descripción fácil de enteder
    res_des = {
        401: "Clavé publica y privada no coinciden",
        410: "El usuario ha eliminado su suscripción manualmente"
    }

    def getDetails():
        return {
            "name": "Push API - Navegadores",
            "description": "Permite enviar notificacion a los clientes a través de los navegadores mediante la API PUSH",
            "meta": {
                "ApplicationServerKey": environ.get("PUSH_API_APP_SERVER_KEY")
            }
        }

    def notify(data, meta={}) -> bool:
        serializer = NotificationSerializer(data=data)

        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)
        try:
            a = webpush(
                subscription_info=data['subscription_data'],
                data=json.dumps({**data["message"], **meta}),
                vapid_private_key=environ.get("PUSH_API_PRIVATE_KEY"),
                vapid_claims={
                    'sub': 'mailto:manuel.anton@satec.es'
                }
            )

            return True, None

        except WebPushException as e:
            # Si el Push Service lanza un error Gone 410 es que el usuario ya no está suscrito
            # Si el Push Service lanza un error Gone 401 es que no coinciden la key pública y la privada del servidor
            if e.response != None:
                description = PushAPIConector.res_des.get(
                    e.response.status_code) or e.message
                return False, description
            else:
                return False, e.message

    def get_subscription_serializer():
        return SubscriptionDataSerializer
