from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.notifications_views import NotificationsApiView
from api.tests.views.util import create_authenticated_user, create_service
from rest_framework import status
from rest_framework.serializers import ErrorDetail

endpoint = "/v1/notifications/"


class TestPostNotifications(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_notifications_post_missing_service_id(self):
        '''Comprueba que se lanza un error cuando falta el id del servicio'''

        # Cuerpo del POST sin el campo service_id
        data = {
            "message": {
                "title": "Test",
                "body": "TestBody"
            }
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = NotificationsApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {'service': [ErrorDetail(string='This field is required.', code='required')]})

    def test_notifications_post_messing_message(self):
        '''Comprueba que se lanza un error cuando falta el id del servicio'''

        # Creamos un nuevo usario
        user, token = create_authenticated_user()

        service = create_service(user)
        service.save()

        # Cuerpo del POST sin el campo message
        data = {
            "service": service.id
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = NotificationsApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {'message': [ErrorDetail(string='This field is required.', code='required')]})

    def test_notifications_post_null_service(self):
        '''Comprueba que se lanza un error cuando el servicio no existe'''

        # Cuerpo del POST
        data = {
            "service": 0,
            "message": {
                "title": "Test",
                "body": "TestBody"
            }
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = NotificationsApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"res": f"Unknown service."})

    def test_notifications_post_not_owned_service(self):
        '''Comprueba que se lanza un error cuando el servicio no es nuestro'''

        # Registramos un servicio por otro usuario
        other_user, other_token = create_authenticated_user()

        service = create_service(other_user)
        service.save()

        # Cuerpo del POST
        data = {
            "service": service.id,
            "message": {
                "title": "Test",
                "body": "TestBody"
            }
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = NotificationsApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'res': 'No tienes permisos.'})
