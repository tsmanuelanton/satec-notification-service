from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.models import Service
from api.serializers import ServicesSerializer

import logging
logger = logging.getLogger("file_logger")


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
                owner=request.user)

        serializer = ServicesSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        '''
        Registra un servicio en el sistema.
        '''

        data = {
            'name': request.data.get('name'),
            'owner': request.user.id, 
            'meta': request.data.get('meta', {})
        }

        serializer = ServicesSerializer(data=data)
        if serializer.is_valid():
            service = serializer.save()
            logger.info(
                f"El usuario {data.get('owner')} ha registrado el servicio '{data.get('name').upper()}' con id {service.id}.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error(
            f"Error al registrar servicio por el usuario {data.get('owner')} - {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServicesDetailsApiView(APIView):

    def get(self, request, service_id, *args, **kwargs):
        '''
        Muestra los detalles del servicio con id pasado por parámetros.
        '''

        service = get_service(service_id)
        if not service:
            return Response(
                {"res": f"Servicio con id {service_id} no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_staff and request.user != service.owner:
            return Response(
                {"res": f"No tienes permisos."},
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
            logger.error(
                f"Error al actualizar el servicio {service_id} - Servicio con id {service_id} no existe.")
            return Response(
                {"res": f"Servicio con id {service_id} no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_staff and request.user != service.owner:
            logger.error(
                f"Error al actualizar el servicio {service_id} - Usuario {request.user.id} no tienes permisos.")
            return Response(
                {"res": f"No tienes permisos."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ServicesSerializer(
            instance=service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"Servicio {service_id} actualizado.")
            return Response(serializer.data, status=status.HTTP_200_OK)

        logger.error(
            f"Error al actualizar servicio {service_id} - {serializer.errors}.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_id, *args, **kwargs):
        '''
        Elimina un servicio del sistema
        '''

        service = get_service(service_id)
        if not service:
            logger.error(
                f"Error al eliminar el servicio {service_id} - Servicio con id {service_id} no existe.")
            return Response(
                {"res": f"Servicio con id {service_id} no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_staff and request.user != service.owner:
            logger.error(
                f"Error al eliminar servicio {service_id} - Usuario {request.user.id} no tienes permisos.")
            return Response(
                {"res": f"No tienes permisos."},
                status=status.HTTP_403_FORBIDDEN
            )

        service.delete()
        logger.info(
            f"Servicio {service_id} eliminado correctamente.")
        return Response(
            {"res": "Servicio eliminado."},
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
