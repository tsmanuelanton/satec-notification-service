from rest_framework import serializers


class SubcriptionDataEmail(serializers.Serializer):
    '''Valida el campo subsription data de la suscripción '''
    smtp_host = serializers.CharField()
    port = serializers.IntegerField(
        min_value=0, max_value=65535)
    From = serializers.CharField()
    To = serializers.CharField()
    user = serializers.EmailField()
    password = serializers.CharField()
