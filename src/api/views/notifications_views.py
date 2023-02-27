from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.models import Conector, Subscription
from api.serializers import MessageSerializer
from api.util import has_permissions, import_conectors
from api.views.services_views import get_service


class NotificationsApiView(APIView):

    def post(self, request, *args, **kwargs):
        '''
        Envía el mensaje recibido al conector aducado
        '''

        msgSerializer = MessageSerializer(data=request.data)
        if not msgSerializer.is_valid():
            return Response(msgSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service_id = request.data.get('service')

        service = get_service(service_id)
        if not service:
            return Response({"res": "Unknown service"}, status=status.HTTP_400_BAD_REQUEST)

        if not has_permissions(request, service.owner):
            return Response(
                {"res": f"No tienes permisos"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Obtenemos los suscriptores asociados a este servicio
        subscriptions = Subscription.objects.filter(service=service)

        try:
            notify_subscriptors(
                msgSerializer["message"].value, msgSerializer["meta"].value, subscriptions)

        except BaseException as e:
            return Response({"res": f"Se ha producido un error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"res": "Éxito"}, status=status.HTTP_200_OK)


def notify_subscriptors(msg, meta, subscriptions):
    for subscription in subscriptions:
        data = {
            "subscription_id": subscription.id,
            "subscription_data": subscription.subscription_data,
            "message":  msg,
            "meta": meta
        }
        send_data_to_conector(
            data, subscription.conector)


def send_data_to_conector(data, conector: Conector):

    meta = data["meta"].get(str(conector.id), {})
    available_conectors = import_conectors("api/conectors")
    for available_con in available_conectors:
        if conector.name == available_con.getDetails().get("name"):
            available_con.notify(data, meta)
