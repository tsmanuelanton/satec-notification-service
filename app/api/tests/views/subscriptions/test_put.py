import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.subscriptions import SubscriptionDetails
from rest_framework import status
from api.tests.views.util import create_service, create_authenticated_user, create_conector, create_subscription, create_subscription_group
from api.serializers import SubscriptionsSerializer
from api.models import Subscription

endpoint = "/v1/subscriptions"


class TestUpdateSubscriptions(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_valid(self):
        '''Comprueba que se registra la suscripción cuando el usuario es el propietario,
            servicio existe,conector existe, la suscripción es válida, y el grupo existe.'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        conector = create_conector()
        service = create_service(user)
        service2 = create_service(user)
        group1 = create_subscription_group(service)
        group2 = create_subscription_group(service2)
        subscription = create_subscription(service, conector, group1)


        conector.save()
        service.save()
        service2.save()
        group1.save()
        group2.save()
        subscription.save()

        # Cuerpo del PUT
        data = {
            "subscription_data": {"key": "Value"},
            "group": group2.id,
            "meta": {
                "user": "user1"
            }
        }

        # PUT  del data
        request = self.factory.put(f"{endpoint}/{subscription.id}", data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(request, subscription_id=subscription.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertDictContainsSubset({"subscription_data": {"key": "Value"},
            "group": group2.id,
            "meta": {
                "user": "user1"
            }}, response.data)
        
        self.assertEqual(response.data.get("created_at"), subscription.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_not_valid(self):
        '''Comprueba que se lanza un error mostrando los errores cuando el serializador encuentra errores'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        service = create_service(user)
        conector = create_conector()
        subscription = create_subscription(service, conector)

        service.save()
        conector.save()
        subscription.save()

        # Cuerpo del PUT
        data = {
            "service": service.id + 1,
            "conector": conector.id,
            "meta": {
                "user": "user1"
            }
        }

        # PUT  del data
        request = self.factory.put(f"{endpoint}/{subscription.id}", data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(request, subscription_id=subscription.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'service':  [f'Invalid pk \"{service.id + 1}\" - object does not exist.']})

        # Comprobamos que la suscripción no se ha actualizado
        updated_subscription = Subscription.objects.get(id=subscription.id)
        self.assertEqual(SubscriptionsSerializer(subscription).data, SubscriptionsSerializer(updated_subscription).data)
        
    def test_not_owner(self):
        '''Comprueba que se lanza un error cuando el usuario no es el dueño de la suscripción'''

        user, token = create_authenticated_user()
        other_user, _ = create_authenticated_user()
        service_not_owned = create_service(other_user)
        conector = create_conector()
        subscription_not_owned = create_subscription(service_not_owned, conector)

        service_not_owned.save()
        conector.save()
        subscription_not_owned.save()

        # Apuntamos el endpoint con el método put
        request = self.factory.put(f"{endpoint}/{subscription_not_owned}")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(request, subscription_id=subscription_not_owned.id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"You do not have permission to perform this action."})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método put
        request = self.factory.put(f"{endpoint}/{1}")

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})
