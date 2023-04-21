from api.conectors.IConector import IConector
from rest_framework.serializers import Serializer
from email.message import EmailMessage
from .serializers import SubcriptionDataEmail
import smtplib


class EmailConector(IConector):
    '''Implementa la interfaz IConector para permitir enviar emails.'''

    def getDetails():
        return {
            'name': 'Email Conector',
            'description': 'Permite obtener notificaciones en tu bandeja de correos.'
        }

    def notify(data, meta={}):
        email = EmailMessage()
        email['From'] = data['subscription_data']['From']
        email['To'] = data['subscription_data']['To']
        email['Subject'] = data['subscription_data']['Subject']
        content = data['message']['title'] + '\n' + data['message']['body']
        email.set_content(content)

        smtp_host = data['subscription_data'].get('smtp_host', "localhost")
        port = data['subscription_data'].get('port', 0)
        smtp = smtplib.SMTP(smtp_host, port, timeout=10)

        if smtp_host != "localhost":
            smtp.starttls()
            smtp.login(data['subscription_data']["user"],
                       data['subscription_data']["password"])

        smtp.sendmail(email['From'], email['To'], email.as_string())
        return True, None

    def get_subscription_serializer() -> Serializer:
        return SubcriptionDataEmail
