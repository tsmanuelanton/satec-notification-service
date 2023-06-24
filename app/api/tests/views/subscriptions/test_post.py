import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.subscriptions import SubscriptionsList
from api.tests.views.util import create_authenticated_user
from rest_framework import status

from api.tests.views.util import create_conector, create_service

endpoint = "/v1/subscriptions"


class TestPostSubscriptions(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_valid(self):
        '''Comprueba que se registra la suscripción cuando el usuario es el propietario,
            servicio existe,conector existe, la suscripción es válida, y el grupo existe.'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        conector = create_conector()
        service = create_service(user)

        conector.save()
        service.save()

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
        self.assertTrue(response.data.get("created_at", False), "missing created_at")

    def test_not_valid(self):
        '''Comprueba que se lanza un error mostrando los errores cuando el serializador encuentra errores'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        conector = create_conector()

        conector.save()

        # Cuerpo del POST
        data = {
            "service": 1,
            "conector": conector.id,
            "meta": {
                "user": "user1"
            }
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Comprobamos que indica el error
        self.assertCountEqual(json.loads(response.content), {'service':  ['Invalid pk "1" - object does not exist.'], 
                                                             'subscription_data': ['This field is required.']})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})