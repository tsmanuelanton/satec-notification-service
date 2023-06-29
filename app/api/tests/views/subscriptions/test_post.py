import json
from unittest import mock
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.subscriptions import SubscriptionsList
from api.tests.views.util import ConectorForTest, FakeSerializer, create_subscription_group, create_user
from rest_framework import status

from api.tests.views.util import create_conector, create_service

endpoint = "/v1/subscriptions"


class TestPostSubscriptions(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_valid(self):
        '''Comprueba que se registra la suscipción con todos los campos,
          servicio existe y pertenece al usuario, el conector existe, 
          contrato del conector se cumple y el grupo existe y pertenece al servicio'''

        # Creamos un nuevo usario autenticado
        user, token = create_user()
        conector = create_conector()
        service = create_service(user)

        # Cuerpo del POST
        data = {
            "service": service.id,
            "conector": conector.id,
            "subscription_data": {"key": "Value"},
            "meta": {
                "user": "user1"
            }
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Comprobamos que se guardan los datos y se añade el campo created_at
        self.assertDictContainsSubset(data, response.data)
        self.assertTrue(response.data.get(
            "created_at", False), "missing created_at")

    def test_group_not_of_service(self):
        '''Comprueba que se lanza un error si se pasa la suscipción con todos los campos,
          servicio existe y pertenece al usuario, el conector existe, 
          contrato del conector se cumple y el grupo existe PERO no pertenece al servicio'''

        user, token = create_user()
        conector = create_conector()
        service = create_service(user)
        other_service = create_service(user)
        conector = create_conector(ConectorForTest.name)
        group = create_subscription_group(other_service)

        subscription_data = {
            "field_required": "value1",
        }

        # Cuerpo del POST
        data = {
            "service": service.id, "conector": conector.id,
            "subscription_data": subscription_data,
            "group": group.id}

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Comprobamos que indica el error
        self.assertCountEqual(response.data,
                              {'group':  ['No coincide el servicio del grupo con el de la suscripción']})

    def test_group_not_exists(self):
        ''''Comprueba que no es válido la suscipción si el grupo no existe'''

        user, _ = create_user()
        service = create_service(user)
        conector = create_conector(ConectorForTest.name)

        # Creamos un nuevo usario autenticado
        user, token = create_user()
        conector = create_conector()

        subscription_data = {
            "field_required": "value1",
        }

        # Cuerpo del POST
        data = {
            "service": service.id, "conector": conector.id,
            "subscription_data": subscription_data,
            "group": 999
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Comprobamos que indica el error
        self.assertCountEqual(
            response.data, {'group':  ['Invalid pk "999" - object does not exist.']})

    def test_conector_mismatched(self):
        '''Comprueba que se lanza error si no se cumple el contrato del conector''',

        user, token = create_user()
        conector = create_conector(ConectorForTest.name)
        service = create_service(user)
        group = create_subscription_group(service)

        subscription_data = {
            # "field_required": "value1",
            "field_not_required": "value2",
        }

        with mock.patch("api.serializers.get_subscription_data_serializer") as mock_get_serializer:
            # Mock de la función que devuelve el serializer
            mock_get_serializer.return_value = FakeSerializer
            data = {"service": service.id, "conector": conector.id,
                    "subscription_data": subscription_data, "group": group.id}

            # POST  del data
            request = self.factory.post(endpoint, data, format="json")
            force_authenticate(request, user, token)

            # Llamamos a la vista
            response = SubscriptionsList.as_view()(request)
            response.render()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(json.loads(response.content),
                             {"subscription_data": [{'field_required': ['This field is required.']}]})

    def test_conector_not_exists(self):
        '''Comprueba que se lanza error si no existe el contrato el conector''',

        user, token = create_user()
        service = create_service(user)

        data = {"service": service.id,
                "conector": 999, "subscription_data": {}}

        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"conector": [
                         'Invalid pk \"999\" - object does not exist.']})

    def test_service_not_of_user(self):
        '''Comprueba que se lanza error si el servicio no pertenece al usuario''',
        user, token = create_user()
        other_user, _ = create_user()
        service_not_owned = create_service(other_user)
        conector = create_conector(ConectorForTest.name)

        data = {"service": service_not_owned.id, "conector": conector.id,
                "subscription_data": {}, }

        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["owner"], [
                         'El servicio no existe o no pertenece al usuario'])

    def test_service_not_exists(self):
        '''Comprueba que se lanza error si el servicio no existe''',
        user, token = create_user()
        conector = create_conector(ConectorForTest.name)

        data = {"service": 999, "conector": conector.id,
                "subscription_data": {}, }

        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {
                         "service": ['Invalid pk \"999\" - object does not exist.']})

    def test_missing_service(self):
        '''Comprueba que se lanza error si falta el servicio''',

        user, token = create_user()
        conector = create_conector(ConectorForTest.name)

        data = {"conector": conector.id,
                "subscription_data": {}, }

        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {
                         "service": ['This field is required.']})

    def test_missing_conector(self):
        '''Comprueba que se lanza error si falta el conector''',

        user, token = create_user()
        service = create_service(user)

        data = {"service": service.id,
                "subscription_data": {}, }

        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["conector"], [
                         'This field is required.'])

    def test_missing_subscription_data(self):
        '''Comprueba que se lanza error si falta el subscription_data''',

        user, token = create_user()
        service = create_service(user)
        conector = create_conector(ConectorForTest.name)

        data = {"service": service.id, "conector": conector.id}

        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["subscription_data"], [
                         'This field is required.'])

    def test_missing_group(self):
        '''Comprueba que se crea una ssuscripción con grupo vacío si falta el grupo''',

        user, token = create_user()
        service = create_service(user)
        conector = create_conector(ConectorForTest.name)

        data = {"service": service.id,
                "conector": conector.id, "subscription_data": {}}

        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["group"])

    def test_missing_meta(self):
        '''Comprueba que se crea una suscripción con meta vacío si falta el meta''',

        user, token = create_user()
        service = create_service(user)
        conector = create_conector(ConectorForTest.name)

        data = {"service": service.id,
                "conector": conector.id, "subscription_data": {}}

        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["meta"], {})

    def test_mssing_all(self):
        '''Comprueba que se lanza error si falta todo''',

        user, token = create_user()

        data = {}

        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {"service": ['This field is required.'],
                          "conector": ['This field is required.'],
                          "subscription_data": ['This field is required.']})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {
                         "detail": f"Authentication credentials were not provided."})
