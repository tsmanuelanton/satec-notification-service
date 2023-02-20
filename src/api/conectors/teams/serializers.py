from rest_framework import serializers


class SubcriptionDataTeams(serializers.Serializer):
    '''Valida el campo subsription data de la suscripción '''
    channel_id = serializers.CharField()
    team_id = serializers.CharField()
    tenant_id = serializers.CharField()
    client_id = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
