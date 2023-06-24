import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.subscriptions import SubscriptionsList
from api.models import Service
from api.tests.views.util import create_authenticated_user, create_service, create_subscription, create_conector
from api.serializers import SubscriptionsSerializer
from rest_framework import status

endpoint = "/v1/subscriptions/"


class TestListSubscriptions(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_subscriptions_list_empty(self):
        '''Comprueba que se devuelve una lista vacía si no hay subscripciones'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_not_owned(self):
        '''Comprueba que no se devuelven subscripciones de otros usuarios'''

        other_user, _ = create_authenticated_user()
        conector = create_conector()
        service_not_owned = create_service(other_user)
        subscription_not_owned = create_subscription(service_not_owned, conector)
        
        conector.save()
        service_not_owned.save()
        subscription_not_owned.save()

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_owned_and_not_owned(self):
        '''Comprueba que se devuelve una lista sólo con las subscripciones asociadas al servicio del usuario'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un conector para cada suscripción
        conector1 = create_conector()
        conector2 = create_conector()
        conector1.save()
        conector2.save()

       # Registramos un servicio por otro usuario
        other_user, _ = create_authenticated_user()
        other_service = Service(
            name="other_user_service", owner=other_user)
        other_service.save()

        other_subscription = create_subscription(other_service, conector1)
        other_subscription.save()

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Creamos un servicio a nombre del usuario
        service = create_service(user)
        service.save()

        # Creamos dos nuevas suscripciones para cada servicio
        subscription1 = create_subscription(service, conector1)
        subscription2 = create_subscription(service, conector2)
        subscription1.save()
        subscription2.save()

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data[0], SubscriptionsSerializer(subscription1).data)
        self.assertEqual(
            response.data[1], SubscriptionsSerializer(subscription2).data)

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Llamamos a la vista
        response = SubscriptionsList.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})
