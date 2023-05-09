from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.subscription_views import SubscriptionsDetailsApiView
from rest_framework import status
from api.tests.views.util import create_service, create_authenticated_user, create_conector, create_subscription
from api.serializers import SubscriptionsSerializer

endpoint = "/v1/subscriptions"


class TestUpdateSubscriptions(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_subscriptions_update_valid(self):
        '''Comprueba que se actualiza la suscripción cuando se modifica el campo subscription_data'''

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_authenticated_user()

        conector = create_conector()
        service = create_service(user)
        subscription = create_subscription(service, conector)

        conector.save()
        service.save()
        subscription.save()

        data = {
            "subscription_data": {"NewKey": "NewValue"},
        }

        # Apuntamos el endpoint con el método put y el campo name actualizado
        request = self.factory.put(
            f'{endpoint}/{subscription.id}', data, format="json")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsDetailsApiView.as_view()(
            request, subscription_id=subscription.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"id": subscription.id, **data})

    def test_subscriptions_update_valid(self):
        '''Comprueba que no se actualiza si se intenta cambiar campos rad_only'''

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_authenticated_user()

        conector = create_conector()
        new_conector = create_conector()

        service = create_service(user)
        new_service = create_service(user)

        subscription = create_subscription(service, conector)

        conector.save()
        new_conector.save()
        service.save()
        new_service.save()
        subscription.save()

        data = {
            "service": new_service.id,
            "conector": new_conector.id,
            "subscription_data": {"NewKey": "NewValue"},
        }

        # Apuntamos el endpoint con el método put y el campo service_name actualizado
        request = self.factory.put(
            f'{endpoint}/{subscription.id}', data, format="json")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsDetailsApiView.as_view()(
            request, subscription_id=subscription.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"id": subscription.id, **data, "meta": {}})

    def test_services_update_empty(self):
        '''Comprueba que no se actualiza la suscripción cuando no se modifica ningún campo'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        conector = create_conector()
        service = create_service(user)
        subscription = create_subscription(service, conector)

        conector.save()
        service.save()
        subscription.save()

        # Apuntamos el endpoint con el método put y un cuerpo vacío
        request = self.factory.put(f'{endpoint}/{subscription.id}', data={})

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsDetailsApiView.as_view()(
            request, subscription_id=subscription.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, SubscriptionsSerializer(subscription).data)

    def test_subscriptions_update_not_owner(self):
        '''Comprueba que se lanza un error al intentar actualizar una suscripción que no pertene al usuario'''

        conector = create_conector()

        # Creamos otro usuario con un servicio
        other_user, other_token = create_authenticated_user()
        not_owned_service = create_service(other_user)

        not_owned_subscription = create_subscription(
            not_owned_service, conector)

        conector.save()
        not_owned_service.save()
        not_owned_subscription.save()

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        # Apuntamos el endpoint con el método put a una suscripción que no somos dueños
        request = self.factory.get(f'{endpoint}/{not_owned_subscription.id}', {
            "subscription_data": {"NewKey": "NewValue"},
        })

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsDetailsApiView.as_view()(
            request, subscription_id=not_owned_subscription.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"res": f"No tienes permisos."})
