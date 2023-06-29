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
        '''Comprueba que se actualiza el servicio excepto usuario y la fecha de creación
          cuando el usuario está autenticado,el servicio existe y es el dueño'''

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_user()
        other_user, _ = create_user()
        my_service = create_service(user)

        data = {
            "name": "newName",
            "owner": other_user.id,
            "created_at": "2021-01-01"
        }

        # Apuntamos el endpoint con el método put y el campo name actualizado
        request = self.factory.put(f'{endpoint}/{my_service.id}', data=data, format="json")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(
            request, service_id=my_service.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["owner"], user.id)
        self.assertNotEqual(response.data["created_at"], data["created_at"])
    
    def test_missing_all(self):
        '''Comprueba que no se actualiza ningún campo si no se introduce ningún campo'''

        user, token = create_user()
        service = create_service(user)

        data = {}

        # Apuntamos el endpoint con el método put y el campo name actualizado
        request = self.factory.put(f'{endpoint}/{service.id}', data=data, format="json")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ServiceDetails.as_view()(
            request, service_id=service.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data["name"], service.name)
        self.assertEqual(response.data["owner"], user.id)
        self.assertNotEqual(response.data["created_at"], service.created_at)

    def test_not_owner(self):
        '''Comprueba que se lanza un error cuando el servicio no pertene al usuario'''

        # Creamos otro usuario con un servicio
        other_user, _ = create_user()
        not_owned_service = create_service(other_user)

        # Creamos un nuevo usario autenticado con un servicio
        user, token = create_user()
        create_service(user)

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
        self.assertEqual(json.loads(response.content), {"detail": f"Service 1 not found."})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.put(f'{endpoint}/{1}')

        # Llamamos a la vista
        response = ServiceDetails.as_view()(request, service_id=1)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})