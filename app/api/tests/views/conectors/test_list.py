import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.conectors import ConectorsList
from rest_framework import status
from api.tests.views.util import FakeSerializer, create_conector, create_user
from api.serializers import ConectorsSerializer
from unittest import mock

endpoint = "/v1/conectors/"


class TestDetailsServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_many(self):
        '''Comprueba que se muestra el conector cuando el usuario esta autenticado y hay varios conectores'''

        # Creamos un nuevo usario autenticado
        user, token = create_user()
        conector1 = create_conector("Conector1")
        conector2 = create_conector("Conector2")

        with mock.patch("api.serializers.get_subscription_data_serializer") as mock_get_serializer:

            mock_get_serializer.return_value = FakeSerializer
            # Apuntamos el endpoint con el método get
            request = self.factory.get(endpoint)
            force_authenticate(request, user, token)

            # Llamamos a la vista
            response = ConectorsList.as_view()(request)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data[0], {
                "id": conector1.id,
                "name": conector1.name,
                "description": conector1.description
            })
            self.assertEqual(response.data[1], {
                "id": conector2.id,
                "name": conector2.name,
                "description": conector2.description
            })
            # Comprobamos que se NO muestra la interfaz del conector para la suscripción
            self.assertIsNone(response.data[0].get("interface"))

    def test_empty(self):
        '''Comprueba que se muestra el conector cuando el usuario esta autenticado y no hay conectores'''

        # Creamos un nuevo usario autenticado
        user, token = create_user()

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
        self.assertEqual(json.loads(response.content), {
                         "detail": f"Authentication credentials were not provided."})
