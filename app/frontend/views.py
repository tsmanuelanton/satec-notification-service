from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView

from frontend.forms import RegisterForm

class SuccessView(View):
    def get(self, request):
        return HttpResponse("¡Gracias por registrarte!")

class RegisterView(FormView):
    template_name = "frontend/index.html"
    form_class = RegisterForm
    success_url = "/success"

    def form_valid(self, form):
        print(form.data.is_valid())
        return super().form_valid(form)
