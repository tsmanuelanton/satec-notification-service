from api.conectors.IConector import IConector
from .serilizers import SubcriptionDataSlack

import requests

class SlackAPIConector(IConector):
    def getDetails() -> dict:
        return {
            "name": "Slack API",
            "description": "Permite obtener notificaciones por tu chat de Slack",
            "meta": {
            }
        }

    async def notify(data, options={}) -> dict or None:

        body = {
            "channel": data['subscription_data']["channel"],
            "text": data['message']["title"] + "\n" + data['message']["body"],
            **options
        }

        headers = {
            "Authorization": "Bearer " + data['subscription_data']["token"]
        }
        res = requests.post("https://slack.com/api/chat.postMessage",
                            json=body, headers=headers)
        res_json = res.json()
        if not res_json.get("ok", False):
            return [res_json.get("error"), res_json.get("warning")]
        return None

    def get_subscription_serializer():
        return SubcriptionDataSlack
