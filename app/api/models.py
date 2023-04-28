from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class Service(models.Model):
    name = models.CharField(max_length=60)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Conector(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    # JSON distinto para campos exclusivos del conector
    meta = models.JSONField(blank=True, default=dict)


class Subscription(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE)
    conector = models.ForeignKey(
        Conector, on_delete=models.CASCADE)
    subscription_data = models.JSONField()
    meta = models.JSONField(blank=True, default=dict)
