from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services import ServiceDetails
from rest_framework import status
from api.tests.views.util import create_conector, create_service, create_user, create_subscription, create_subscription_group
from api.serializers import SubscriptionsSerializer
from api.views.subscription_groups import SubscriptionGroupDetails

endpoint = "/v1/groups"

class TestGetSubscriptionGroup(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_user_owner(self):
        '''Comprueba que se muestra id, servicio, metainformación, suscripciones del grupo y
         fecha de creación la suscripción cuando el usuario es el dueño.'''

        user, token = create_user()
        service = create_service(user)
        conector = create_conector()
        group = create_subscription_group(service)
        subscription1 = create_subscription(service, conector, group)
        subscription2 = create_subscription(service, conector, group)

        # Apuntamos el endpoint con el método get
        request = self.factory.get(f'{endpoint}/{group.id}')
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupDetails.as_view()(
            request, group_id=group.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({
            "id": group.id,
            "name": group.name,
            "service": service.id,
            "meta": group.meta,
            "subscriptions": SubscriptionsSerializer((subscription1, subscription2), many=True).data,
        }, response.data)
        self.assertIsNotNone(response.data["created_at"])
    
    
    def test_not_owner(self):
        '''Comprueba que se muestra error de permisos  cuando el usuario no es el dueño'''

        user, token = create_user()
        another_user, _ = create_user()
        service = create_service(another_user)
        group = create_subscription_group(service)

        # Apuntamos el endpoint con el método get
        request = self.factory.get(f'{endpoint}/{group.id}')
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupDetails.as_view()(
            request, group_id=group.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_non_exist(self):
        '''Comprueba que se indica que no se ha encontrado el grupo cuando no existe'''

        user, token = create_user()
        another_user, _ = create_user()
        service = create_service(another_user)
        group = create_subscription_group(service)

        # Apuntamos el endpoint con el método get
        request = self.factory.get(f'{endpoint}/{group.id + 1}')
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupDetails.as_view()(
            request, group_id=group.id + 1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"detail": f"Subscription group {group.id + 1} not found."})

    def test_not_authenticated(self):
        '''Comprueba que se muestran un error cuando el usuario no está autenticado'''

        user, _ = create_user()
        service = create_service(user)
        group = create_subscription_group(service)

        # Apuntamos el endpoint con el método get
        request = self.factory.get(f'{endpoint}/{group.id}')

        # Llamamos a la vista
        response = SubscriptionGroupDetails.as_view()(
            request, group_id=group.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )
    