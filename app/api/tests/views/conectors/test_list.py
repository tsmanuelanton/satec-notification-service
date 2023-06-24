import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.conectors import ConectorDetails, ConectorsList
from rest_framework import status
from api.tests.views.util import create_conector, create_authenticated_user
from api.serializers import ConectorsSerializer

endpoint = "/v1/conectors/"


class TestDetailsServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_empty(self):
        '''Comprueba que se muestra el conector cuando el usuario esta autenticado y hay varios conectores'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        conector1 = create_conector("Conector1")
        conector2 = create_conector("Conector2")
        conector1.save()
        conector2.save()

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ConectorsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, [ConectorsSerializer(conector1).data, ConectorsSerializer(conector2).data])

    def test_empty(self):
        '''Comprueba que se muestra el conector cuando el usuario esta autenticado y no hay conectores'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ConectorsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Llamamos a la vista
        response = ConectorsList.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})
