from api.conectors.IConector import IConector
import requests
from .serializers import SubcriptionDataTelegram


class TelegramConector(IConector):
    def getDetails():
        return {
            "name": "Telegram Conector",
            "description": "Permite obtener notificaciones a través de Telegram",
            "meta": {}
        }

    def notify(data, meta={}) -> bool:

        try:
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
                print(res.json())
            return res.json()

        except BaseException as e:
            print(e)
            raise e
        return True

    def get_subscription_serializer():
        return SubcriptionDataTelegram
