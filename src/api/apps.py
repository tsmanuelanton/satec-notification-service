from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.utils import OperationalError
from api.util import import_conectors


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        '''Cuando la app se haya inicializado, ejecutamos el siguiente código'''
        # Los imports tienen que estar aquí para que este lista  toda la app antes de hacer imports

        try:

            register_conectors()
        except OperationalError as e:
            if str(e) == "no such table: api_conector":
                # Si no existe la tabla, esperamos a que el usario haga un migrate y
                # volvemos a intentar registrar los conectores
                # https://stackoverflow.com/a/60562764
                post_migrate.connect(register_conectors, sender=self)
            else:
                raise e


def register_conectors():
    from api.models import Conector
    from api.serializers import ConectorsSerializer

    CONECTORS_DIR = "api\conectors"
    conectors = import_conectors(CONECTORS_DIR)
    for conector in conectors:
        serialized = ConectorsSerializer(
            data=conector.getDetails())
        # Comprueba que no se haya registrado previamente
        if not Conector.objects.filter(name=conector.getDetails().get("name")):
            if serialized.is_valid():
                serialized.save()
            else:
                raise BaseException(serialized.errors)
