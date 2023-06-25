from rest_framework.test import APITestCase
from api.serializers import SubscriptionGroupsSerializer
from api.models import SubscriptionGroup
from api.tests.views.util import create_service, create_user
endpoint = "/v1/conectors"

class TestConectorSerializer(APITestCase):

    def test_service_exists(self):
        '''Comprueba que es válido un grupo con todos los campos y cuyo servicio existe'''
        user, _ = create_user()
        service = create_service(user)
        service.save()

        data = {"name": "conectorNuevo", "service": service.id, "meta": {"key": "value"}}
        serializer = SubscriptionGroupsSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_service_not_exists(self):
        '''Comprueba que no es válido un grupo con todos los campos y cuyo servicio no existe'''
        data = {"name": "conectorNuevo", "service": 1, "meta": {"key": "value"}}
        serializer = SubscriptionGroupsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["service"][0]), "Invalid pk \"1\" - object does not exist.")
    
    def test_missing_name(self):
        '''Comprueba que se lanza un error indicando que falta el nombre'''
        user, _ = create_user()
        service = create_service(user)
        service.save()

        data = {"service": service.id, "meta": {"key": "value"}}
        serializer = SubscriptionGroupsSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors.get("name")[0], serializer.error_messages["required"])
    
    def test_missing_service(self):
        '''Comprueba que se lanza un error indicando que falta el servicio'''
        data = {"name": "conectorNuevo", "meta": {"key": "value"}}
        serializer = SubscriptionGroupsSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors.get("service")[0], serializer.error_messages["required"])
    
    def test_missing_meta(self):
        '''Comprueba que es válido cuando falta el campo meta'''
        user, _ = create_user()
        service = create_service(user)
        service.save()

        data = {"name": "conectorNuevo", "service": service.id}
        serializer = SubscriptionGroupsSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_all(self):
        '''Comprueba que se muestra un error indicando los campos obligatorios que faltan'''
        data = {}
        serializer = SubscriptionGroupsSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        self.assertEqual(serializer.errors.get("name")[0], serializer.error_messages["required"])
        self.assertEqual(serializer.errors.get("service")[0], serializer.error_messages["required"])
        self.assertIsNone(serializer.errors.get("meta"))