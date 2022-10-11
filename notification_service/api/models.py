from django.db import models
from rest_framework.authtoken.models import Token


class Service(models.Model):
    service_name = models.CharField(max_length=60)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)


class Conector(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    # JSON distinto para campos exclusivos del conector
    meta = models.JSONField()


class Subscription(models.Model):
    service_id = models.ForeignKey(
        Service, related_name="service_id", on_delete=models.CASCADE)
    conector_id = models.ForeignKey(Conector, on_delete=models.CASCADE)
    subscription_data = models.JSONField()
