from api.conectors.IConector import IConector
from rest_framework.serializers import Serializer
from email.message import EmailMessage
from .serializers import SubcriptionDataEmail
import aiosmtplib

class EmailConector(IConector):
    '''Implementa la interfaz IConector para permitir enviar emails.'''

    def getDetails() -> dict:
        return {
            'name': 'Email Conector',
            'description': 'Permite obtener notificaciones en tu bandeja de correos.'
        }

    async def notify(data, options={}) -> dict:
        email = EmailMessage()
        email['From'] = data['subscription_data']['From']
        email['To'] = data['subscription_data']['To']
        email['Subject'] = data['message']['title']
        content = data['message']['body']
        email.set_content(content)

        smtp_host = data['subscription_data'].get('smtp_host', "localhost")
        port = data['subscription_data'].get('port', 0)
        smtp = aiosmtplib.SMTP(smtp_host, port)
        await smtp.connect()

        if smtp_host != "localhost":
            await smtp.login(data['subscription_data']["user"],
                       data['subscription_data']["password"])

        res = await smtp.sendmail(email['From'], email['To'], email.as_string())
        return res[0]

    def get_subscription_serializer() -> Serializer:
        return SubcriptionDataEmail
