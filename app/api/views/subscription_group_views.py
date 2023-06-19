from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from api.models import Subscription, SubscriptionGroup
from api.serializers import SubscriptionGroupsSerializer
from api.models import Service
from api.util import has_permissions

import logging
logger = logging.getLogger("file_logger")


class SubscriptionGroupListApiView(APIView):

    def get(self, request, *args, **kwargs):
        '''
        Muestra los grupos existentes.
        '''

        subs_groups = None

        if request.user.is_staff:
            subs_groups = SubscriptionGroup.objects.all()
        else:
            services = Service.objects.filter(
                owner=request.user)
            subs_groups = SubscriptionGroup.objects.filter(
                service_id__in=services)

        serializer = SubscriptionGroupsSerializer(subs_groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Registra un grupo en el sistema.
        '''

        serializer = SubscriptionGroupsSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(
                f"Error al registrar el grupo - {serializer.errors}.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        group = serializer.save()
        logger.info(
            f"Grupo nuevo con id {group.id} registrada al servicio '{group.service.name.upper()}' con id {group.service.id}.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubscriptionsGroupDetailsApiView(APIView):

    def get(self, request, group_id, *args, **kwargs):
        '''
        Muestra los detalles del grupo de suscipción con el id pasado por parámetros.
        '''
        subscription_group = get_group(group_id)
        if not subscription_group:
            return Response(
                {"res": f"Grupo con id {subscription_group} no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not has_permissions(request, subscription_group.service.owner):
            return Response(
                {"res": f"No tienes permisos."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SubscriptionGroupsSerializer(subscription_group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, group_id, *args, **kwargs):
        '''
        Actualizar un grupo de suscriptores.
        '''

        subscription_group = get_group(group_id)
        if not subscription_group:
            logger.error(
                f"Error al actualizar el grupo {subscription_group} - Grupo de suscriptores con id {subscription_group} no existe.")
            return Response(
                {"res": f"Grupo de suscriptores con id {subscription_group} no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not has_permissions(request, subscription_group.service.owner):
            logger.error(
                f"Error al actualizar el grupo de suscripción {subscription_group} - Usuario {request.user.id} no tienes permisos.")
            return Response(
                {"res": f"No tienes permisos."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SubscriptionGroup(
            instance=subscription_group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"Grupo de suscripción {subscription_group} actualizado.")
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, group_id, *args, **kwargs):
        '''
        Eliminar una grupo de suscripción del sistema
        '''

        subscription_group = get_group(group_id)

        if not subscription_group:
            logger.error(
                f"Error al eliminar el grupo de suscripción {group_id} - Grupo de suscripción con id {group_id} no existe.")
            return Response({"res": f"Grupo de suscripción con id {group_id} no existe."}, status=status.HTTP_404_NOT_FOUND)

        if not has_permissions(request, subscription_group.service.owner):
            logger.error(
                f"Error al eliminar el grupo de suscripción {group_id} - Usuario {request.user.id} no tienes permisos.")
            return Response(
                {"res": f"No tienes permisos."},
                status=status.HTTP_403_FORBIDDEN
            )

        subscription_group.delete()
        logger.info(
            f"Grupo de suscripción {group_id} eliminada correctamente.")
        return Response({"res": "Suscripción eliminada."})


def get_group(group_id):
    '''
    Busca en la BD el grupo con id group_id
    '''
    try:
        return SubscriptionGroup.objects.get(id=group_id)
    except SubscriptionGroup.DoesNotExist:
        return None
