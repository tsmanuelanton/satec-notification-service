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

            tenant_id = data['subscription_data']['tenant_id']
            client_id = data['subscription_data']['client_id']
            email = data['subscription_data']['email']
            password = data['subscription_data']['password']

            token = TeamsConector.get_token(
                email, password, client_id,  tenant_id)

            headers = {
                "Authorization": "Bearer " + token,
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

    # https://learn.microsoft.com/en-us/graph/auth/auth-concepts
    def get_token(email: str, password: str, client_id: str, tenant_id: str):
        '''Obtiene token de acceso mediante autenticación por usario y contraseña'''

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        body = {
            "client_id": client_id,
            "scope": "https://graph.microsoft.com/.default",
            "username": email,
            "password": password,
            "grant_type": "password"
        }

        url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        res = requests.post(url, body, headers=headers)

        if res.ok:
            return res.json().get("access_token")

        raise BaseException(res.json())
