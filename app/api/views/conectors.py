from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.serializers import ConectorsSerializer
from api.models import Conector
from api.util import get_conector

class ConectorsList(APIView):

    def get(self, request, *args, **kwargs):
        '''
        Muestra los conectores disponibles.
        '''

        conectors = Conector.objects
        serializer = ConectorsSerializer(conectors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ConectorDetails(APIView):

    def get(self, request, conector_id, *args, **kwargs):
        '''
        Muestra los detalles del conector
        '''

        conector = get_conector(conector_id)
        if not conector:
            return Response(
                {"detail": f"Conector {conector_id} not found."},
                status=status.HTTP_404_NOT_FOUND)

        serializer = ConectorsSerializer(conector, context={"show_details": True})
        return Response(serializer.data, status=status.HTTP_200_OK)
