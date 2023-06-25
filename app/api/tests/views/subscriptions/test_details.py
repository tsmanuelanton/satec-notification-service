import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.subscriptions import SubscriptionDetails
from api.tests.views.util import create_user, create_service, create_subscription, create_conector
from api.serializers import SubscriptionsSerializer
from rest_framework import status

endpoint = "/v1/subscriptions"

class TestDetailsSubscriptions(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_user_is_owner(self):
        '''Comprueba que se muestran los datos cuando el servicio pertenece al usuario'''

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_user()

        conector = create_conector()
        service = create_service(user)
        subscription = create_subscription(service, conector)

        # Apuntamos el endpoint con el método get
        request = self.factory.get(f'{endpoint}/{subscription.id}')

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(
            request, subscription_id=subscription.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, SubscriptionsSerializer(subscription).data)

    def test_not_owner(self):
        '''Comprueba que se lanza un error cuando la suscripción no pertene al usuario'''

        # Creamos otro usuario una suscipción asociada
        other_user, _ = create_user()
        conector = create_conector()
        not_owned_service = create_service(other_user)
        other_subscription = create_subscription(not_owned_service, conector)

        request = self.factory.get(f'{endpoint}/{other_subscription.id}')

        # Creamos un nuevo usario autenticado
        user, token = create_user()

        force_authenticate(request, user, token)

        # Llamamos a la vista con la suscripción que no nos pertenece
        response = SubscriptionDetails.as_view()(
            request, subscription_id=other_subscription.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": f"You do not have permission to perform this action."})

    def test_not_exists(self):
        '''Comprueba que se lanza un error cuando no existe la suscripción'''

        # Creamos un nuevo usario autenticado
        user, token = create_user()

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint + "/1")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(request, subscription_id=1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"detail": f"Suscripción con id 1 no existe."})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint + "/1")

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})
