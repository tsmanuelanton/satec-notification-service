from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.serializers import ConectorsSerializer
from api.models import Conector


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
