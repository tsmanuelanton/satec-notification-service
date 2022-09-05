from django.db import models


class Subscriptions(models.Model):
    service_id = models.CharField(max_length=30)
    subscription_data = models.JSONField()
