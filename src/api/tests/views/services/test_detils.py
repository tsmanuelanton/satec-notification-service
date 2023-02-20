from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services_views import ServicesDetailsApiView
from rest_framework import status
from api.tests.views.util import create_service, create_authenticated_user
from api.serializers import ServicesSerializer

endpoint = "/v1/services"


class TestDetailsServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_services_details_owner(self):
        '''Comprueba que se muestran los datos cuando el servicio pertenece al usuario'''

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_authenticated_user()
        my_service = create_service(user)
        my_service.save()

        # Apuntamos el endpoint con el método get
        request = self.factory.get(f'{endpoint}/{my_service.id}')

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesDetailsApiView.as_view()(
            request, service_id=my_service.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, ServicesSerializer(my_service).data)

    def test_services_details_not_owner(self):
        '''Comprueba que se lanza un error cuando el servicio no pertene al usuario'''

        # Creamos otro usuario con un servicio
        other_user, other_token = create_authenticated_user()
        not_owned_service = create_service(other_user)
        not_owned_service.save()

        request = self.factory.get(f'{endpoint}/{not_owned_service.id}')

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesDetailsApiView.as_view()(
            request, service_id=not_owned_service.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"res": f"No tienes permisos"})

    def test_services_details_null(self):
        '''Comprueba que se lanza un error cuando no existe el servicio'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint + "/1")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesDetailsApiView.as_view()(request, service_id=1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"res": f"Servicio con id 1 no existe"})
