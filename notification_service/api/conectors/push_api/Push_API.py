import json

from notification_service.api.models import Subscription
from .serializers import NotificationSerializer
from pywebpush import webpush, WebPushException
from os import path
from django.conf import settings

vapid_pkey_file_path = path.join(
    settings.BASE_DIR, "api", "conectors", "push_api", "secrets", "private_key.pem")

# Comprobamos que existe la key
try:
    open(vapid_pkey_file_path, "r")
except FileNotFoundError as e:
    raise FileNotFoundError(
        "No se ha encontrado la clave PRIVADA VAPID en " + e.filename)


def notify(data):
    '''
    Envía notificaciones a los navegadores de los suscriptores
    '''
    serializer = NotificationSerializer(data=data)

    if not serializer.is_valid():
        raise SyntaxError(serializer.errors)

    try:
        webpush(
            subscription_info=data['subscription']['subscription_data'],
            data=data['message'],
            vapid_private_key=vapid_pkey_file_path,
            vapid_claims={
                'sub': 'mailto:manuel.anton@satec.es'
            }
        )

    except WebPushException as e:
        # Si el Push Service lanza un error Gone 410 es que el usuario ya no está suscrito
        if e.response.status_code == 410:
            # Borramos la suscripción de nuestra BD
            data['subscription'].delete()
        else:
            raise e
