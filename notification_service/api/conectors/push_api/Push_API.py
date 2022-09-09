import json
from .serializers import NotificationSerializer
from pywebpush import webpush


def notify(data):
    '''
    Envía notificaciones a los navegadores de los suscriptores
    '''
    serializer = NotificationSerializer(data=data)

    if not serializer.is_valid():
        raise BaseException(serializer.errors)

    for subscription in data['subscription_data']:
        webpush(
            subscription_info=subscription,
            data=json.dumps(data['message']),
            vapid_private_key='GfFUOwHGvlVfBfALVhI6-PatG1e5o383J_ZTvvJZKoc',
            vapid_claims={
                'sub': 'mailto:email@email.com'
            }
        )
