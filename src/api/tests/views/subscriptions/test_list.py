from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.subscription_views import SubscriptionsListApiView
from api.models import Service
from api.tests.views.util import create_authenticated_user, create_service, create_subscription, create_conector
from api.serializers import SubscriptionsSerializer

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
        response = SubscriptionsListApiView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_subscriptions_list_one(self):
        '''Comprueba que se devuelve sólo con la subscripcion asociada al servicio del usuario'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un conector
        conector = create_conector()
        conector.save()

        # Registramos un servicio por otro usuario
        other_user, other_token = create_authenticated_user()
        other_service = Service(
            name="other_user_service", owner=other_user)
        other_service.save()

        other_subscription = create_subscription(other_service, conector)
        other_subscription.save()

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()
        force_authenticate(request, user, token)

        # Creamos un servicio a nombre del usuario
        service = create_service(user)
        service.save()

        subscription = create_subscription(service, conector)
        subscription.save()

        # Llamamos a la vista
        response = SubscriptionsListApiView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0], SubscriptionsSerializer(subscription).data)

    def test_subscriptions_list_many(self):
        '''Comprueba que se devuelve una lista sólo con las subscripciones asociadas al servicio del usuario'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Creamos un conector para cada suscripción
        conector1 = create_conector()
        conector2 = create_conector()
        conector1.save()
        conector2.save()

       # Registramos un servicio por otro usuario
        other_user, other_token = create_authenticated_user()
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
        response = SubscriptionsListApiView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data[0], SubscriptionsSerializer(subscription1).data)
        self.assertEqual(
            response.data[1], SubscriptionsSerializer(subscription2).data)
