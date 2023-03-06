from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.conectors_views import ConectorsDetailsApiView
from rest_framework import status
from api.tests.views.util import create_authenticated_user
from api.serializers import ConectorsSerializer
from api.models import Conector

endpoint = "/v1/conectors"


class TestDetailsConectors(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_conectors_details_null(self):
        '''Comprueba que se lanza un error cuando no existe el conector con el id'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint + "/1")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ConectorsDetailsApiView.as_view()(request, conector_id=1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"res": f"Conector con id 1 no existe."})

    def test_conectors_details_valid(self):
        '''Comprueba que se muestran los datos cuando el conector existe'''

        # Creamos un nuevo usario autenticado
        user, token = create_authenticated_user()

        conector = Conector(
            name="Conector1", description="Conector prueba 2", meta={"Key": "Value"})
        conector.save()

        # Apuntamos el endpoint con el método get
        request = self.factory.get(f'{endpoint}/{conector.id}')

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ConectorsDetailsApiView.as_view()(
            request, conector_id=conector.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,  ConectorsSerializer(conector).data)
