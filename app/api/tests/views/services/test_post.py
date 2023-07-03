import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services import ServicesList
from api.tests.views.util import create_user
from rest_framework import status
from rest_framework.serializers import ErrorDetail

from api.models import Service
from api.serializers import ServicesSerializer

endpoint = "/v1/services/"


class TestPostServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()


    def test_all_fields(self):
        '''Comprueba que se registra un servicio con todos los parámetro'''

        # Cuerpo del POST
        data = {"name": "service_0", "meta":{"description": "Brief description"}}

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")

        # Creamos un nuevo usario autenticado
        user, token = create_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesList.as_view()(request)

        # Obtenermos el servicio creado (el único por eso get())
        service_from_db = Service.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Comprobamos que se registra el serivico
        self.assertEqual(service_from_db.name, "service_0")

        # Comprobamos que se guardan los datos y se asigna el dueño y el campo created_at
        self.assertEqual(service_from_db.name, data["name"])
        self.assertEqual(service_from_db.owner.id, user.id)
        self.assertEqual(service_from_db.meta["description"], data["meta"]["description"])
        self.assertTrue(service_from_db.created_at, "missing created_at")

        # Comprobamos que la respuesta del post sea el servicio creado
        self.assertEqual(
            response.data, ServicesSerializer(service_from_db, context={"show_details": True}).data)

    def test_missing_name(self):
        '''Comprueba que se lanza un error cuando el serialziador lanza un error por falta el nombre vacío'''

        # Cuerpo del POST sin el campo name
        data = {"meta":{"description": "Brief description"}}

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")

        # Creamos un nuevo usario autenticado
        user, token = create_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {'name': [ErrorDetail(string='This field may not be null.', code='null')]})
    
    def test_missing_meta(self):
        '''Comprueba que se se crea un servicio sin meta cuando no se especifica'''

        # Cuerpo del POST sin el campo name
        data = {"name": "newName"}

        # POST  del data
        request = self.factory.post(endpoint, data)

        # Creamos un nuevo usario autenticado
        user, token = create_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["meta"], {})
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["owner"], user.id)
        self.assertIsNotNone(response.data["created_at"])
    
    def test_missing_all(self):
        '''Comprueba que se muestra un error indicando los campos obligatorios que faltan si no se especifica ninguno'''
        user, _ = create_user()
        data = {}

        # POST  del data
        request = self.factory.post(endpoint, data)

        # Creamos un nuevo usario autenticado
        user, token = create_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServicesList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {'name': [ErrorDetail(string='This field may not be null.', code='null')]})


    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint)

        # Llamamos a la vista
        response = ServicesList.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})