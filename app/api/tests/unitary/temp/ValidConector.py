
from rest_framework.serializers import Serializer
from api.conectors.IConector import IConector
from rest_framework import serializers

class ValidConector(IConector):

    def getDetails() -> dict:
        raise NotImplementedError

    async def notify(data, options={}) -> dict or None:

        raise NotImplementedError

    def get_subscription_serializer() -> Serializer:
        raise NotImplementedError
    