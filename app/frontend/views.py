import environ
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from frontend.forms import RegisterForm
import requests

env = environ.Env()
environ.Env.read_env()
service_id = env("ID_SERVICE_REGISTER_SNS", None)
token = env("TOKEN_SERVICE_REGISTER_SNS", None)

if not service_id or not token:
    raise ValueError("ID_SERVICE_REGISTER_SNS and TOKEN_SERVICE_REGISTER_SNS must be set in .env file")


class SuccessView(View):
    def get(self, request):
        return render(request, "frontend/success.html")

class RegisterView(FormView):
    template_name = "frontend/index.html"
    form_class = RegisterForm
    success_url = "/success"

    def form_valid(self, form):
        if form.is_valid():
            send_mail(form.cleaned_data)
        return super().form_valid(form)
    
def send_mail(data):
    '''Usa la API  de notificaicones para enviar un email al administrador'''
    headers = {'Content-type': 'application/json', 'Authorization': f"Token {token}"}
    data = {
        "service": 1,
        "message": {
            "title": "Solicitud de registro",
            "body": format_data(data)
        }
    }
    res = requests.post("http://localhost:8000/api/v1/notifications2",headers=headers, json=data)
    if not res.ok:
        raise Exception(f"Error al enviar el email: STATUS CODE {res.status_code} - {res.reason} ")

def format_data(data):
    return f'''
        Nombre: {data["name"]}
        Apellido: {data["lastname"]}
        Email: {data["email"]}
        Uso profesional: {data["commercial_use"]}
        Nombre organización: {data["company_name"]}
        Descripción de uso: {data["description"]}
        '''
        

