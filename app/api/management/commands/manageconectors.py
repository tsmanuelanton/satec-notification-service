from django.core.management.base import BaseCommand, CommandError
from api.models import Conector
from api.serializers import ConectorsSerializer
from api.util import import_conectors

class Command(BaseCommand):
    help = "Reads code from api/conectors directory and lets list, add or delete them from the database."

    def add_arguments(self, parser):

        parser.add_argument(
            "add",
            nargs="?",
            help="Add available conectors in api/conectors to app's database",
        )
        parser.add_argument(
            "--delete",
            nargs="+",
            help="Delete specified conectors from database",
        )

    def handle(self, *args, **options):
        if options["delete"]:
           self.delete_conectors(options["delete"])
        elif options["add"]:
           self.add_conectors()
        else:  # Si no se especifica ninguna opción, muestra todos los conectores registrados
            self.list_conector()

    def list_conector(self):
        self.stdout.write(
                    self.style.SUCCESS(f'Listing all registered conectors:')
                )
        for conector in Conector.objects.all():
            self.stdout.write(
                self.style.SQL_TABLE(f'-{conector.name} - {conector.description}')
            )

    def add_conectors(self):
        conectors = import_conectors("api/conectors") # Lee e importa los conectores disponibles
        added_conectors = []

        # Añade todos los conectores si no se especifica ninguno o los que se especifiquen
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
                    raise CommandError(serialized.errors)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {len(added_conectors)} new conector(s) - {", ".join(added_conectors)}')
        )

    def delete_conectors(self, conectors_names):
        del_conectors = []
        for conector_name in conectors_names:
            conector = Conector.objects.filter(name=conector_name)
            if conector:
                conector.delete()
                del_conectors.append(conector_name)
            else:
                self.stdout.write(
                    self.style.WARNING(f'Conector {conector_name} not found')
                )
        self.style.SUCCESS(f'Successfully deleted {len(del_conectors)} conector(s) - {", ".join(del_conectors)}')