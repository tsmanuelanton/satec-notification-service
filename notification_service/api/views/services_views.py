from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.models import Service
from api.serializers import ServicesSerializer
from .util import has_permissions


class ServicesListApiView(APIView):

    def get(self, request: Request, *args, **kwargs):
        '''
        Muestra los servicios registrados del usuario.
        '''

        services = None
        if request.user.is_staff:
            services = Service.objects.all()
        else:
            services = Service.objects.filter(
                service_owner=request.user)

        serializer = ServicesSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        '''
        Registra un servicio en el sistema.
        '''

        data = {
            'service_name': request.data.get('service_name'),
            'service_owner': request.user.id
        }

        serializer = ServicesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServicesDetailsApiView(APIView):

    def get(self, request, service_id, *args, **kwargs):
        '''
        Muestra los detalles del servicio con id pasado por parámetros.
        '''

        service = get_service(service_id)
        if not service:
            return Response(
                {"res": f"Servicio con id {service_id} no existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.is_staff or request.user != service.service_owner:
            return Response(
                {"res": f"No tienes permisos"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ServicesSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, service_id, *args, **kwargs):
        '''
        Actualizar un servicio
        '''

        service = get_service(service_id)
        if not service:
            return Response(
                {"res": f"Servicio con id {service_id} no existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.is_staff or request.user != service.service_owner:
            return Response(
                {"res": f"No tienes permisos"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ServicesSerializer(
            instance=service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_id, *args, **kwargs):
        '''
        Elimina un servicio del sistema
        '''

        service = get_service(service_id)
        if not service:
            return Response(
                {"res": f"Servicio con id {service_id} no existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.is_staff or request.user != service.service_owner:
            return Response(
                {"res": f"No tienes permisos"},
                status=status.HTTP_403_FORBIDDEN
            )

        service.delete()

        return Response(
            {"res": "Servicio eliminado"},
            status=status.HTTP_200_OK
        )


def get_service(service_id):
    '''
    Busca en la BD un servicio concreto
    '''
    try:
        return Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return None
