from django.db import models


class Service(models.Model):
    service_name = models.CharField(max_length=60)


class Subscription(models.Model):
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    subscription_data = models.JSONField()
