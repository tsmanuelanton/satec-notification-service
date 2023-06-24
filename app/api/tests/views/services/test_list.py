import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services import ServicesList
from api.models import Service
from api.tests.views.util import create_authenticated_user, create_service
from api.serializers import ServicesSerializer
from rest_framework import status

endpoint = "/v1/services/"


class TestListServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_empty(self):
        '''Comprueba que se devuelve una lista vacía si no hay servicios'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_owned_and_not_owned(self):
        '''Comprueba que se devuelve una lista con sólo los servicios registrados a nombre del usuario'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Registramos un servicio por otro usuario
        other_user, _ = create_authenticated_user()
        Service(name="other_user_service",
                owner=other_user).save()

        # Creamos un usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Creamos varios servicios a nombre del usuario user
        created_service0 = create_service(user)
        created_service1 = create_service(user)
        created_service0.save()
        created_service1.save()

        # Llamamos a la vista
        response = ServicesList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data[0], ServicesSerializer(created_service0).data)
        self.assertEqual(
            response.data[1], ServicesSerializer(created_service1).data)
        
    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Llamamos a la vista
        response = ServicesList.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})
        
