from rest_framework.test import APITestCase
from api.serializers import ServicesSerializer
from api.models import Service
from api.tests.views.util import create_user
endpoint = "/v1/conectors"

class TestConectorSerializer(APITestCase):

    def test_user_exists(self):
        '''Comprueba que es válido un servicio con todos los campos y cuyo dueño existe'''
        user, _ = create_user()

        data = {"name": "conectorNuevo", "owner": user.id, "meta": {"key": "value"}}
        serializer = ServicesSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_user_not_exists(self):
        '''Comprueba que no es válido un servicio con todos los campos y cuyo dueño no existe'''
        data = {"name": "conectorNuevo", "owner": 1, "meta": {"key": "value"}}
        serializer = ServicesSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["owner"][0]), "Invalid pk \"1\" - object does not exist.")
    
    def test_missing_name(self):
        '''Comprueba que se lanza un error indicando que falta el nombre'''
        user, _ = create_user()

        data = {"owner": user.id, "meta": {"key": "value"}}
        serializer = ServicesSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors.get("name")[0], serializer.error_messages["required"])

    def test_missing_owner(self):
        '''Comprueba que se lanza un error indicando que falta el dueño'''
        data = {"name": "conectorNuevo", "meta": {"key": "value"}}
        serializer = ServicesSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors.get("owner")[0], serializer.error_messages["required"])
    
    def test_missing_meta(self):
        '''Comprueba que es válido cuando falta el campo meta'''
        user, _ = create_user()

        data = {"name": "conectorNuevo", "owner": user.id}
        self.assertTrue(ServicesSerializer(data=data).is_valid())
    
    def test_missing_all(self):
        '''Comprueba que se muestra un error indicando los campos obligatorios que faltan'''
        data = {}
        serializer = ServicesSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        self.assertEqual(serializer.errors.get("name")[0], serializer.error_messages["required"])
        self.assertEqual(serializer.errors.get("owner")[0], serializer.error_messages["required"])
        self.assertIsNone(serializer.errors.get("meta"))