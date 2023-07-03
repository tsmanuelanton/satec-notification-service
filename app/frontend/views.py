import environ
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from frontend.forms import RegisterForm
import requests
import logging
logger = logging.getLogger("file_logger")


class SuccessView(View):
    def get(self, request):
        return render(request, "frontend/success.html")

class RegisterView(FormView):
    template_name = "frontend/index.html"
    form_class = RegisterForm
    # Se considera success url cuando el formulario es valido,
    success_url = "/success"

    def form_valid(self, form):
        context = self.get_context_data()
        if form.is_valid():
            context["error"] = send_mail(form.cleaned_data)
        return render(self.request, "frontend/success.html", context=context)
    
def send_mail(data) -> str:
    '''Usa la API  de notificaicones para enviar un email al administrador'''

    env = environ.Env()
    environ.Env.read_env()
    
    service_id = env("ID_SERVICE_REGISTER_SNS")
    token = env("TOKEN_SERVICE_REGISTER_SNS")

    headers = {'Content-type': 'application/json', 'Authorization': f"Token {token}"}
    data = {
        "service": service_id,
        "message": {
            "title": "Solicitud de registro",
            "body": format_data(data)
        }
    }
    # Se hace por localhost ya que es para la otra app de django que escucha en el purto 8000
    res = requests.post(f"http://localhost:8000/api/v1/notifications",headers=headers, json=data)
    if not res.ok:
        logger.error(
            f"Error al enviar el email: ERROR {res.status_code} - {res.reason} -{res.json()}")
        return "Se ha producido un error al enviar el email, por favor intente más tarde."
    return None

def format_data(data):
    return f'''
        Nombre: {data["name"]}
        Apellido: {data["lastname"]}
        Email: {data["email"]}
        Uso profesional: {data["commercial_use"]}
        Nombre organización: {data["company_name"]}
        Descripción de uso: {data["description"]}
        '''
        

