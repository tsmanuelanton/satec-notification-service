from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Subscriptions
from .serializers import SubscriptionsSerializer


class SuscriptionsListApiView(APIView):

    def get(self, request, *args, **kwargs):
        '''
        Muestra las suscripciones registradas.
        '''

        subscriptions = Subscriptions.objects
        serializer = SubscriptionsSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Registra una suscripción en el sistema.
        '''

        data = {
            'service_id': request.data.get('service_id'),
            'subscription_data': request.data.get('subscription_data'),
        }

        serializer = SubscriptionsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuscriptionsDetailsApiView(APIView):

    def get_subscription(self, subscription_id):
        '''
        Busca en la BD la suscripción con id subscription_id
        '''
        try:
            return Subscriptions.objects.get(id=subscription_id)
        except Subscriptions.DoesNotExist:
            return None

    def get(self, request, subscription_id, *args, **kwargs):
        '''
        Muestra los detalles de la suscripción con el id pasado por parámetros.
        '''

        subscription = self.get_subscription(subscription_id)
        if not subscription:
            return Response(
                {"res": f"Suscripción con id {subscription_id} no existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SubscriptionsSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, subscription_id, *args, **kwargs):
        '''
        Actualizar una suscripción
        '''

        data = {
            'service_id': request.data.get('service_id'),
            'subscription_data': request.data.get('subscription_data'),
        }

        subscription = self.get_subscription(subscription_id)
        if not subscription:
            return Response(
                {"res": f"Suscripción con id {subscription_id} no existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SubscriptionsSerializer(
            instance=subscription, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subscription_id, *args, **kwargs):
        '''
        Eliminar una suscripción del sistema
        '''

        subscription = self.get_subscription(subscription_id)
        if not subscription:
            return Response(
                {"res": f"Suscripción con id {subscription_id} no existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription.delete()

        return Response(
            {"res": "Suscripción eliminada"},
            status=status.HTTP_200_OK
        )
