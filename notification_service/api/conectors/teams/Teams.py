from api.conectors.IConector import IConector
import requests
from .serializers import SubcriptionDataTeams


class TeamsConector(IConector):
    def getDetails():
        return {
            "name": "Microsoft Teams Conector",
            "description": "Permite obtener notificaciones a través de Microsoft Teams",
            "meta": {}
        }

    def notify(data, meta={}) -> bool:

        try:
            body = {
                "body": {
                    "content": data['message']["title"] + "\n" + data['message']["body"]
                },
                **meta
            }

            headers = {
                "Authorization": "Bearer " + data['subscription_data']["token"],
                "Content-Type": "application/json"
            }

            team_id = data['subscription_data']['team_id']
            channel_id = data['subscription_data']['channel_id']
            endpoint = f'https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages'

            res = requests.post(endpoint, json=body, headers=headers)
            if not res.ok:
                print(res.json())
                return res.json()

        except BaseException as e:
            print(e)
            raise e
        return True

    def get_subscription_serializer():
        return SubcriptionDataTeams
