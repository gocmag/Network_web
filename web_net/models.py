from django.db import models
from netfields import InetAddressField, NetManager
import ipaddress

class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, verbose_name='Имя региона')

    class Meta:
        verbose_name = 'Region'

    def __str__(self):
        return self.name



class VLAN(models.Model):
    id = models.AutoField(primary_key=True)
    vlan_id = models.IntegerField(verbose_name='VLAN')
    description = models.CharField(max_length=100, verbose_name='Описание', null=True, blank=True)
    region_reletionship = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион')

    class Meta:
        ordering = ('vlan_id',)
        verbose_name = 'VLAN'

    def __str__(self):
        return str(self.vlan_id)



class Networks(models.Model):
    id = models.AutoField(primary_key=True)
    network = InetAddressField(null=False, verbose_name='Сеть')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Описание')
    region_reletionship = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион')
    vlan_reletionship = models.ForeignKey(VLAN, on_delete=models.SET_NULL, null=True, blank=True,
                                             verbose_name='VLAN')
    objects = NetManager()

    class Meta:
        ordering = ('network',)
        verbose_name = 'Network'

    def __str__(self):
        return str(self.network)

    def save(self,*args,**kwargs):
        super(Networks, self).save(*args,**kwargs)
        network_object = Networks.objects.get(id=self.id)
        subnet = ipaddress.ip_network(self.network)
        ip_adresses = list(subnet.hosts())
        for ip_adress in ip_adresses:
            ip_adress = str(ip_adress)
            adress_object = Adress(ip_address=ip_adress)
            adress_object.network_reletionship = network_object
            adress_object.save()


class Adress(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    network_reletionship = models.ForeignKey(Networks, on_delete=models.CASCADE, null=False, blank=False)
    arrow_image = models.CharField(max_length=100, default='/static/Photo/Arrow.png')

    def __str__(self):
        return self.ip_address


class Tunnels(models.Model):
    id = models.AutoField(primary_key=True)
    firstTunnelName = models.CharField(max_length=30, null=False, blank=False)
    firstTunnelPhisicalAddress = models.GenericIPAddressField(null=False, blank=False)
    firstTunnelNetworkAddress = models.GenericIPAddressField(null=False, blank=False)
    secondTunnelName = models.CharField(max_length=30, null=False, blank=False)
    secondTunnelPhisicalAddress = models.GenericIPAddressField(null=False, blank=False)
    secondTunnelNetworkAddress = models.GenericIPAddressField(null=False, blank=False)

    class Meta:
        ordering = ('firstTunnelPhisicalAddress', 'secondTunnelPhisicalAddress')
