# from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
# from api.tests.views.util import create_authenticated_user
# from rest_framework import status
# from rest_framework.serializers import ErrorDetail
# from api.models import Conector
# from api.serializers import ConectorsSerializer
# from api.views.conectors_views import ConectorsListApiView

# endpoint = "/v1/conectors/"


# class TestPostConectors(APITestCase):

#     def setUp(self) -> None:
#         self.factory = APIRequestFactory()

#     def test_conector_post_valid(self):
#         '''Comprueba que se guarda el conector correctamente'''

#         # Cuerpo del POST
#         data = {
#             "name": "Conector0",
#             "description": "Description conector 0",
#             "meta": {"Key": "ABC123"}
#         }

#         # POST  del data
#         request = self.factory.post(endpoint, data, format='json')

#         # Creamos un nuevo usario autenticado
#         user, token = create_authenticated_user()
#         force_authenticate(request, user, token)

#         # Indicamos que el usuario es superusuario
#         user.is_superuser = True

#         # Llamamos a la vista
#         response = ConectorsListApiView.as_view()(request)

#         # Obtenermos el servicio creado (el único por eso get())
#         conector_saved = Conector.objects.get()

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(
#             response.data, ConectorsSerializer(conector_saved).data)

#     def test_conector_post_valid_empty_meta(self):
#         '''Comprueba que se guarda correctamente el conector con el campo meta vacío'''

#         # Cuerpo del POST
#         data = {
#             "name": "Conector1",
#             "description": "Description conector 1",
#             "meta": {}
#         }

#         # POST  del data
#         request = self.factory.post(endpoint, data, format='json')

#         # Creamos un nuevo usario autenticado
#         user, token = create_authenticated_user()
#         force_authenticate(request, user, token)

#         # Indicamos que el usuario es superusuario
#         user.is_superuser = True

#         # Llamamos a la vista
#         response = ConectorsListApiView.as_view()(request)

#         # Obtenermos el servicio creado (el único por eso get())
#         conector_saved = Conector.objects.get()

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(
#             response.data, ConectorsSerializer(conector_saved).data)

#     def test_conector_post_fobbiden_staff(self):
#         '''Comprueba que se lanza un error 403 si el usario es staff '''

#         # Cuerpo del POST
#         data = {
#             "name": "Conector01",
#             "description": "Description conector 01",
#             "meta": {"Key": "ABC123"}
#         }

#         # POST  del data
#         request = self.factory.post(endpoint, data, format='json')

#         # Creamos un nuevo usario autenticado
#         user, token = create_authenticated_user()
#         force_authenticate(request, user, token)

#         # Indicamos que el usuario es staff
#         user.is_staff = True

#         # Llamamos a la vista
#         response = ConectorsListApiView.as_view()(request)

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(
#             response.data, {'res': "Permisos insuficientes"})

#     def test_conector_post_forbidden(self):
#         '''Comprueba que se lanza un error 403 si el usario no es un superusuario'''

#         # Cuerpo del POST
#         data = {
#             "name": "Conector2",
#             "description": "Description conector 2",
#             "meta": {}
#         }

#         # POST  del data
#         request = self.factory.post(endpoint, data, format='json')

#         # Creamos un nuevo usario autenticado
#         user, token = create_authenticated_user()
#         force_authenticate(request, user, token)

#         # Llamamos a la vista
#         response = ConectorsListApiView.as_view()(request)

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(
#             response.data, {'res': "Permisos insuficientes"})

#     def test_conectors_post_missing_all(self):
#         '''Comprueba que se lanza un error cuando faltan todos los campos'''

#         # Cuerpo del POST vacío
#         data = {}

#         # POST  del data
#         request = self.factory.post(endpoint, data, format='json')

#         # Creamos un nuevo usario autenticado
#         user, token = create_authenticated_user()
#         force_authenticate(request, user, token)

#         # Indicamos que el usuario es superusuario
#         user.is_superuser = True

#         # Llamamos a la vista
#         response = ConectorsListApiView.as_view()(request)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             response.data, {
#                 'name': [ErrorDetail(string='This field may not be null.', code='null')],
#                 'description': [ErrorDetail(string='This field may not be null.', code='null')],
#                 'meta': [ErrorDetail(string='This field may not be null.', code='null')]
#             })

#     def test_conectors_post_missing_name(self):
#         '''Comprueba que se lanza un error cuando falta el nombre'''

#         # Cuerpo del POST sin name
#         data = {
#             "description": "Description conector 3",
#             "meta": {}
#         }

#         # POST  del data
#         request = self.factory.post(endpoint, data, format='json')

#         # Creamos un nuevo usario autenticado
#         user, token = create_authenticated_user()
#         force_authenticate(request, user, token)

#         # Indicamos que el usuario es superusuario
#         user.is_superuser = True

#         # Llamamos a la vista
#         response = ConectorsListApiView.as_view()(request)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             response.data, {'name': [ErrorDetail(string='This field may not be null.', code='null')]})

#     def test_conectors_post_missing_description(self):
#         '''Comprueba que se lanza un error cuando falta el nombre'''

#         # Cuerpo del POST sin name
#         data = {
#             "name": "Conector4",
#             "meta": {}
#         }

#         # POST  del data
#         request = self.factory.post(endpoint, data, format='json')

#         # Creamos un nuevo usario autenticado
#         user, token = create_authenticated_user()
#         force_authenticate(request, user, token)

#         # Indicamos que el usuario es superusuario
#         user.is_superuser = True

#         # Llamamos a la vista
#         response = ConectorsListApiView.as_view()(request)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             response.data, {'description': [ErrorDetail(string='This field may not be null.', code='null')]})

#     def test_conectors_post_missing_meta(self):
#         '''Comprueba que se lanza un error cuando falta el nombre'''

#         # Cuerpo del POST sin name
#         data = {
#             "name": "Conector5",
#             "description": "Description 5"
#         }

#         # POST  del data
#         request = self.factory.post(endpoint, data, format='json')

#         # Creamos un nuevo usario autenticado
#         user, token = create_authenticated_user()
#         force_authenticate(request, user, token)

#         # Indicamos que el usuario es superusuario
#         user.is_superuser = True

#         # Llamamos a la vista
#         response = ConectorsListApiView.as_view()(request)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             response.data, {'meta': [ErrorDetail(string='This field may not be null.', code='null')]})
