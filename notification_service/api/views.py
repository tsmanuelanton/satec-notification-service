import json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Conector, Service, Subscription
from .serializers import ConectorsSerializer, MessageSerializer, ServicesSerializer, SubscriptionsSerializer
from .conectors.push_api import Push_API


class SuscriptionsListApiView(APIView):

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


class ServicesListApiView(APIView):

    def get(self, request, *args, **kwargs):
        '''
        Muestra los servicios registrados.
        '''

        services = Service.objects
        serializer = ServicesSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Registra un servicio en el sistema.
        '''

        data = {
            'service_name': request.data.get('service_name'),
        }

        serializer = ServicesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServicesDetailsApiView(APIView):

    def get_service(service_id):
        '''
        Busca en la BD un servicio concreto
        '''
        try:
            return Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return None

    def get(self, request, service_id, *args, **kwargs):
        '''
        Muestra los detalles del servicio con id pasado por parámetros.
        '''

        service = ServicesDetailsApiView.get_service(service_id)
        if not service:
            return Response(
                {"res": f"Servicio con id {service_id} no existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ServicesSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, service_id, *args, **kwargs):
        '''
        Actualizar un servicio
        '''

        data = {
            'service_name': request.data.get('service_name'),
        }

        service = self.get_service(service_id)
        if not service:
            return Response(
                {"res": f"Servicio con id {service_id} no existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ServicesSerializer(
            instance=service, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_id, *args, **kwargs):
        '''
        Elimina un servicio del sistema
        '''

        service = self.get_service(service_id)
        if not service:
            return Response(
                {"res": f"Servicio con id {service_id} no existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        service.delete()

        return Response(
            {"res": "Servicio eliminado"},
            status=status.HTTP_200_OK
        )


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

        # TODO: Comprobar que el cliente es el servicio que dice ser

        # Obtenemos los suscriptores asociados a este servicio
        subscriptions = Subscription.objects.filter(service_id=service_id)

        for subscription in subscriptions:
            data = {
                "subscription": subscription,
                "message":  json.dumps(msgSerializer["message"].value)
            }
            try:
                MessagesApiView.sendDataToConector(
                    data, subscription.conector_id.id)

            except Conector.BaseException:
                return Response({"res": "Se ha producido un error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"res": "Éxito"}, status=status.HTTP_200_OK)


class ConectorsApiView(APIView):

    def get(self, request, *args, **kwargs):
        '''
        Muestra los conectores disponibles.
        '''

        conectors = Conector.objects
        serializer = ConectorsSerializer(conectors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Registra una suscripción en el sistema.
        '''

        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'meta': request.data.get('meta'),
        }

        serializer = ConectorsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
