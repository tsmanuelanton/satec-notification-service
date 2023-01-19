from rest_framework import serializers


class SubcriptionDataTeams(serializers.Serializer):
    '''Valida el campo subsription data de la suscripción '''
    channel_id = serializers.CharField()
    team_id = serializers.CharField()
    token = serializers.CharField()
