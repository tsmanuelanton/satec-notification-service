from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services_views import ServicesListApiView
from api.tests.views.util import create_authenticated_user
from rest_framework import status
from rest_framework.serializers import ErrorDetail

from api.models import Service
from api.serializers import ServicesSerializer

endpoint = "/v1/services/"


class TestPostServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_services_post_missing_service_name(self):
        '''Comprueba que se lanza un error cuando falta el campo service_name'''

        # Cuerpo del POST sin el campo service_name
        data = {}

        # POST  del data
        request = self.factory.post(endpoint, data)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesListApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {'service_name': [ErrorDetail(string='This field may not be null.', code='null')]})

    def test_services_post_valid(self):
        '''Comprueba que se registra un servicio válido'''

        # Cuerpo del POST sin el campo service_name
        data = {"service_name": "service_0"}

        # POST  del data
        request = self.factory.post(endpoint, data)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesListApiView.as_view()(request)

        # Obtenermos el servicio creado (el único por eso get())
        service_from_db = Service.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Comprobamos que se registra el serivico
        self.assertEqual(service_from_db.service_name, "service_0")
        # Comprobamos que la respuesta del post sea el servicio creado
        self.assertEqual(
            response.data, ServicesSerializer(service_from_db).data)
