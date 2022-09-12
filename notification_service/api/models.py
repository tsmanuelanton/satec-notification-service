from django.db import models


class Service(models.Model):
    service_name = models.CharField(max_length=60)


class Conector(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    # JSON distinto para campos exclusivos del conector
    meta = models.JSONField()


class Subscription(models.Model):
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    conector_id = models.ForeignKey(Conector, on_delete=models.CASCADE)
    subscription_data = models.JSONField()
