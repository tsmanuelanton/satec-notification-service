from abc import ABC, abstractmethod
from rest_framework.serializers import Serializer


class IConector(ABC):
    '''Interfaz que declara el contrato de todas los subtipos de conectores'''

    @abstractmethod
    def getDetails():
        '''Devuelve un diccionario con los detalles del conector'''
        raise NotImplementedError

    @abstractmethod
    async def notify(data, meta={}) -> dict or None:
        '''Envía notificaciones a los navegadores de los suscriptores y
        devuelve un dic si se ha producido un error'''
        raise NotImplementedError

    @abstractmethod
    def get_subscription_serializer() -> Serializer:
        '''Devuelve el serializador para la suscripción de este conector'''
        raise NotImplementedError
