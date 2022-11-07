from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.utils import OperationalError


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        '''Cuando la app se haya inicializado, ejecutamos el siguiente código'''
        # Los imports tienen que estar aquí para que este lista  toda la app antes de hacer imports
        from api.serializers import ConectorsSerializer
        from api.models import Conector
        from api.conectors.push_api.Push_API import PushAPIConector

        def register_conectors(sender, **kwargs):
            '''Registra los conectores que tenemos en la BD'''
            conector_details = PushAPIConector.getDetails()
            # Comprueba que no se haya registrado previamente
            if not Conector.objects.filter(name=conector_details.get("name")):
                serialized = ConectorsSerializer(data=conector_details)
                if serialized.is_valid():
                    serialized.save()
                else:
                    raise (serialized.errors)

        try:
            register_conectors(None)
        except OperationalError as e:
            if str(e) == "no such table: api_conector":
                # Si no existe la tabla, esperamos a que el usario haga un migrate y
                # volvemos a intentar registrar los conectores
                # https://stackoverflow.com/a/60562764
                post_migrate.connect(register_conectors, sender=self)
            else:
                raise e
