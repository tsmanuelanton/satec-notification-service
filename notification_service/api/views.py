from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Subscriptions
from .serializers import SubscriptionsSerializer


class SuscriptionsApiView(APIView):

    def get(self, request, *args, **kwargs):
        '''
        Muestra las suscripciones registradas.
        '''

        subscriptions = Subscriptions.objects
        serializer = SubscriptionsSerializer(subscriptions, many=True)
        return Response(serializer.data)

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
