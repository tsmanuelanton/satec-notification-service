from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services_views import ServicesDetailsApiView
from api.tests.views.util import create_authenticated_user, create_service
from rest_framework import status

endpoint = "/v1/services/"


class TestDeleteServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_services_delete_forbidden(self):
        '''Comprueba que se lanza un error al intentar borrar un servicio que no pertene al usuario'''

        request = self.factory.delete(endpoint)

        # Creamos otro usario con un servicio
        other_user, _ = create_authenticated_user()
        not_owner_service = create_service(other_user)
        not_owner_service.save()

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Intentamos realizar un delete con el id del servicio que no poseemos
        service_id = not_owner_service.id
        response = ServicesDetailsApiView.as_view()(request, service_id=service_id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"res": f"No tienes permisos."})

    def test_services_delete_null(self):
        '''Comprueba que se lanza un error al intentar borrar un servicio que no existe'''

        request = self.factory.delete(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        service_id = 1

        # Llamamos a la vista
        response = ServicesDetailsApiView.as_view()(request, service_id=service_id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"res": f"Servicio con id {service_id} no existe."})

    def test_services_delete_valid(self):
        '''Comprueba que se borra el servicio correctamente'''

        request = self.factory.delete(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Registramos un serivcio a este usuario
        service = create_service(user)
        service.save()

        # Llamamos a la vista
        response = ServicesDetailsApiView.as_view()(request, service_id=service.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"res": "Servicio eliminado."})
