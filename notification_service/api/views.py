from django.http import HttpRequest, JsonResponse


def index(request: HttpRequest):
    return JsonResponse({'Página': "Índice"})
