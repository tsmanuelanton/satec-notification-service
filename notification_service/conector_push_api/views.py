from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from conector_push_api.serializers import NotificationSerializer
from pywebpush import webpush, WebPushException


class NotificationApiView(APIView):

    def post(self, request, *args, **kwargs):
        '''
        Envía notificaciones a los navegadores e los suscriptores
        '''

        serializer = NotificationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        subscriptions = serializer.data['subscription_data']

        # for subscription in subscriptions:
        # TODO : Enviamos la notificación al push service correspondiente
        # try:
        #     webpush(
        #         subscription_info=subscription,
        #         data= serializer.data["message"],
        #         vapid_private_key='some-private-key',
        #         vapid_claims={
        #             'sub': 'mailto:email@email.com'
        #         }
        #     )
        # except WebPushException as e:
        #     raise e

        return Response({"res": "Éxito"}, status=status.HTTP_200_OK)
