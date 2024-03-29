from api.conectors.IConector import IConector
import requests
from .serializers import SubcriptionDataTeams


class TeamsConector(IConector):
    def getDetails() -> dict:
        return {
            "name": "Microsoft Teams Conector",
            "description": "Permite obtener notificaciones a través de Microsoft Teams",
            "meta": {}
        }

    async def notify(data, options={}) -> dict or None:

        body = {
            "body": {
                "content": data['message']["title"] + "\n" + data['message']["body"]
            },
            **options
        }

        tenant_id = data['subscription_data']['tenant_id']
        client_id = data['subscription_data']['client_id']
        email = data['subscription_data']['email']
        password = data['subscription_data']['password']

        res_token = TeamsConector.get_token(
            email, password, client_id,  tenant_id)
        if not res_token.ok:
            return False, {"description": res_token.json()}

        token = res_token.json()

        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }

        team_id = data['subscription_data']['team_id']
        channel_id = data['subscription_data']['channel_id']
        endpoint = f'https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages'

        res = requests.post(endpoint, json=body, headers=headers)
        if not res.ok:
            res_json = res.json()
            error = res_json.get("error")
            if error:
                return {"description": error["message"]}

        return None

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
        return res
