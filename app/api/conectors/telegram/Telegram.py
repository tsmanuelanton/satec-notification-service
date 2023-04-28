from api.conectors.IConector import IConector
import requests
from .serializers import SubcriptionDataTelegram


class TelegramConector(IConector):
    def getDetails() -> dict:
        return {
            "name": "Telegram Conector",
            "description": "Permite obtener notificaciones a través de Telegram",
            "meta": {}
        }

    async def notify(data, options={}) -> dict or None:

        body = {
            "chat_id": data['subscription_data']['chat_id'],
            "text": data['message']["title"] + "\n" + data['message']["body"]
        }

        bot_token = data['subscription_data']['bot_token']

        headers = {
            "Content-Type": "application/json"
        }

        endpoint = f'https://api.telegram.org/bot{bot_token}/sendMessage'

        res = requests.post(endpoint, json=body, headers=headers)
        if not res.ok:
            return res.json()["description"]
        return None

    def get_subscription_serializer():
        return SubcriptionDataTelegram
