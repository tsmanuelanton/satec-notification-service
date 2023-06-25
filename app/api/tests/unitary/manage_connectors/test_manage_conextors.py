from rest_framework.test import APITestCase
from django.core.management import call_command
from io import StringIO
from unittest import mock
from api.models import Conector
from api.tests.views.util import ConectorForTest
class TestManageConectors(APITestCase):

    def test_add_unique(self):
        '''Comprueba que se añade el conector si no está registrado'''
        with mock.patch("api.util.import_conectors") as mock_import_conectors:
            mock_import_conectors.return_value = [ConectorForTest]
            out = StringIO()
            call_command('manageconectors', '-a', stdout=out)
            self.assertIn(
                f'Successfully imported 1 new conector(s) - {ConectorForTest.name}',
                    out.getvalue()
                )
            self.assertEqual(Conector.objects.count(), 1)
    
    def test_add_repeated(self):
        '''Comprueba que no se añade el conector si ya está registrado'''
        with mock.patch("api.util.import_conectors") as mock_import_conectors:

            Conector.objects.create(name=ConectorForTest.name, description="PreviousConector").save()
            conector_repeated = ConectorForTest
            mock_import_conectors.return_value = [conector_repeated]
            out = StringIO()
            call_command('manageconectors', '--add', stdout=out)
            self.assertIn(
                f'Already registred conector {conector_repeated.name}',
                    out.getvalue()
                )
            self.assertEqual(Conector.objects.count(), 1)
    
    def test_delete_one(self):
        '''Comprueba que se elimina el conector si está registrado'''
            
        conector = Conector.objects.create(name="Conector1", description="PreviousConector")
        conector.save()
        out = StringIO()
        call_command('manageconectors', '-d', conector.name, stdout=out)
        self.assertIn(
            f'Successfully deleted 1 conector(s) - {conector.name}',
                out.getvalue()
            )
        self.assertEqual(Conector.objects.count(), 0)
    
    def test_delete_multiple(self):
        '''Comprueba que se eliminan los conectores si están registrados'''
        conector1 = Conector.objects.create(name="Conector1", description="PreviousConector")
        conector2 = Conector.objects.create(name="Conector2", description="PreviousConector")
        conector1.save()
        conector2.save()
        out = StringIO()
        call_command('manageconectors', '-d', conector1.name, conector2.name, stdout=out)
        self.assertIn(
            f'Successfully deleted 2 conector(s) - {conector1.name}, {conector2.name}',
                out.getvalue()
            )
        self.assertEqual(Conector.objects.count(), 0)
    
    def test_delete_not_registered(self):
        '''Comprueba que no se elimina el conector si no está registrado'''

        out = StringIO()
        call_command('manageconectors', '--delete', "Conector1", stdout=out)
        self.assertIn(
            f'Conector Conector1 not found',
                out.getvalue()
            )

    def test_list_empty(self):
        '''Comprueba que se lista correctamente si no hay conectores registrados'''
        out = StringIO()
        call_command('manageconectors', '-l', stdout=out)
        self.assertIn(
            f'No conectors found',
                out.getvalue()
            )
    
    def test_list_with_conectors(self):
        '''Comprueba que se lista correctamente si hay conectores registrados'''
        conector1 = Conector.objects.create(name="Conector1", description="PreviousConector")
        conector2 = Conector.objects.create(name="Conector2", description="PreviousConector")
        conector1.save()
        conector2.save()
        out = StringIO()
        call_command('manageconectors', "--list", stdout=out)
        self.assertIn(
            f'{conector1.name} - {conector2.description}',
                out.getvalue()
            )
        self.assertIn(
            f'{conector2.name} - {conector2.description}',
                out.getvalue()
            )
