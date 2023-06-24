from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.subscriptions import SubscriptionDetails
from api.tests.views.util import create_authenticated_user, create_service, create_subscription, create_conector
from rest_framework import status


endpoint = "/v1/subscriptions/"


class TestDeleteSubscriptions(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_subscriptions_delete_valid(self):
        '''Comprueba que se borra la suscripción correctamente'''

        request = self.factory.delete(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        conector = create_conector()
        service = create_service(user)
        subscription = create_subscription(service, conector)

        conector.save()
        service.save()
        subscription.save()

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(
            request, subscription_id=subscription.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"detail": "Suscripción eliminada."})

    def test_subscriptions_delete_forbidden(self):
        '''Comprueba que se lanza un error al intentar borrar una suscripción que no pertene al usuario'''

        request = self.factory.delete(endpoint)

        conector = create_conector()

        # Creamos otro usario con una suscripción
        other_user, other_token = create_authenticated_user()
        not_owner_service = create_service(other_user)

        other_subscription = create_subscription(not_owner_service, conector)

        conector.save()
        not_owner_service.save()
        other_subscription.save()

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Intentamos realizar un delete con el id que no poseemos
        response = SubscriptionDetails.as_view()(
            request, subscription_id=other_subscription.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": f"You do not have permission to perform this action."})

    def test_services_delete_null(self):
        '''Comprueba que se lanza un error al intentar borrar una suscripción que no existe'''

        request = self.factory.delete(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionDetails.as_view()(request, subscription_id=0)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"detail": f"Suscripción con id 0 no existe."})
