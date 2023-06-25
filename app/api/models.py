from django.db import models
from django.contrib.auth.models import User

MAX_SERVICE_NAME_LENGTH = 45
MAX_CONECTOR_NAME_LENGTH = 60


class Service(models.Model):
    name = models.CharField(max_length=MAX_SERVICE_NAME_LENGTH)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    meta = models.JSONField(null=True, blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

class Conector(models.Model):
    name = models.CharField(max_length=MAX_CONECTOR_NAME_LENGTH, unique=True)
    description = models.TextField()
    # JSON distinto para campos exclusivos del conector
    meta = models.JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


class SubscriptionGroup(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    meta = models.JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE)
    conector = models.ForeignKey(
        Conector, on_delete=models.CASCADE)
    group = models.ForeignKey(
        SubscriptionGroup, on_delete=models.SET_NULL, null=True)
    subscription_data = models.JSONField()
    meta = models.JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
