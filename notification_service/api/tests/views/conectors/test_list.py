from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.tests.views.util import create_authenticated_user
from api.views.conectors_views import ConectorsListApiView
from api.models import Conector
from api.serializers import ConectorsSerializer

endpoint = "/v1/conectors/"


class TestListServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_conectors_list_empty(self):
        '''Comprueba que se devuelve una lista vacía si no hay conectores'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ConectorsListApiView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_conectors_list_one(self):
        '''Comprueba que se devuelve una lista con el conector registrado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Creamos un conector
        created_conector = Conector(
            name="Conector1", description="Conector prueba 1", meta={})
        created_conector.save()

        # Llamamos a la vista
        response = ConectorsListApiView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0], ConectorsSerializer(created_conector).data)

    def test_conectors_list_many(self):
        '''Comprueba que se devuelve una lista con los conectores registrados'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Creamos un conector
        created_conector1 = Conector(
            name="Conector2", description="Conector prueba 2", meta={"Key": "Value"})
        created_conector1.save()

        created_conector2 = Conector(
            name="Conector3", description="Conector prueba 3", meta={})
        created_conector2.save()

        # Llamamos a la vista
        response = ConectorsListApiView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data[0], ConectorsSerializer(created_conector1).data)
        self.assertEqual(
            response.data[1], ConectorsSerializer(created_conector2).data)
