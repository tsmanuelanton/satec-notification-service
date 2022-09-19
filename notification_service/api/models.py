from django.db import models


class Service(models.Model):
    service_name = models.CharField(max_length=60)
    token = models.CharField(max_length=45, unique=True)


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
    token = models.ForeignKey(
        Service, to_field="token", on_delete=models.CASCADE)
