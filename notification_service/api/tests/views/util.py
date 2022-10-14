import random
import string
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import Service


def create_authenticated_user():
    '''Devuelve un nuevo usuario con un token asociado'''

    # Genera un nombre un aleatorio de logitud length_name
    length_name = 5
    letters = string.ascii_lowercase
    new_name = ''.join(random.choice(letters) for i in range(length_name))

    user = User.objects.create_user(
        new_name, new_name + "@test.com", "passwd" + new_name)
    token = Token.objects.create(user=user)

    return user, token


def create_service(token=None):
    '''Devuelve un nuevo servicio y opcionalmente, lo registra con el token pasado por parámetros'''

    # Genera un nombre un aleatorio de logitud length_name
    length_name = 5
    letters = string.ascii_lowercase
    new_name = ''.join(random.choice(letters) for i in range(length_name))

    return Service(service_name=new_name, token=token)
