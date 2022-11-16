from api.conectors.IConector import IConector
import requests


class SlackAPIConector(IConector):
    def getDetails():
        return {
            "name": "Slack API",
            "description": "Permite obtener notificaciones por tu chat de Slack",
            "meta": {
            }
        }

    def notify(data) -> bool:

        # TODO validar campos del data

        try:
            body = {
                "channel": data['subscription_data']["channel"],
                "text": data['message']
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
        pass
