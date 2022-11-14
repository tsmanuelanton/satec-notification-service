[![Tests](https://github.com/manuel-anton-satec/satec-notification-service/actions/workflows/run_tests.yml/badge.svg)](https://github.com/manuel-anton-satec/satec-notification-service/actions/workflows/run_tests.yml)

# satec-notification-service

Servicio que permite registrar usarios para enviarles notificaciones/mensajes a través de múltiples plataformas.

![Esquema del servicio ](Esquema.svg "Esquema del servicio")

El sistema ofrece una API desarrollada con Django Rest Framework para gestionar las suscripciones, ver plataformas disponibles o añadir aplicaciones que generen notificaciones.

### Plataformas disponibles

El servicio ofrece, actualmente, los siguientes medios para recibir las notificaciones/mensajes.

>- **Navegador web**: Los suscriptores de esta plataforma reciben los mensajes en su navegador web gracias a la tecnología web [Push API](https://developer.mozilla.org/es/docs/Web/API/Push_API).


### Rutas de la API

| Endpoint | GET | POST | PUT |DELETE|
| -- | -- | -- | -- | -- |
| `v1/subscriptions` | Listar las suscripciones | Registrar una suscripción | N/A | N/A |
| `v1/subscriptions/id` | N/A | N/A | Actualizar la suscripción | Eliminar suscripción |
| `v1/services` | Listar los servicios | Registrar un nuevo servicio | N/A | N/A
| `v1/services/id` | N/A | N/A | Actualizar servicio | Eliminar servicio
| `v1/conectors` | Muestra los conectores disponibles | N/A | N/A | N/A
| `v1/notifications` | N/A | Enviar mensaje para notificar a los suscriptores | N/A | N/A |

### Instalación

Creamos un directorio e inicilizamos un entorno virtual de python dentro.
Depués, ejecutamos los siguientes comandos
```
git clone https://github.com/manuel-anton-satec/satec-notification-service`git
cd satec-notification-service
pip install -r requirements.txt
cd notification_service
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```