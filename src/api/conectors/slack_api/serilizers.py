from rest_framework import serializers


class SubcriptionDataSlack(serializers.Serializer):
    '''Valida el campo subsription data de la suscripción '''
    channel = serializers.CharField()
    token = serializers.CharField()
