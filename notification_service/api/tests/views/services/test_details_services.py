from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services_views import ServicesDetailsApiView
from rest_framework import status
from api.tests.views.util import create_service, create_authenticated_user
from api.serializers import ServicesSerializer

endpoint = "/v1/details"


class TestDetailsServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_services_details_null(self):
        '''Comprueba que se lanza un error cuando no existe la id del servicio'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesDetailsApiView.as_view()(request, service_id=1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"res": f"Servicio con id 1 no existe"})

    def test_services_details_owner(self):
        '''Comprueba que se muestran los datos cuando el servicio pertenece al usuario'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_authenticated_user()
        my_service = create_service(token)
        my_service.save()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesDetailsApiView.as_view()(
            request, service_id=my_service.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, ServicesSerializer(my_service).data)

    def test_services_details_not_owner(self):
        '''Comprueba que se lanza un error cuando el servicio no pertene al usuario'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos otro usuario con un servicio
        other_user, other_token = create_authenticated_user()
        not_owned_service = create_service(other_token)
        not_owned_service.save()

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_authenticated_user()
        my_service = create_service(token)
        my_service.save()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesDetailsApiView.as_view()(
            request, service_id=not_owned_service.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"res": f"No tienes permisos"})
