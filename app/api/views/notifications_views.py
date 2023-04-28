from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.models import Conector, Subscription
from api.serializers import MessageSerializer
from api.util import has_permissions, import_conectors
from api.views.services_views import get_service

import logging
logger = logging.getLogger("file_logger")

import asyncio
from asgiref.sync import async_to_sync
import time

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
        
        # Enviamos las notificaciones a los suscriptores
        successfull_msgs, not_successfull_msgs, fails = notify_subscriptors(
            msgSerializer, service)
        
        logger.info(
            f"El servicio {service.name} con id {service.id} ha enviado {successfull_msgs} notificaciones exitosas y han fallado {not_successfull_msgs}.")

        return Response({"res": f"Se han enviado {successfull_msgs} notificaciones exitosas y han fallado {not_successfull_msgs}.",
                         "fallos": fails}, status=status.HTTP_200_OK)
    
async def send_data_to_conector(data, conector: Conector):
    '''Obtinene los conectores cargados y envía los datos al conector adecuado'''
    try:
        options = data["options"].get(str(conector.id), {})
        available_conectors = import_conectors("api/conectors")
        for available_con in available_conectors:
            if conector.name == available_con.getDetails().get("name"):
                return (await available_con.notify(data, options)), conector
    except BaseException as e:
        return str(e), conector
        

@async_to_sync
async def notify_subscriptors(msgSerializer, service):
    '''Envía las notificaciones a los suscriptores del servicio'''
    fails = []
    tasks = [] # Almacena las tareas send_data_to_conector
    successfull_msgs, not_successfull_msgs = 0, 0

    subscriptions = Subscription.objects.filter(
        service=service).select_related("conector") # Obtenemos las suscripciones del servicio y sus conectores
    
    async for subscription in subscriptions:
        conector = subscription.conector
        if len(msgSerializer.data["restricted_to"]) > 0:
            if conector.id not in msgSerializer.data["restricted_to"]:
                continue
        data = {
            "subscription_id": subscription.id,
            "subscription_data": subscription.subscription_data,
            "message":  msgSerializer["message"].value,
            "options": msgSerializer["options"].value
        }

        coroutine = send_data_to_conector(data, conector)
        tasks.append(asyncio.create_task(coroutine))
    
    for task in asyncio.as_completed(tasks):
        error_info, conector =  await task # Obtenemos el resultado de la tarea send_data_to_conector
        if not error_info:
            successfull_msgs += 1
        else:
            not_successfull_msgs += 1
            notification_context = {
                "subscription_id": subscription.id,
                "conector_name": conector.name
            }
            info = {
                "service_name": service.name,
                "service_id": service.id,
                **notification_context,
                "description": error_info
            }

            logger.error(f"Error al notificar - {info}")
            fails.append({**notification_context, "description": error_info})

    return successfull_msgs, not_successfull_msgs, fails
