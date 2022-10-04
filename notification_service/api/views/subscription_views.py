from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from api.models import Conector, Subscription
from api.serializers import SubscriptionsSerializer
from api.conectors.push_api import Push_API


class SuscriptionsListApiView(APIView):

    def from_conector_get_subscription_serializer(conector_id):
        '''
        Devuelve el serializador del subscription_data del conector
        '''
        conector = Conector.objects.get(id=conector_id)
        if conector.name == 'Push API - Navegadores':
            return Push_API.get_subscription_serializer()

    def get(self, request, *args, **kwargs):
        '''
        Muestra las suscripciones registradas.
        '''

        subscriptions = Subscription.objects
        serializer = SubscriptionsSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Registra una suscripción en el sistema.
        '''

        serializer = SubscriptionsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Validar el campo subscription_data con el conector específico
        subscription_data_serializer = SuscriptionsListApiView.from_conector_get_subscription_serializer(
            request.data.get('conector_id'))
        serialized = subscription_data_serializer(
            data=request.data.get('subscription_data'))
        if not serialized.is_valid():
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SuscriptionsDetailsApiView(APIView):

    def get_subscription(self, subscription_id):
        '''
        Busca en la BD la suscripción con id subscription_id
        '''
        try:
            return Subscription.objects.get(id=subscription_id)
        except Subscription.DoesNotExist:
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

        subscription = self.get_subscription(subscription_id)
        if not subscription:
            return Response(
                {"res": f"Suscripción con id {subscription_id} no existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SubscriptionsSerializer(
            instance=subscription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, subscription_id, *args, **kwargs):
        '''
        Eliminar una suscripción del sistema
        '''

        if not request.data.get("token"):
            return Response({"res": f"Falta el token de seguridad"}, status=status.HTTP_400_BAD_REQUEST)

        subscription = self.get_subscription(subscription_id)

        if not subscription:
            return Response({"res": f"No se ha encontrado ninguna subscripción con id {subscription_id}"}, status=status.HTTP_404_NOT_FOUND)

        if request.data["token"] != subscription.service_id.token:
            return Response({"res": "Token no válido"}, status=status.HTTP_401_UNAUTHORIZED)

        subscription.delete()

        return Response({"res": "Subscripción eliminada"})
