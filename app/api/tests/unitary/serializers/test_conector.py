from rest_framework.test import APITestCase
from api.serializers import ConectorsSerializer
from api.tests.views.util import create_conector
endpoint = "/v1/conectors"

class TestConectorSerializer(APITestCase):

    def test_full_unique(self):
        '''Comprueba que es válido un conector con todos los campos y  con nombre único'''

        data = {"name": "conectorNuevo", "description": "descripción", "meta": {"key": "value"}}
        self.assertTrue(ConectorsSerializer(data=data).is_valid())
    
    def test_full_not_unique(self):
        '''Comprueba que se muestra un error indicando que el nombre ya existe'''

        create_conector("conectorPrevio")
        data = {"name": "conectorPrevio", "description": "descripción", "meta": {"key": "value"}}
        serializer = ConectorsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    
    def test_missing_name(self):
        '''Comprueba que se lanza un error indicando que falta el nombre'''

        data = {"description": "descripción", "meta": {"key": "value"}}
        serializer = ConectorsSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors.get("name")[0], serializer.error_messages["required"])


    def test_missing_description(self):
        '''Comprueba que se lanzan errores indicando que falta la descripción'''

        data = {"name": "conectorPrevio", "meta": {"key": "value"}}
        serializer = ConectorsSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors.get("description")[0], serializer.error_messages["required"])
    
    def test_missing_meta(self):
        '''Comprueba que es válido cuando falta el campo meta'''

        data = {"name": "conectorPrevio", "description": "descripción"}
        self.assertTrue(ConectorsSerializer(data=data).is_valid())
    
    def test_missing_all(self):
        '''Comprueba que se muestra un error indicando los campos obligatorios que faltan'''

        data = {}
        serializer = ConectorsSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        self.assertEqual(serializer.errors.get("name")[0], serializer.error_messages["required"])
        self.assertEqual(serializer.errors.get("description")[0], serializer.error_messages["required"])
        self.assertIsNone(serializer.errors.get("meta"))

