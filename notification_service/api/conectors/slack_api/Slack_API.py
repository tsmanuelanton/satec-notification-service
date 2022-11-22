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

    def notify(data) -> bool:

        try:
            body = {
                "channel": data['subscription_data']["channel"],
                "text": data['message']["body"],
            }

            headers = {
                "Authorization": f"Bearer " + data['subscription_data']["token"]
            }
            res = requests.post("https://slack.com/api/chat.postMessage",
                                json=body, headers=headers)
            if not res.ok:
                print(res.json())
                return res.json()

        except BaseException as e:
            print(e)
            raise e
        return True

    def get_subscription_serializer():
        return SubcriptionDataSlack
