import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework import status
from api.tests.views.util import create_conector, create_service, create_user, create_subscription, create_subscription_group
from api.views.subscription_groups import SubscriptionGroupDetails
from api.serializers import SubscriptionsSerializer

endpoint = "/v1/groups"

class TestPutSubscriptionGroup(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_authenticated_modify_all(self):
        '''Comprueba que se modifica el grupo excepto servicio y fecha de creación cuando
          el usuario está autenticado e introduce todos los campos'''

        user, token = create_user()
        service = create_service(user)
        group = create_subscription_group(service)
        new_service = create_service(user)

        data = {
            "name": "Grupo de prueba",
            "service": new_service.id,
            "meta": {
                "field": "value"
            }
        }

        # Apuntamos el endpoint con el método get
        request = self.factory.put(f'{endpoint}/{group.id}', data=data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupDetails.as_view()(
            request, group_id=group.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({
            "id": group.id,
            "name": "Grupo de prueba",
            "service": service.id,
            "meta": {
                "field": "value"
            }
        }, response.data)
        self.assertIsNotNone(response.data.get("created_at"))

    def test_missing_all(self):
        '''Comprueba que no se actualiza ningún campo si no se introduce ningún campo'''
        user, token = create_user()
        service = create_service(user)
        group = create_subscription_group(service)

        data = {}
         # Apuntamos el endpoint con el método get
        request = self.factory.put(f'{endpoint}/{group.id}', data=data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupDetails.as_view()(
            request, group_id=group.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {
            "id": group.id,
            "service": service.id,
            "name": group.name,
            "meta": group.meta,
            "subscriptions": [],
            "created_at": group.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        })
    
    def test_not_owner(self):
        '''Comprueba no se produce ningún error ni cambio si no se introducen campos'''

        user, token = create_user()
        another_user, _ = create_user()
        service = create_service(another_user)
        conector = create_conector()
        group = create_subscription_group(service)
        create_subscription(service, conector, group) # subscription_in_group
        
        data = {
            "name": "Grupo de prueba",
        }

        # Apuntamos el endpoint con el método get
        request = self.factory.put(f'{endpoint}/{group.id}', data=data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupDetails.as_view()(
            request, group_id=group.id)

        response.render()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"You do not have permission to perform this action."})

    def test_group_non_existent(self):
        '''Comprueba no se produce ningún error ni cambio si no se introducen campos'''

        user, token = create_user()
       
        data = {
            "name": "Grupo de prueba",
        }

        # Apuntamos el endpoint con el método get
        request = self.factory.put(f'{endpoint}/1', data=data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupDetails.as_view()(
            request, group_id=1)

        response.render()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail":"Subscription group 1 not found."})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        user, _ = create_user()
        service = create_service(user)
        group = create_subscription_group(service)

        data = {
            "name": "Grupo de prueba",
            "service": service.id,
        }

        # Apuntamos el endpoint con el método get
        request = self.factory.put(f'{endpoint}/{group.id}', data=data, format="json")

        # Llamamos a la vista
        response = SubscriptionGroupDetails.as_view()(
            request, group_id=group.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )
    