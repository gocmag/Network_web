from django.db import models
from netfields import InetAddressField, NetManager
from django.utils import timezone

class Networks(models.Model):
    id = models.AutoField(primary_key=True)
    network = InetAddressField()
    description = models.CharField(max_length=200, null=True)
    vlan = models.IntegerField(null=True)

    def __str__(self):
        return self.network
