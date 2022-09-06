# satec-notification-service

API desarrollada con Django Rest Framework que permite enviar notificaciones a los usuarios suscritos.

![Esquema del servicio ](Esquema.svg "Esquema del servicio")

Estructura de rutas de la API:

| Endpoint | GET | POST | PUT |DELETE|
| -- | -- | -- | -- | -- |
| `v1/subscriptions` | Listar las suscripciones | Registrar una suscripción | N/A | N/A |
| `v1/subscriptions/id` | N/A | N/A | Actualizar la suscripción | Eliminar suscripción |
| `v1/services` | Listar los servicios | Registrar un nuevo servicio | N/A | N/A
| `v1/services/id` | N/A | N/A | Actualizar servicio | Eliminar servicio
| `v1/notify` | N/A | Enviar mensaje para notificar a los suscriptores | N/A | N/A |