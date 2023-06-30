import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services import ServiceDetails
from api.tests.views.util import create_conector, create_subscription, create_subscription_group, create_user, create_service
from rest_framework import status

from api.models import Subscription, SubscriptionGroup

endpoint = "/v1/services/"


class TestDeleteServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_user_is_owner(self):
        '''Comprueba que cuando el usuario es el dueño, se elimina el servicio junto
          con las sucripciones y grupos de este servicio '''

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_user()
        service1 = create_service(user)
        service2 = create_service(user)
        conector = create_conector()
        group = create_subscription_group(service1)
        subscription1 = create_subscription(service1, conector, group)
        subscription2 = create_subscription(service1, conector, group)
        subscription3 = create_subscription(service2, conector)


        # Apuntamos el endpoint con el método get
        request = self.factory.delete(f'{endpoint}/{service1.id}')

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(
            request, service_id=service1.id)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {"detail": f"Resource {service1.id} deleted successfully."})

        # Comprobamos que se ha eliminado el servicio y los grupos y servicios
        self.assertIsNone(Subscription.objects.filter(id=subscription1.id).first())
        self.assertIsNone(Subscription.objects.filter(id=subscription2.id).first())
        self.assertIsNone(SubscriptionGroup.objects.filter(id=group.id).first())

        # Comprobamos que no se ha eliminado la suscripción del otro servicio
        self.assertIsNotNone(Subscription.objects.get(id=subscription3.id))

    def test_not_owner(self):
        '''Comprueba que se lanza un error cuando el servicio no pertene al usuario'''

        # Creamos otro usuario con un servicio
        other_user, _ = create_user()
        not_owned_service = create_service(other_user)

        request = self.factory.delete(f'{endpoint}/{not_owned_service.id}')

        # Creamos un nuevo usario autenticado
        user, token = create_user()
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(
            request, service_id=not_owned_service.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": f"You do not have permission to perform this action."})
        
    
    def test_service_not_exist(self):
        '''Comprueba que se lanza un error cuando no existe el servicio'''

        # Creamos un nuevo usario autenticado
        user, token = create_user()

        # Apuntamos el endpoint con el método get
        request = self.factory.delete(endpoint + "/1")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(request, service_id=1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"detail": f"Service 1 not found."})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método delete
        request = self.factory.delete(endpoint + "/1")

        # Llamamos a la vista
        response = ServiceDetails.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})