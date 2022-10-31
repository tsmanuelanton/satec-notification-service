from abc import ABC, abstractmethod
from rest_framework.serializers import Serializer


class IConector(ABC):
    '''Interfaz que declara el contrato de todas los subtipos de conectores'''

    @abstractmethod
    def notify(self, data):
        '''Envía el mensaje a los suscriptores conenido en data'''
        pass

    @abstractmethod
    def get_subscription_serializer(self) -> Serializer:
        '''Devuelve el serializador para la suscripción de este conector'''
        pass
