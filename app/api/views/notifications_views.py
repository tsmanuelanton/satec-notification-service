from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.models import Conector, Subscription
from api.serializers import MessageSerializer
from api.util import has_permissions, import_conectors
from api.views.services_views import get_service

import logging
logger = logging.getLogger("file_logger")


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
            return Response({"res": "Unknown service."}, status=status.HTTP_400_BAD_REQUEST)

        if not has_permissions(request, service.owner):
            return Response(
                {"res": f"No tienes permisos."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Obtenemos los suscriptores asociados a este servicio
        subscriptions = Subscription.objects.filter(service=service)

        successfull_msgs = 0
        not_successfull_msgs = 0

        fails = []
        for subscription in subscriptions:
            conector = subscription.conector
            if len(msgSerializer.data["restricted_to"]) > 0:
                if conector.id not in msgSerializer.data["restricted_to"]:
                    continue
            service_info = {"service_name": service.name,
                            "service_id": service.id}
            notification_context = {"subscription_id": subscription.id,
                                    "conector_name": conector.name}
            try:
                data = {
                    "subscription_id": subscription.id,
                    "subscription_data": subscription.subscription_data,
                    "message":  msgSerializer["message"].value,
                    "meta": msgSerializer["meta"].value
                }

                success, error_info = send_data_to_conector(
                    data, subscription.conector)

                if success:
                    successfull_msgs += 1
                else:
                    not_successfull_msgs += 1
                    info = service_info | notification_context | {
                        "description": error_info}
                    logger.error(
                        f"Error al notificar - {info}.")
                    fails.append(notification_context | {
                                 "description": str(error_info)})

            except BaseException as e:
                not_successfull_msgs += 1
                info = service_info | notification_context | {"description": e}
                logger.error(
                    f"Error al notificar - {info}")
                fails.append(notification_context | {"description": str(e)})

        logger.info(
            f"El servicio {service.name} con id {service.id} ha enviado {successfull_msgs} notificaciones exitosas y han fallado {not_successfull_msgs}.")

        return Response({"res": f"Se han enviado {successfull_msgs} notificaciones exitosas y han fallado {not_successfull_msgs}.",
                         "fallos": fails}, status=status.HTTP_200_OK)


def send_data_to_conector(data, conector: Conector):

    meta = data["meta"].get(str(conector.id), {})
    available_conectors = import_conectors("api/conectors")
    for available_con in available_conectors:
        if conector.name == available_con.getDetails().get("name"):
            return available_con.notify(data, meta)
