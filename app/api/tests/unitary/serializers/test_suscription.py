from rest_framework.test import APITestCase
from api.serializers import SubscriptionsSerializer
from api.tests.views.util import ConectorForTest, FakeSerializer, create_service, create_user, create_conector, create_subscription_group
endpoint = "/v1/conectors"
from unittest import mock

class TestConectorSerializer(APITestCase):

    def test_all_valid(self):
        '''Comprueba que es válido la suscipción con todos los campos y todos válidos'''
        user, _ = create_user()
        service = create_service(user)
        conector = create_conector(ConectorForTest.name)
        group = create_subscription_group(service)

        subscription_data = {
            "field_required": "value1",
            "field_not_required": "value2",
        }

        data = {"service": service.id, "conector": conector.id, "subscription_data": subscription_data, "group": group.id}
        serializer = SubscriptionsSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_service_not_exists(self):
        '''Comprueba que no es válido la suscipción si el servicio no existe'''
        user, _ = create_user()
        conector = create_conector(ConectorForTest.name)
        service = create_service(user)
        group = create_subscription_group(service)

        subscription_data = {
            "field_required": "value1",
            "field_not_required": "value2",
        }

        data = {"service": 999, "conector": conector.id, "subscription_data": subscription_data, "group": group.id}
        serializer = SubscriptionsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["service"][0]), 'Invalid pk \"999\" - object does not exist.')
    
    def test_conector_not_exists(self):
        '''Comprueba que no es válido la suscipción si el conector no existe'''
        user, _ = create_user()
        service = create_service(user)

        group = create_subscription_group(service)


        subscription_data = {
            "field_required": "value1",
            "field_not_required": "value2",
        }

        data = {"service": service.id, "conector": 999, "subscription_data": subscription_data, "group": group.id}
        serializer = SubscriptionsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["conector"][0]), 'Invalid pk \"999\" - object does not exist.')

    def test_bad_subscription_data(self):
        '''Comprueba que no es válido la suscipción si el conector no existe'''
        user, _ = create_user()
        conector = create_conector(ConectorForTest.name)
        service = create_service(user)
        group = create_subscription_group(service)

        subscription_data = {
            # "field_required": "value1",
            "field_not_required": "value2",
        }

        with mock.patch("api.serializers.get_subscription_data_serializer") as mock_get_serializer:
            # Mock de la función que devuelve el serializer
            mock_get_serializer.return_value = FakeSerializer
            data = {"service": service.id, "conector": conector.id, "subscription_data": subscription_data, "group": group.id}
            serializer = SubscriptionsSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertEqual(str(serializer.errors["subscription_data"][0]["field_required"][0]), 'This field is required.')

    def test_group_not_exists(self):
        ''''Comprueba que no es válido la suscipción si el grupo no existe'''
        user, _ = create_user()
        service = create_service(user)

        conector = create_conector(ConectorForTest.name)


        subscription_data = {
            "field_required": "value1",
            "field_not_required": "value2",
        }

        data = {"service": service.id, "conector": conector.id, "subscription_data": subscription_data, "group": 999}
        serializer = SubscriptionsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["group"][0]), 'Invalid pk \"999\" - object does not exist.')
    
    def test_missing_service(self):
        '''Comprueba que no es válido la suscipción si falta el servicio'''
        user, _ = create_user()
        conector = create_conector(ConectorForTest.name)
        service = create_service(user)
        group = create_subscription_group(service)

        subscription_data = {
            "field_required": "value1",
            "field_not_required": "value2",
        }

        data = {"conector": conector.id, "subscription_data": subscription_data, "group": group.id}
        serializer = SubscriptionsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["service"][0]), 'This field is required.')
    
    def test_missing_conector(self):
        '''Comprueba que no es válido la suscipción si falta el conector'''
        user, _ = create_user()
        service = create_service(user)
        group = create_subscription_group(service)

        subscription_data = {
            "field_required": "value1",
            "field_not_required": "value2",
        }

        data = {"service": service.id, "subscription_data": subscription_data, "group": group.id}
        serializer = SubscriptionsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["conector"][0]), 'This field is required.')

    def test_missing_subscription_data(self):
        '''Comprueba que no es válido la suscipción si falta el subscription_data'''
        user, _ = create_user()
        service = create_service(user)
        conector = create_conector(ConectorForTest.name)
        group = create_subscription_group(service)

        data = {"service": service.id, "conector": conector.id, "group": group.id}
        serializer = SubscriptionsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["subscription_data"][0]), 'This field is required.')
    
    def test_missing_group(self):
        '''Comprueba que no es válido la suscipción si falta el grupo'''
        user, _ = create_user()
        service = create_service(user)
        conector = create_conector(ConectorForTest.name)

        subscription_data = {
            "field_required": "value1",
            "field_not_required": "value2",
        }

        data = {"service": service.id, "conector": conector.id, "subscription_data": subscription_data}
        serializer = SubscriptionsSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_missing_subscription_data(self):
        '''Comprueba que no es válido la suscipción si falta el subscription_data'''
        user, _ = create_user()
        service = create_service(user)
        conector = create_conector(ConectorForTest.name)
        group = create_subscription_group(service)

        data = {"service": service.id, "conector": conector.id, "group": group.id}
        serializer = SubscriptionsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["subscription_data"][0]), 'This field is required.')
    
    def test_missing_meta(self):
        '''Comprueba que no es válido la suscipción si falta el meta'''
        user, _ = create_user()
        service = create_service(user)
        conector = create_conector(ConectorForTest.name)
        group = create_subscription_group(service)

        subscription_data = {
            "field_required": "value1",
            "field_not_required": "value2",
        }

        data = {"service": service.id, "conector": conector.id, "subscription_data": subscription_data, "group": group.id}
        serializer = SubscriptionsSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_missing_all(self):
        '''Comprueba que no es válido la suscipción si falta todo'''
        data = {}
        serializer = SubscriptionsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["service"][0]), 'This field is required.')
        self.assertEqual(str(serializer.errors["conector"][0]), 'This field is required.')
        self.assertEqual(str(serializer.errors["subscription_data"][0]), 'This field is required.')
