from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.serializers import ConectorsSerializer
from api.models import Conector


class ConectorsListApiView(APIView):

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


class ConectorsDetailsApiView(APIView):

    def get(self, request, conector_id, *args, **kwargs):
        '''
        Muestra los detalles del conector
        '''

        conector = get_conector(conector_id)
        if not conector:
            return Response(
                {"res": f"Conector con id {conector_id} no existe"},
                status=status.HTTP_404_NOT_FOUND)

        serializer = ConectorsSerializer(conector)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, conector_id, *args, **kwargs):
        '''
        Registra una suscripción en el sistema.
        '''

        conector = get_conector(conector_id)
        if not conector:
            return Response(
                {"res": f"Conector con id {conector_id} no existe"},
                status=status.HTTP_404_NOT_FOUND)

        serializer = ConectorsSerializer(
            instance=conector, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, conector_id, *args, **kwargs):
        '''
        Eliminar una suscripción del sistema
        '''

        conector = get_conector(conector_id)
        if not conector:
            return Response(
                {"res": f"Conector con id {conector_id} no existe"},
                status=status.HTTP_404_NOT_FOUND)

        conector.delete()

        return Response({"res": f"Conector {conector_id} eliminada"})


def get_conector(conector_id):
    '''
    Busca en la BD un conector concreto
    '''
    try:
        return Conector.objects.get(id=conector_id)
    except Conector.DoesNotExist:
        return None
