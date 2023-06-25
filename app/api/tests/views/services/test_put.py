import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services import ServiceDetails
from rest_framework import status
from api.tests.views.util import create_service, create_user
from api.serializers import ServicesSerializer

endpoint = "/v1/services"


class TestUpdateServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_valid(self):
        '''Comprueba que se actualiza el servicio cuando el usuario está autenticado, es el dueño y no hay errores'''

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_user()
        my_service = create_service(user)
        my_service.save()

        data = {
            "name": "name"
        }

        # Apuntamos el endpoint con el método put y el campo name actualizado
        request = self.factory.put(f'{endpoint}/{my_service.id}', data=data)

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(
            request, service_id=my_service.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data.get("created_at"), my_service.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        

    def test_invalid(self):
        '''Comprueba que se lanza un error cuando el usuario está autenticado, es el dueño y hay errores'''

        # Creamos un nuevo usario autenticado
        user, token = create_user()

        # Creamos el servicio a actualizar
        service = create_service(user)
        service.save()

        data = {
            "owner": -1
        }

        # Apuntamos el endpoint con el método put y un cuerpo vacío
        request = self.factory.put(f'{endpoint}/{service.id}', data=data)
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(request, service_id=service.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),{'owner': ['Invalid pk "-1" - object does not exist.']})

    def test_not_owner(self):
        '''Comprueba que se lanza un error cuando el servicio no pertene al usuario'''

        # Creamos otro usuario con un servicio
        other_user, other_token = create_user()
        not_owned_service = create_service(other_user)
        not_owned_service.save()

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_user()
        my_service = create_service(user)
        my_service.save()

        data = {
            "name": "name"
        }

        # Apuntamos el endpoint con el método put a un servicio que no somos dueños
        request = self.factory.put(f'{endpoint}/{not_owned_service.id}', data=data)

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(
            request, service_id=not_owned_service.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": f"You do not have permission to perform this action."})

    def test_not_exist(self):
        '''Comprueba que se lanza un error cuando el servicio no existe'''
        user, token = create_user()

        # Apuntamos el endpoint con el método get
        request = self.factory.put(f'{endpoint}/{1}')
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(request, service_id=1)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": f"Servicio con id 1 no existe."})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.put(f'{endpoint}/{1}')

        # Llamamos a la vista
        response = ServiceDetails.as_view()(request, service_id=1)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})