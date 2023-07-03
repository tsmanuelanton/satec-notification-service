import asyncio
import json
from rest_framework.test import APIRequestFactory, force_authenticate, APITransactionTestCase
from api.views.notifications import NotificationDetails
from api.tests.views.util import ConectorForTest, ConectorForTestB, create_user, create_conector, create_service, create_subscription, create_subscription_group
from rest_framework import status
from unittest import mock
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

endpoint = "/api/v1/conectors"

class TestPostNotifications(APITransactionTestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_restricted_one_group(self):
        '''Comprueba que se envían las notificaciones a un grupo concreto'''

        # Creamos un nuevo usario
        user, token = create_user()

        conector = create_conector(ConectorForTest.name)
        service = create_service(user)

        # subscription out group
        create_subscription(service, conector)

        group1 = create_subscription_group(service)
        subscription_in_group1 = create_subscription(service, conector, group1)
        subscription2_in_group1 = create_subscription(
            service, conector, group1)

        group2 = create_subscription_group(service)
        # subscription in group 2
        create_subscription(service, conector, group2)

        # Cuerpo del POST sin el campo message
        data = {
            "service": service.id,
            "message": {
                "title": "TestTitle",
                "body": "TestBody"
            },
            "restricted_to_groups": [group1.id]
        }

        # Mockeamos el import de los conectores para que solo se cargue el conector de test
        with mock.patch("api.util.import_conectors") as mock_import_conectors:
            mock_import_conectors.return_value = [ConectorForTest]

            # POST  del data
            request = self.factory.post(endpoint, data, format="json")
            force_authenticate(request, user, token)

            # # Llamamos a la vista
            response = asyncio.run(NotificationDetails.as_view()(request))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data["successful"]), 2)
            self.assertCountEqual(response.data["successful"],
                                  [{'subscription_id': subscription_in_group1.id,
                                    'conector_name': 'ConectorForTest'},
                                   {'subscription_id': subscription2_in_group1.id,
                                    'conector_name': 'ConectorForTest'}])

    def test_restricted_two_group(self):
        '''Comprueba que se envían las notificaciones a un grupo concreto'''
        # Creamos un nuevo usario
        user, token = create_user()

        conector = create_conector(ConectorForTest.name)
        service = create_service(user)
        # subscription out group
        create_subscription(service, conector)

        group1 = create_subscription_group(service)
        subscription_in_group1 = create_subscription(service, conector, group1)
        subscription2_in_group1 = create_subscription(
            service, conector, group1)

        group2 = create_subscription_group(service)
        subscription_in_group2 = create_subscription(service, conector, group2)

        # Cuerpo del POST sin el campo message
        data = {
            "service": service.id,
            "message": {
                "title": "TestTitle",
                "body": "TestBody"
            },
            "restricted_to_groups": [group1.id, group2.id]
        }

        # Mockeamos el import de los conectores para que solo se cargue el conector de test
        with mock.patch("api.util.import_conectors") as mock_import_conectors:
            mock_import_conectors.return_value = [ConectorForTest]

            # POST  del data
            request = self.factory.post(endpoint, data, format="json")
            force_authenticate(request, user, token)

            # # Llamamos a la vista
            response = asyncio.run(NotificationDetails.as_view()(request))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data["successful"]), 3)
            self.assertCountEqual(response.data["successful"],
                                  [{'subscription_id': subscription_in_group1.id,
                                    'conector_name': 'ConectorForTest'},
                                   {'subscription_id':  subscription2_in_group1.id,
                                    'conector_name': 'ConectorForTest'},
                                   {'subscription_id':  subscription_in_group2.id,
                                    'conector_name': 'ConectorForTest'}])

    def test_restricted_invalid_group(self):
        '''Comprueba que se envían las notificaciones a un grupo concreto'''
        # Creamos un nuevo usario
        user, token = create_user()

        conector = create_conector(ConectorForTest.name)
        service = create_service(user)
        other_service = create_service(user)

        group_of_other_service = create_subscription_group(other_service)
        # subscription_in_group1
        create_subscription(service, conector, group_of_other_service)

        # Cuerpo del POST sin el campo message
        data = {
            "service": service.id,
            "message": {
                "title": "TestTitle",
                "body": "TestBody"
            },
            "restricted_to_groups": [group_of_other_service.id]
        }

        # Mockeamos el import de los conectores para que solo se cargue el conector de test
        with mock.patch("api.util.import_conectors") as mock_import_conectors:
            mock_import_conectors.return_value = [ConectorForTest]

            # POST  del data
            request = self.factory.post(endpoint, data, format="json")
            force_authenticate(request, user, token)

            # # Llamamos a la vista
            response = asyncio.run(NotificationDetails.as_view()(request))
            response.render()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(json.loads(response.content), {"restricted_to_groups": [
                             f"El grupo con {group_of_other_service.id} no existe"]})

    def test__not_restricted(self):
        '''Comprueba que se envían las notificaciones  a todos los suscriptores del servicio'''

        # Creamos un nuevo usario
        user, token = create_user()

        conector = create_conector(ConectorForTest.name)
        service = create_service(user)

        subscription_out_group = create_subscription(service, conector)

        group1 = create_subscription_group(service)
        subscription_in_group1 = create_subscription(service, conector, group1)
        subscription2_in_group1 = create_subscription(
            service, conector, group1)

        # Cuerpo del POST sin el campo message
        data = {
            "service": service.id,
            "message": {
                "title": "TestTitle",
                "body": "TestBody"
            },
        }

        # Mockeamos el import de los conectores para que solo se cargue el conector de test
        with mock.patch("api.util.import_conectors") as mock_import_conectors:
            mock_import_conectors.return_value = [ConectorForTest]

            # POST  del data
            request = self.factory.post(endpoint, data, format="json")
            force_authenticate(request, user, token)

            # # Llamamos a la vista
            response = asyncio.run(NotificationDetails.as_view()(request))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data["successful"]), 3)
            self.assertCountEqual(response.data["successful"],
                                  [{'subscription_id': subscription_out_group.id,
                                    'conector_name': 'ConectorForTest'},
                                   {'subscription_id': subscription_in_group1.id,
                                    'conector_name': 'ConectorForTest'},
                                   {'subscription_id': subscription2_in_group1.id,
                                    'conector_name': 'ConectorForTest'}])

    def test_notification_fails(self):
        '''Comprueba que se muestra un error si el servicio no pertenece al usuario autenticado'''

        # Creamos un nuevo usario
        user, token = create_user()
        other_user, _ = create_user()

        service = create_service(other_user)

        # Cuerpo del POST sin el campo message
        data = {
            "service": service.id,
            "message": {
                "title": "TestTitle",
                "body": "TestBody"
            },
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # # Llamamos a la vista
        response = asyncio.run(NotificationDetails.as_view()(request))
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {
                         "detail": "You do not have permission to perform this action."})

    def test_serializer_fails(self):
        '''Comprueba que se muestra un error si falta un campo requerido'''

        # Creamos un nuevo usario
        user, token = create_user()
        other_user, _ = create_user()

        service = create_service(other_user)

        # Cuerpo del POST sin el campo message
        data = {
            "service": service.id,
            "message": {
                "body": "TestBody"
            },
        }

        # POST  del data
        request = self.factory.post(endpoint, data, format="json")
        force_authenticate(request, user, token)

        # # Llamamos a la vista
        response = asyncio.run(NotificationDetails.as_view()(request))
        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {
                         'message': {'title': ['This field is required.']}})

    def test_notification_fails(self):
        '''Comprueba que se muestran información del envío si este falla'''

        # Creamos un nuevo usario
        user, token = create_user()
        service = create_service(user)

        conector1 = create_conector(ConectorForTest.name)
        conector2 = create_conector(ConectorForTestB.name)
        subscription1 = create_subscription(service, conector1)
        subscription2 = create_subscription(service, conector2)

        # Cuerpo del POST sin el campo message
        data = {
            "service": service.id,
            "message": {
                "title": "TestTitle",
                "body": "TestBody"
            },
            # Forzamos el fallo del envío de la notificación en el conector2
            "options": {
                f"{conector2.id}": {
                    "force_fail": True
                }
            }
        }

        # Mockeamos el import de los conectores para que solo se cargue el conector de test
        with mock.patch("api.util.import_conectors") as mock_import_conectors:

            mock_import_conectors.return_value = [
                ConectorForTest, ConectorForTestB]

            # POST  del data
            request = self.factory.post(endpoint, data, format="json")
            force_authenticate(request, user, token)

            # Llamamos a la vista
            response = asyncio.run(NotificationDetails.as_view()(request))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["successful"],
                             [{'subscription_id': subscription1.id,
                               'conector_name': ConectorForTest.name}])
            self.assertEqual(response.data["fails"],
                             [{'subscription_id': subscription2.id,
                               'conector_name': ConectorForTestB.name,
                               "description": {"force_fail": True}}])

    def test_token_not_sent(self):
        '''Comprueba que se muestra un error si el token no se envia'''

        # POST  del data
        request = self.factory.post(endpoint, format="json")

        # Llamamos a la vista
        response = asyncio.run(NotificationDetails.as_view()(request))
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {
            "detail": "Authentication credentials were not provided."
        })

    def test_token_unrecognized(self):
        '''Comprueba que se muestra un error si el token no se reconoce'''

        token = Token.generate_key()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(endpoint, format="json")

        # Llamamos a la vista
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {
            "detail": "Invalid token."
        })
