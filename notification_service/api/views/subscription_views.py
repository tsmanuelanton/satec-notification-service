from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.models import Conector, Subscription
from api.serializers import DeleteSubsciptionSerilizer, SubscriptionsSerializer
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

        data = {
            'service_id': request.data.get('service_id'),
            'conector_id': request.data.get('conector_id'),
            'subscription_data': request.data.get('subscription_data'),
            'token': request.data.get('token'),
        }

        serializer = SubscriptionsSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Validar el campo subscription_data con el conector específico
        subscription_data_serializer = SuscriptionsListApiView.from_conector_get_subscription_serializer(
            data["conector_id"])
        serialized = subscription_data_serializer(
            data=data["subscription_data"])
        if not serialized.is_valid():
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SuscriptionsDetailsApiView(APIView):

    def get_subscription(self, field_value, field_name=id):
        '''
        Busca en la BD la suscripción con id subscription_id
        '''
        try:
            return Subscription.objects.get(field_name=field_value)
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

        serilizer = DeleteSubsciptionSerilizer(data=request.data)
        # field_name = request.data.get("fild_name")
        # field_value = request.data.get("field_value")

        # errors = []
        # if not field_name:
        #     errors.append("Falta el campo fild_name")
        # if not field_value:
        #     errors.append("Falta el campo field_value")

        # if errors.count() > 0:
        #     return Response({"res": errors})

        # subscription = self.get_subscription(field_value, field_name)
        # if not subscription:
        #     return Response(
        #         {"res": f"Suscripción con campo {field_name} {field_value} no existe"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # subscription.delete()

        # return Response(
        #     {"res": "Suscripción eliminada"},
        #     status=status.HTTP_200_OK
        # )
