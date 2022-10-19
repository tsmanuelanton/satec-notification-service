import random
import string
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import Service, Conector


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


def create_service(token=None):
    '''Devuelve un nuevo servicio y, opcionalmente, lo registra con el token pasado por parámetros'''
    # Genera un nombre un aleatorio
    new_name = gen_random_word()
    return Service(service_name=new_name, token=token)


def create_conector():
    '''Devuelve un nuevo conector'''
    # Genera un nombre un aleatorio
    new_name = gen_random_word()

    return Conector(name=new_name, description=f"Descripción de {new_name}", meta={"Key": new_name})
