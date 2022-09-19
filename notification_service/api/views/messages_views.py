import json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.models import Conector, Subscription
from api.serializers import MessageSerializer
from api.conectors.push_api import Push_API
from api.views.services_views import ServicesDetailsApiView


class MessagesApiView(APIView):

    def sendDataToConector(data, conector_id):
        conector = Conector.objects.get(id=conector_id)
        if getattr(conector, "name") == 'Push API - Navegadores':
            Push_API.notify(data)

    def post(self, request, *args, **kwargs):
        '''
        Envía el mensaje recibido al conector aducado
        '''

        msgSerializer = MessageSerializer(data=request.data)
        if not msgSerializer.is_valid():
            return Response(msgSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service_id = request.data.get('service_id')

        service = ServicesDetailsApiView.get_service(service_id)
        if not service:
            return Response({"res": f"Servicio con id {service_id} no existe"}, status=status.HTTP_400_BAD_REQUEST)

        if service.token != msgSerializer.data['token']:
            return Response({"res": "El token no corresponde a ningún servicio"}, status=status.HTTP_401_UNAUTHORIZED)

        # Obtenemos los suscriptores asociados a este servicio
        subscriptions = Subscription.objects.filter(service_id=service_id)

        try:
            for subscription in subscriptions:
                data = {
                    "subscription_id": subscription.id,
                    "subscription_data": subscription.subscription_data,
                    "message":  json.dumps(msgSerializer["message"].value)
                }

                MessagesApiView.sendDataToConector(
                    data, subscription.conector_id.id)

        except BaseException as e:
            print(e)
            return Response({"res": "Se ha producido un error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"res": "Éxito"}, status=status.HTTP_200_OK)
