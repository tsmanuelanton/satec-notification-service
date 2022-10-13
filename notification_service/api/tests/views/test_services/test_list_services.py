import json
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from api.views.services_views import ServicesListApiView
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from api.models import Service
import random
import string

endpoint = "/v1/services/"


class TestListServices(APITestCase):

    def asser_equal(self, service_a, service_b):
        '''Comprueba que el Servicio service_a es igual al dict service_b que contiene otro servicio'''
        self.assertEqual(service_a.service_name, service_b["service_name"])
        self.assertEqual(service_a.token.key, service_b["token"])

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_services_list_empty(self):
        '''Comprueba que se devuelve una lista vacía si no hay servicios'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesListApiView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_services_list_one(self):
        '''Comprueba que se devuelve una lista con el servicio registrado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Creamos un servicio a nombre del usuario
        created_service = create_service(token)
        created_service.save()

        # Llamamos a la vista
        response = ServicesListApiView.as_view()(request)

        returned_service = dict(response.data[0])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.asser_equal(created_service, returned_service)

    def test_services_list_many(self):
        '''Comprueba que se devuelve una lista con los servicios registrado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Creamos varios servicios a nombre del usuario
        created_service0 = create_service(token)
        created_service1 = create_service(token)
        created_service0.save()
        created_service1.save()

        # Llamamos a la vista
        response = ServicesListApiView.as_view()(request)

        returned_service0 = dict(response.data[0])
        returned_service1 = dict(response.data[1])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.asser_equal(created_service0, returned_service0)
        self.asser_equal(created_service1, returned_service1)

    def test_services_list_many_notowned(self):
        '''Comprueba que se devuelve una lista con los servicios registrados a nombre del usuario '''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Registramos un servicio por otro usuario
        other_user, other_token = create_authenticated_user()
        Service(service_name="other_user_service", token=other_token).save()

        # Creamos un usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Creamos varios servicios a nombre del usuario user
        created_service0 = create_service(token)
        created_service1 = create_service(token)
        created_service0.save()
        created_service1.save()

        # Llamamos a la vista
        response = ServicesListApiView.as_view()(request)

        returned_service0 = dict(response.data[0])
        returned_service1 = dict(response.data[1])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.asser_equal(created_service0, returned_service0)
        self.asser_equal(created_service1, returned_service1)


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
