# from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
# from api.tests.views.util import create_authenticated_user
# from api.views.conectors_views import ConectorsDetailsApiView
# from api.models import Conector
# from rest_framework import status

# endpoint = "/v1/conectors/"


# class TestDeleteConectors(APITestCase):

#     def setUp(self) -> None:
#         self.factory = APIRequestFactory()

#     def test_conectors_delete_valid(self):
#         '''Comprueba que se borra el conector correctamente'''

#         request = self.factory.delete(endpoint)

#         # Creamos un nuevo usario autenticado
#         user, token = create_authenticated_user()
#         force_authenticate(request, user, token)

#         # Indicamos que el usuario es superusuario
#         user.is_superuser = True

#         conector = Conector(
#             name="Conector1", description="Conector prueba 2", meta={"Key": "Value"})
#         conector.save()

#         # Llamamos a la vista
#         response = ConectorsDetailsApiView.as_view()(request, conector_id=conector.id)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(
#             response.data, {"res": "Conector 1 eliminado"})

#     def test_conectors_delete_forbidden(self):
#         '''Comprueba que se lanza un error al intentar borrar un conector sin ser superuser'''

#         request = self.factory.delete(endpoint)

#         # Creamos otro usario con un servicio
#         user, token = create_authenticated_user()
#         force_authenticate(request, user, token)

#         conector = Conector(
#             name="Conector1", description="Conector prueba 2", meta={"Key": "Value"})
#         conector.save()

#         # Intentamos realizar un delete
#         response = ConectorsDetailsApiView.as_view()(request, conector_id=conector.id)

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(
#             response.data, {"res": f"Permisos insuficientes"})

#     def test_conectors_delete_null(self):
#         '''Comprueba que se lanza un error al intentar borrar un conector que no existe'''

#         request = self.factory.delete(endpoint)

#         # Creamos un nuevo usario autenticado
#         user, token = create_authenticated_user()
#         force_authenticate(request, user, token)

#         # Indicamos que el usuario es superusuario
#         user.is_superuser = True

#         # Llamamos a la vista con el id del conector que no existe
#         response = ConectorsDetailsApiView.as_view()(request, conector_id=1)

#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(
#             response.data, {"res": f"Conector con id 1 no existe"})
