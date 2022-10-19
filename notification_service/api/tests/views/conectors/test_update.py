from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework import status
from api.tests.views.util import create_conector, create_authenticated_user
from api.views.conectors_views import ConectorsDetailsApiView
from api.serializers import ConectorsSerializer


endpoint = "/v1/services"


class TestUpdateServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_conectors_update_valid(self):
        '''Comprueba que se actualiza el conector cuando se pasan todos los campos'''

        # Creamos un nuevo superusuario
        user, token = create_authenticated_user()
        user.is_superuser = True

        # Creamos el servicio a actualizar
        conector = create_conector()
        conector.save()

        updated_fields = {
            "name": "Conector1",
            "description": "Conector prueba 2",
            "meta": {"Key": "Value"},
        }

        # Apuntamos el endpoint  con el método put
        request = self.factory.put(
            f'{endpoint}/{conector.id}', data=updated_fields, format="json")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ConectorsDetailsApiView.as_view()(request, conector_id=conector.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": conector.id, **updated_fields})

    def test_conectors_update_forbidden(self):
        '''Comprueba que se lanza un error al intentar actulizar un conecor sin ser superuser'''

        # Creamos un nuevo superusuario
        user, token = create_authenticated_user()

        # Creamos el servicio a actualizar
        conector = create_conector()
        conector.save()

        updated_fields = {
            "name": "Conector1",
            "description": "Conector prueba 2",
            "meta": {"Key": "Value"},
        }

        # Apuntamos el endpoint  con el método put
        request = self.factory.put(
            f'{endpoint}/{conector.id}', data=updated_fields, format="json")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ConectorsDetailsApiView.as_view()(request, conector_id=conector.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"res": "Permisos insuficientes"})

    def test_conectors_update_empty(self):
        '''Comprueba que no se actualiza ningún campo del conector al enviar un json vacío'''

        # Creamos un nuevo superusuario
        user, token = create_authenticated_user()
        user.is_superuser = True

        # Creamos el servicio a actualizar
        conector = create_conector()
        conector.save()

        # Apuntamos el endpoint con el método put y un cuerpo vacío
        request = self.factory.put(f'{endpoint}/{conector.id}', data={})

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ConectorsDetailsApiView.as_view()(request, conector_id=conector.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, ConectorsSerializer(conector).data)

    def test_conectors_update_partial(self):
        '''Comprueba que se acrtualiza correctamente el conector cuando se pasan los campos de forma parcial'''

        # Creamos un nuevo superusuario
        user, token = create_authenticated_user()
        user.is_superuser = True

        fields_to_update = [
            {"name": "new Name"},
            {"description": "new Description"},
            {"meta": {"Key": "new Meta"}},
        ]

        for field_to_update in fields_to_update:
            conector = create_conector()
            conector.save()

            # Mandamos actualizar el campo del conector actual
            request = self.factory.put(
                f'{endpoint}/{conector.id}', data=field_to_update, format="json")

            force_authenticate(request, user, token)

            # Llamamos a la vista
            response = ConectorsDetailsApiView.as_view()(request, conector_id=conector.id)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response.data,
                {**ConectorsSerializer(conector).data, **field_to_update})
