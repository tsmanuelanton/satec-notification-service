import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services import ServiceDetails
from rest_framework import status
from api.tests.views.util import create_service, create_user
from api.serializers import ServicesSerializer

endpoint = "/v1/services"


class TestDetailsServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_user_is_owner(self):
        '''Comprueba que se muestran los datos cuando el servicio pertenece al usuario'''

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_user()
        my_service = create_service(user)

        # Apuntamos el endpoint con el método get
        request = self.factory.get(f'{endpoint}/{my_service.id}')

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(
            request, service_id=my_service.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, ServicesSerializer(my_service).data)

    def test_not_owner(self):
        '''Comprueba que se lanza un error cuando el servicio no pertene al usuario'''

        # Creamos otro usuario con un servicio
        other_user, _ = create_user()
        not_owned_service = create_service(other_user)

        request = self.factory.get(f'{endpoint}/{not_owned_service.id}')

        # Creamos un nuevo usario autenticado
        user, token = create_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(
            request, service_id=not_owned_service.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": f"You do not have permission to perform this action."})

    def test_service_not_exist(self):
        '''Comprueba que se lanza un error cuando no existe el servicio'''

        # Creamos un nuevo usario autenticado
        user, token = create_user()

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint + "/1")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(request, service_id=1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"detail": f"Service 1 not found."})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint + "/1")

        # Llamamos a la vista
        response = ServiceDetails.as_view()(request, service_id=1)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})
