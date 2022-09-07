from django.shortcuts import HttpResponse

# Create your views here.


def notify(request):
    return HttpResponse("Conector para notificar en el navegador")
