from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services_views import ServicesListApiView
from api.models import Service
from api.tests.views.util import create_authenticated_user, create_service
from api.serializers import ServicesSerializer

endpoint = "/v1/services/"


class TestListServices(APITestCase):

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
        created_service = create_service(user)
        created_service.save()

        # Llamamos a la vista
        response = ServicesListApiView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0], ServicesSerializer(created_service).data)

    def test_services_list_many(self):
        '''Comprueba que se devuelve una lista con los servicios registrado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Creamos varios servicios a nombre del usuario
        created_service0 = create_service(user)
        created_service1 = create_service(user)
        created_service0.save()
        created_service1.save()

        # Llamamos a la vista
        response = ServicesListApiView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data[0], ServicesSerializer(created_service0).data)
        self.assertEqual(
            response.data[1], ServicesSerializer(created_service1).data)

    def test_services_list_many_notowned(self):
        '''Comprueba que se devuelve una lista con los servicios registrados a nombre del usuario '''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Registramos un servicio por otro usuario
        other_user, other_token = create_authenticated_user()
        Service(service_name="other_user_service",
                service_owner=other_user).save()

        # Creamos un usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Creamos varios servicios a nombre del usuario user
        created_service0 = create_service(user)
        created_service1 = create_service(user)
        created_service0.save()
        created_service1.save()

        # Llamamos a la vista
        response = ServicesListApiView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data[0], ServicesSerializer(created_service0).data)
        self.assertEqual(
            response.data[1], ServicesSerializer(created_service1).data)
