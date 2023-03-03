from api.conectors.IConector import IConector
import requests
from .serilizers import SubcriptionDataSlack


class SlackAPIConector(IConector):
    def getDetails():
        return {
            "name": "Slack API",
            "description": "Permite obtener notificaciones por tu chat de Slack",
            "meta": {
            }
        }

    def notify(data, meta={}) -> bool:

        body = {
            "channel": data['subscription_data']["channel"],
            "text": data['message']["title"] + "\n" + data['message']["body"],
            **meta
        }

        headers = {
            "Authorization": "Bearer " + data['subscription_data']["token"]
        }
        res = requests.post("https://slack.com/api/chat.postMessage",
                            json=body, headers=headers)
        res_json = res.json()
        if not res_json.get("ok", False):
            return False, {"description": {res_json.get("error"), res_json.get("warning")}}
        return True, {}

    def get_subscription_serializer():
        return SubcriptionDataSlack
