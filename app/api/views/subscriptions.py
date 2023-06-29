from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from api.models import Subscription
from api.serializers import SubscriptionsSerializer
from api.models import Service
from api.util import get_subscription, has_permissions

import logging
logger = logging.getLogger("file_logger")


class SubscriptionsList(APIView):

    def get(self, request, *args, **kwargs):
        '''
        Muestra las suscripciones registradas.
        '''

        subscriptions = None

        if request.user.is_staff:
            subscriptions = Subscription.objects.all()
        else:
            services = Service.objects.filter(
                owner=request.user)
            subscriptions = Subscription.objects.filter(
                service_id__in=services)

        serializer = SubscriptionsSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Registra una suscripción en el sistema.
        '''

        serializer = SubscriptionsSerializer(data=request.data, context={"show_details": True, "request": request})
        if not serializer.is_valid():
            logger.error(
                f"Error al registrar suscripción nueva - {serializer.errors}.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        subscription = serializer.save()
        logger.info(
            f"Suscripción nueva con id {subscription.id} registrada al servicio '{subscription.service.name}' con id {subscription.service.id}.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubscriptionDetails(APIView):

    def get(self, request, subscription_id, *args, **kwargs):
        '''
        Muestra los detalles de la suscripción con el id pasado por parámetros.
        '''

        subscription = get_subscription(subscription_id)
        if not subscription:
            return Response(
                {"detail": f"Subscription {subscription_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not has_permissions(request, subscription.service.owner):
            return Response(
                {"detail": f"You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SubscriptionsSerializer(subscription, context={"show_details": True})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, subscription_id, *args, **kwargs):
        '''
        Actualizar una suscripción
        '''

        subscription = get_subscription(subscription_id)
        if not subscription:
            logger.error(
                f"Error al actualizar la suscripción {subscription_id} - Suscripción con id {subscription_id} no existe.")
            return Response(
                {"detail": f"Subscription {subscription_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not has_permissions(request, subscription.service.owner):
            logger.error(
                f"Error al actualizar la suscripción {subscription_id} - Usuario {request.user.id} no tienes permisos.")
            return Response(
                {"detail": f"You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SubscriptionsSerializer(
            instance=subscription, data=request.data, partial=True, context={"show_details": True, "request": request})
        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"Suscripción {subscription_id} actualizado.")
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, subscription_id, *args, **kwargs):
        '''
        Eliminar una suscripción del sistema
        '''

        subscription = get_subscription(subscription_id)

        if not subscription:
            logger.error(
                f"Error al eliminar la suscripción {subscription_id} - Suscripción con id {subscription_id} no existe.")
            return Response({"detail": f"Subscription {subscription_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        if not has_permissions(request, subscription.service.owner):
            logger.error(
                f"Error al eliminar la suscripción {subscription_id} - Usuario {request.user.id} no tienes permisos.")
            return Response(
                {"detail": f"You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        subscription.delete()
        logger.info(
            f"Suscripción {subscription_id} eliminada correctamente.")
        return Response({"detail": f"Resource {subscription_id} deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

