import importlib
import inspect
from pathlib import Path
from api.models import Conector, Service, Subscription, SubscriptionGroup
from api.conectors.IConector import IConector


def has_permissions(request, user):
    return request.user.is_staff or request.user == user


def import_conectors(path = "api/conectors"):
    '''Detecta los conectores disponibles y los importa y devuelve la lista de conectores'''

    path = Path(path)
    conectors = []
    for file in path.iterdir():
        if file.is_dir():
            conectors = conectors + import_conectors(file)
        if file.suffix == ".py" and not file.name.startswith("__"):
            # Eliminamos la extensión .py y sustituimos el separador / por .
            module_path = file.as_posix()[:-3].replace("/", ".")
            module = importlib.import_module(module_path)
            for name in dir(module):
                obj = getattr(module, name)
                if inspect.isclass(obj) and obj != IConector and issubclass(obj, IConector):
                    conectors.append(obj)
    return conectors

def get_conector(conector_id):
    '''
    Busca en la BD un conector concreto
    '''
    try:
        return Conector.objects.get(id=conector_id)
    except Conector.DoesNotExist:
        return None

def get_service(service_id):
    '''
    Busca en la BD un servicio concreto
    '''
    try:
        return Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return None

def get_group(group_id):
    '''
    Busca en la BD el grupo con id group_id
    '''
    try:
        return SubscriptionGroup.objects.get(id=group_id)
    except SubscriptionGroup.DoesNotExist:
        return None

def get_subscription(subscription_id):
    '''
    Busca en la BD la suscripción con id subscription_id
    '''
    try:
        return Subscription.objects.get(id=subscription_id)
    except Subscription.DoesNotExist:
        return None