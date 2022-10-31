from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services_views import ServicesDetailsApiView
from rest_framework import status
from api.tests.views.util import create_service, create_authenticated_user
from api.serializers import ServicesSerializer

endpoint = "/v1/services"


class TestUpdateServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_services_update_valid(self):
        '''Comprueba que se actualiza el servicio cuando se pasan todos los campos'''

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_authenticated_user()
        my_service = create_service(token)
        my_service.save()

        # Apuntamos el endpoint con el método put y el campo service_name actualizado
        request = self.factory.put(f'{endpoint}/{my_service.id}', {
            "service_name": "name",
        })

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesDetailsApiView.as_view()(
            request, service_id=my_service.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            dict(response.data)["service_name"], "name")

    def test_services_update_empty(self):
        '''Comprueba que no se actualiza el servíco cuando no se modifica ningún campo'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        # Creamos el servicio a actualizar
        service = create_service(token)
        service.save()

        # Apuntamos el endpoint con el método put y un cuerpo vacío
        request = self.factory.put(f'{endpoint}/{service.id}', data={})

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesDetailsApiView.as_view()(request, service_id=service.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, ServicesSerializer(service).data)

    def test_services_update_not_owner(self):
        '''Comprueba que se lanza un error cuando el servicio no pertene al usuario'''

        # Creamos otro usuario con un servicio
        other_user, other_token = create_authenticated_user()
        not_owned_service = create_service(other_token)
        not_owned_service.save()

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_authenticated_user()
        my_service = create_service(token)
        my_service.save()

        # Apuntamos el endpoint con el método put a un servicio que no somos dueños
        request = self.factory.get(f'{endpoint}/{not_owned_service.id}', {
            "service_name": "name",
        })

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesDetailsApiView.as_view()(
            request, service_id=not_owned_service.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"res": f"No tienes permisos"})
