import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework import status
from api.tests.views.util import create_conector, create_service, create_authenticated_user, create_subscription, create_subscription_group
from api.views.subscription_groups import SubscriptionGroupsList
from api.models import SubscriptionGroup

endpoint = "/v1/groups"

class TestPostSubscriptionGroup(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_authenticated_service_exists(self):
        '''Comprueba que se crea el grupo cuando el usuario está autenticado y existe el servicio'''

        user, token = create_authenticated_user()
        service = create_service(user)
        conector = create_conector()
        subscription= create_subscription(service, conector)
        group = create_subscription_group(service)
        subscription_in_group = create_subscription(service, conector, group)

        service.save()
        conector.save()
        subscription.save()
        group.save()
        subscription_in_group.save()

        new_group = {
            "name": "Grupo de prueba",
            "service": service.id,
        }

        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint, data=new_group, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], new_group["name"])
        self.assertEqual(response.data["service"], service.id)
    
    def test_authenticated_service_no_exists(self):
        '''Comprueba que se lanza un error cuando el usuario está autenticado y no existe el servicio'''

        user, token = create_authenticated_user()
        service = create_service(user)
        conector = create_conector()
        subscription= create_subscription(service, conector)
        group = create_subscription_group(service)

        service.save()
        conector.save()
        subscription.save()
        group.save()

        new_group = {
            "name": "Grupo de prueba",
            "service": service.id + 1,
            "meta": {
                "field": "value"
            }
        }

        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint, data=new_group, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SubscriptionGroup.objects.all().count(), 1)
        self.assertEqual(json.loads(response.content), {"service":[f"Invalid pk \"{service.id + 1}\" - object does not exist."]})
        self.assertTrue(response.data.get("created_at", False), "missing created_at")


    def test_authenticated_missing_service(self):
        '''Comprueba que se lanza un error cuando falta el servicio en la petición'''

        user, token = create_authenticated_user()

        new_group = {
            "name": "Grupo de prueba",
            "meta": {
                "field": "value"
            }
        }

        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint, data=new_group, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"service": ["This field is required."]})

    def test_authenticated_missing_name_and_optionals(self):
        '''Comprueba que se lanza un error cuando falta el campo nombre y otros opcionales'''

        user, token = create_authenticated_user()
        service = create_service(user)
        service.save()

        new_group = {
            "service": service.id,
        }

        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint, data=new_group, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"name": ["This field is required."]})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        user, _ = create_authenticated_user()
        service = create_service(user)
        service.save()

        group = {
            "name": "Grupo de prueba",
            "service": service.id,
        }

        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint, data=group, format="json")

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )
    