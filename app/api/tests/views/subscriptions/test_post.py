from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.subscription_views import SubscriptionsListApiView
from api.tests.views.util import create_authenticated_user
from rest_framework import status
from rest_framework.serializers import ErrorDetail

from api.models import Subscription
from api.tests.views.util import create_conector, create_service

endpoint = "/v1/subscriptions"


class TestPostSubscriptions(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_subscriptions_post_valid(self):
        '''Comprueba que se registra la suscripción cuando se pasan todos los datos'''

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
        response = SubscriptionsListApiView.as_view()(request)

        # Obtenermos el servicio creado (el único por eso get())
        subscription_saved = Subscription.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Comprobamos que indica el error
        self.assertEqual(
            response.data, {"id": subscription_saved.id, **data})

    def test_subscriptions_post_invalid_service(self):
        '''Comprueba que se lanza un error si el servicio no existe'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        conector = create_conector()

        conector.save()

        # Cuerpo del POST
        data = {
            "service": 1,
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
        response = SubscriptionsListApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Comprobamos que indica el error
        self.assertEqual(
            response.data, {'service': [ErrorDetail(string='Unknown service', code='does_not_exist')]})

    def test_subscriptions_post_invalid_connector(self):
        '''Comprueba que se lanza un error si el conector no existe'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        service = create_service(user)
        service.save()

        # Cuerpo del POST
        data = {
            "service": service.id,
            "conector": 1,
            "subscription_data": {"key": "Value"},
            "meta": {
                "user": "user1"
            }
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsListApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Comprobamos que indica el error
        self.assertEqual(
            response.data, {'conector': [ErrorDetail(string='Unknown conector', code='does_not_exist')]})

    def test_subscriptions_post_missing_service(self):
        '''Comrpueba que se lanza un error si falta el servicio al registrar la suscripción'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        conector = create_conector()

        conector.save()

        # Cuerpo del POST
        data = {
            "conector": conector.id,
            "subscription_data": {"key": "Value"},
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsListApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Comprobamos que indica el error
        self.assertEqual(
            response.data, {'service': [ErrorDetail(string='This field is required.', code='required')]})

    def test_subscriptions_post_missing_conector(self):
        '''Comrpueba que se lanza un error si falta el conector al registrar la suscripción'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        service = create_service(user)
        service.save()

        # Cuerpo del POST
        data = {
            "service": service.id,
            "subscription_data": {"key": "Value"},
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsListApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Comprobamos que indica el error
        self.assertEqual(
            response.data, {'conector': [ErrorDetail(string='This field is required.', code='required')]})

    def test_subscriptions_post_missing_subscription_data(self):
        '''Comrpueba que se lanza un error si falta el campo suscription_data al registrar la suscripción'''

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
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionsListApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Comprobamos que indica el error
        self.assertEqual(
            response.data, {'subscription_data': [ErrorDetail(string='This field is required.', code='required')]})
