from django.core.management.base import BaseCommand
from api.models import Conector
from api.serializers import ConectorsSerializer
from api.util import import_conectors

class Command(BaseCommand):
    help = "Reads code from api/conectors directory and adds them to the database."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        CONECTORS_DIR = "api/conectors"
        conectors = import_conectors(CONECTORS_DIR) # Lee e importa los conectores disponibles

        added_conectors = []
        for conector in conectors:
            serialized = ConectorsSerializer(
                data=conector.getDetails())
            
            conector_name = conector.getDetails().get("name")
            # Comprueba que no se haya registrado previamente
            if not Conector.objects.filter(name=conector_name):
                if serialized.is_valid():
                    serialized.save()
                    added_conectors.append(conector_name)
                else:
                    raise BaseException(serialized.errors)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {len(added_conectors)} new conectors - {", ".join(added_conectors)}')
        )

