import importlib
import inspect
from pathlib import Path

from api.conectors.IConector import IConector


def has_permissions(request, user):
    return request.user.is_staff or request.user == user


def import_conectors(path):
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
