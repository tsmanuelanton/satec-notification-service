import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.subscriptions import SubscriptionDetails
from rest_framework import status
from api.tests.views.util import FakeSerializer, ConectorForTest, create_service, create_user, create_conector, create_subscription, create_subscription_group
from api.serializers import SubscriptionsSerializer
from api.models import Subscription
from unittest import mock

endpoint = "/v1/subscriptions"


class TestUpdateSubscriptions(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_valid(self):
        '''Comprueba que se actualizan los campos introducidos, menos servicio, 
        conector y fecha de creación si el usuario es dueño y
        el grupo pertenece al servicio y la suscripción es compatible con el conector'''

        # Creamos un nuevo usario autenticado
        user, token = create_user()

        conector = create_conector(ConectorForTest.name)
        service = create_service(user)
        group1 = create_subscription_group(service)
        group2 = create_subscription_group(service)
        subscription = create_subscription(service, conector, group1)

        # Cuerpo del PUT
        data = {
            "subscription_data": {"field_required": "Value"},
            "group": group2.id,
            "meta": {
                "user": "user1"
            }
        }

        # PUT  del data
        request = self.factory.put(
            f"{endpoint}/{subscription.id}", data, format="json")
        force_authenticate(request, user, token)

        with mock.patch("api.serializers.get_subscription_data_serializer") as mock_get_serializer:
            mock_get_serializer.return_value = FakeSerializer
            # Llamamos a la vista
            response = SubscriptionDetails.as_view()(
                request, subscription_id=subscription.id)

            self.assertEqual(response.status_code,
                             status.HTTP_200_OK, response.data)

            self.assertDictContainsSubset({
                "id": subscription.id,
                "service": service.id,
                "conector": conector.id,
                "subscription_data": {"field_required": "Value"},
                "group": group2.id,
                "meta": {
                    "user": "user1"
                }}, response.data)

            self.assertEqual(response.data.get(
                "created_at"), subscription.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_empty(self):
        '''Comprueba que si no se pasa ningún campo,
            no se actualiza ningún campo.'''

        # Creamos un nuevo usario autenticado
        user, token = create_user()

        conector = create_conector(ConectorForTest.name)
        service = create_service(user)
        group1 = create_subscription_group(service)
        subscription = create_subscription(service, conector, group1)

        # Cuerpo del PUT
        data = {}

        with mock.patch("api.serializers.get_subscription_data_serializer") as mock_get_serializer:
            mock_get_serializer.return_value = FakeSerializer

            # PUT  del data
            request = self.factory.put(
            f"{endpoint}/{subscription.id}", data, format="json")
            force_authenticate(request, user, token)

            # Llamamos a la vista
            response = SubscriptionDetails.as_view()(
                request, subscription_id=subscription.id)

            self.assertEqual(response.status_code,
                             status.HTTP_200_OK, response.data)

            self.assertDictContainsSubset({
                "id": subscription.id,
                "service": service.id,
                "conector": conector.id,
                "subscription_data": subscription.subscription_data,
                "group": group1.id,
                "meta": subscription.meta
            }, response.data)

            self.assertEqual(response.data.get(
                "created_at"), subscription.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_not_compatible(self):
        '''Comprueba que se lanza un error si la suscripción es incompatible con el conector'''
        # Creamos un nuevo usario autenticado
        user, token = create_user()
        conector = create_conector(ConectorForTest.name)
        service = create_service(user)
        subscription = create_subscription(service, conector)

        subscription_data = {
            # "field_required": "value1",
            "field_not_required": "value2",
        }

        with mock.patch("api.serializers.get_subscription_data_serializer") as mock_get_serializer:
            mock_get_serializer.return_value = FakeSerializer

            data = {"subscription_data": subscription_data}

            # PUT  del data
            request = self.factory.put(
                f"{endpoint}/{subscription.id}", data, format="json")
            force_authenticate(request, user, token)

            # Llamamos a la vista
            response = SubscriptionDetails.as_view()(
                request, subscription_id=subscription.id)
            response.render()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(json.loads(response.content),
                             {"subscription_data": [{'field_required': ['This field is required.']}]})

    def test_group_invalid(self):
        '''Comprueba que se lanza un error si el grupo no pertenece al servicio'''

        user, token = create_user()
        conector = create_conector(ConectorForTest.name)
        service1 = create_service(user)
        service2 = create_service(user)
        subscription = create_subscription(service1, conector)
        group = create_subscription_group(service2)

        # Cuerpo del POST
        data = {
            "group": group.id
        }

        # POST  del data
        request = self.factory.put(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(
            request, subscription_id=subscription.id)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Comprobamos que indica el error
        self.assertCountEqual(response.data,
                              {'group':  ['No coincide el servicio del grupo con el de la suscripción']})

    def test_group_inexistant(self):
        '''Comprueba que se lanza un error si el grupo no existe'''

        user, token = create_user()
        conector = create_conector(ConectorForTest.name)
        service = create_service(user)
        subscription = create_subscription(service, conector)

        # Cuerpo del POST
        data = {
            "group": 1
        }

        # POST  del data
        request = self.factory.put(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(
            request, subscription_id=subscription.id)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Comprobamos que indica el error
        self.assertCountEqual(response.data,
                              {'group':  ['No coincide el servicio del grupo con el de la suscripción']})

    def test_not_exists(self):
        '''Comprueba que se lanza un error cuando el usuario no es el dueño de la suscripción'''

        user, token = create_user()
        other_user, _ = create_user()
        service_not_owned = create_service(other_user)
        conector = create_conector()
        subscription_not_owned = create_subscription(
            service_not_owned, conector)

        # Apuntamos el endpoint con el método put
        request = self.factory.put(f"{endpoint}/{subscription_not_owned}")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(
            request, subscription_id=subscription_not_owned.id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {
                         "detail": f"You do not have permission to perform this action."})

    def test_not_exists(self):
        '''Comprueba que se lanza error si no existe la suscripción'''

        user, token = create_user()
        # Apuntamos el endpoint con el método put
        request = self.factory.put(f"{endpoint}/{999}")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(
            request, subscription_id=999)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {
                         "detail": f"Subscription 999 not found."})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método put
        request = self.factory.put(f"{endpoint}/{1}")

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {
                         "detail": f"Authentication credentials were not provided."})
