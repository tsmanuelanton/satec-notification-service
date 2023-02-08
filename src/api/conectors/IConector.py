from abc import ABC, abstractmethod
from rest_framework.serializers import Serializer


class IConector(ABC):
    '''Interfaz que declara el contrato de todas los subtipos de conectores'''

    @abstractmethod
    def getDetails():
        '''Devuelve un diccionario con los detalles del conector'''

    @abstractmethod
    def notify(data, meta={}):
        '''Envía notificaciones a los navegadores de los suscriptores y
        devuelve True si ha tenido éxito la operación'''
        pass

    @abstractmethod
    def get_subscription_serializer() -> Serializer:
        '''Devuelve el serializador para la suscripción de este conector'''
        pass
