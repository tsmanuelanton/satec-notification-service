import random
import string
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import Service, Conector, Subscription, SubscriptionGroup
from api.conectors.IConector import IConector
from rest_framework import serializers

class ConectorForTest(IConector):
    '''Conector para pruebas'''

    name = "ConectorForTest"

    def getDetails() -> dict:
        return {
            'name': ConectorForTest.name,
        }

    async def notify(data, options={}) -> dict or None:
        return None

    def get_subscription_serializer() -> serializers:
        return FakeSerializer
    

class FakeSerializer(serializers.Serializer):
    '''Serializador para pruebas'''
    field_required = serializers.CharField(required=True)
    field_not_required = serializers.CharField(required=False)


def gen_random_word(length=5) -> string:
    length_name = length
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length_name))


def create_authenticated_user():
    '''Devuelve un nuevo usuario con un token asociado'''

    # Genera un nombre un aleatorio
    new_name = gen_random_word()

    user = User.objects.create_user(
        new_name, f"{new_name}@test.com", f"passwd{new_name}")
    token = Token.objects.create(user=user)

    return user, token


def create_service(user):
    '''Devuelve un nuevo servicio y, opcionalmente, lo registra con el token pasado por parámetros'''
    # Genera un nombre un aleatorio
    new_name = gen_random_word()
    return Service(name=new_name, owner=user)


def create_conector(name: str = None):
    '''Devuelve un nuevo conector'''
    # Genera un nombre un aleatorio
    new_name = name or gen_random_word()

    return Conector(name= name or new_name, description=f"Descripción de {new_name}", meta={"Key": new_name})


def create_subscription(service: Service, conector: Conector, group : SubscriptionGroup = None) -> Subscription:
    '''Devuelve un nueva suscripción asociada al servicio
    y conector que se pasan por parámetros'''
    # Genera un nombre un aleatorio
    value = gen_random_word()
    return Subscription(service=service, conector=conector,
                         subscription_data={"Field": value}, group=group)

def create_subscription_group(service: Service) -> Subscription:
    '''Devuelve un nuevo grupo de suscripción asociada al servicio que se pase por parámetros'''
    # Genera un nombre un aleatorio
    value = gen_random_word()
    return SubscriptionGroup(service=service, name=value)
