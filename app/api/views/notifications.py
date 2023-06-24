from rest_framework import status
from rest_framework.response import Response
from api.models import Service, Subscription
from api.serializers import MessageSerializer
from api.util import has_permissions, import_conectors

import logging
logger = logging.getLogger("file_logger")

import asyncio
from adrf.views import APIView
from rest_framework.permissions import IsAuthenticated
class NotificationDetails(APIView):
    
    permission_classes = [IsAuthenticated]
    async def post(self, request,  *args, **kwargs):
        '''
        Envía el mensaje recibido al conector aducado
        '''

        msgSerializer = MessageSerializer(data=request.data)
        if not await msgSerializer.is_valid():
            return Response(msgSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service_id = request.data.get('service')
        service = await Service.objects.select_related().aget(id=service_id)
        if not service:
            return Response({"detail": "Unknown service."}, status=status.HTTP_400_BAD_REQUEST)

        if not has_permissions(request, service.owner):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Enviamos las notificaciones a los suscriptores
        successful, fails = await notify_subscriptors(
            msgSerializer.validated_data,
                service)

        logger.info(
            f"El servicio {service.name} con id {service.id} ha enviado {len(successful)} notificaciones exitosas y han fallado {len(fails)}.")

        return Response({"detail": f"Se han enviado {len(successful)} notificaciones exitosas y han fallado {len(fails)}.",
                            "enviados": successful,
                            "fallos": fails}, status=status.HTTP_200_OK)

    
async def notify_subscriptor(subscription,message, options):
    '''Obtinene los conectores cargados y envía los datos al conector adecuado'''
    try:
        conector = subscription.conector
        available_conectors = import_conectors()

        data = {
            "subscription_data": subscription.subscription_data,
            "message":  message,
        }
        for available_con in available_conectors:
            if conector.name == available_con.getDetails().get("name"):
                return subscription, (await available_con.notify(data, options))
    except BaseException as e:
        return subscription, str(e)


async def notify_subscriptors(notification_req, service):
    '''Envía las notificaciones a los suscriptores del servicio'''
    successes, fails = [], []
    subscriptions = Subscription.objects.filter(
        service=service).select_related("conector", "group") # Obtenemos las suscripciones del servicio y sus conectores
    
    tasks = [] # Almacena las tareas send_data_to_conector
    async for subscription in subscriptions:
        if len(notification_req["restricted_to_groups"]) > 0:
            if subscription.group == None or subscription.group.id not in notification_req["restricted_to_groups"]:
                continue
        message = notification_req["message"]
        conector_options =  notification_req["options"].get(str(subscription.conector.id))

        coroutine = notify_subscriptor(subscription,message, conector_options)
        tasks.append(coroutine)

    for task in asyncio.as_completed(tasks):
        subscription, error_info =  await task # Obtenemos el resultado de la tarea send_data_to_conector
        notification_context = {
            "subscription_id": subscription.id,
            "conector_name": subscription.conector.name
        }
        if not error_info:
            successes.append(notification_context)
        else:
            info = {
                "service_name": service.name,
                "service_id": service.id,
                **notification_context,
                "description": error_info
            }

            logger.error(f"Error al notificar - {info}")
            fails.append({**notification_context, "description": error_info})

    return successes, fails
