from rest_framework import serializers


class SubcriptionDataTelegram(serializers.Serializer):
    '''Valida la suscripción de Telegram'''
    chat_id = serializers.CharField()
    bot_token = serializers.CharField()
