import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework import status
from api.tests.views.util import create_conector, create_service, create_user, create_subscription, create_subscription_group
from api.views.subscription_groups import SubscriptionGroupsList
from api.models import SubscriptionGroup

endpoint = "/v1/groups"

class TestPostSubscriptionGroup(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
    
    def test_owned_service(self):
        '''Comprueba que se crea y muestra un nuevo grupo de suscripciones registrado
          a nombre del usuario si el usuario es el dueño del servicio'''
        user, token = create_user()
        service = create_service(user)

        data = {"name": "conectorNuevo", "service": service.id, "meta": {"key": "value"}}
        
        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint, data=data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(data, response.data)
        self.assertIsNotNone(response.data["created_at"])
    
    def test_service_not_owned(self):
        '''Comprueba que se lanza un error si el usuario no es el dueño del servicio'''
        user, token = create_user()
        other_user, token = create_user()
        service = create_service(other_user)

        data = {"name": "conectorNuevo", "service": service.id, "meta": {"key": "value"}}
        
        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint, data=data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"service": ["El servicio no existe o no pertenece al usuario"]})

    def test_service_no_exists(self):
        '''Comprueba que se lanza un error cuando el usuario está autenticado y no existe el servicio'''

        user, token = create_user()
        service = create_service(user)
        conector = create_conector()
        create_subscription(service, conector)

        data = {
            "name": "Grupo de prueba",
            "service": service.id + 1,
            "meta": {
                "field": "value"
            }
        }

        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint, data=data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"service":[f"Invalid pk \"{service.id + 1}\" - object does not exist."]})


    def test_missing_service(self):
        '''Comprueba que se lanza un error cuando falta el servicio en la petición'''

        user, token = create_user()

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

    def test_missing_name(self):
        '''Comprueba que se lanza un error indicando que falta el nombre'''
        user, token = create_user()

        service = create_service(user)

        data = {"service": service.id, "meta": {"key": "value"}}
        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint, data=data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"name": ["This field is required."]})


    def test_missing_meta(self):
        '''Comprueba que se crea un grupo correctamente si no se especifica el meta'''
        user, token = create_user()
        service = create_service(user)

        data = {"name": "conectorNuevo", "service": service.id}
        # Apuntamos el endpoint con el método get
        request = self.factory.post(endpoint, data=data, format="json")
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset({
            "name": "conectorNuevo",
            "service": service.id,
            "meta": {}
        }, response.data)

    def test_missing_all(self):
        '''Comprueba que se lanza un error indicando que faltan los campos nombre y servicio'''

        user, token = create_user()
        service = create_service(user)

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

        user, _ = create_user()
        service = create_service(user)

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
    