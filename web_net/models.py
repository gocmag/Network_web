from django.db import models
from netfields import InetAddressField, NetManager
import ipaddress

class Region(models.Model):
    region_type = [
        ('core', 'Ядро'),
        ('pat', 'ПАТ')
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, verbose_name='Имя региона')
    region_type = models.CharField(max_length=10, blank=False, choices=region_type)
    geokod = models.IntegerField(blank=True)

    class Meta:
        verbose_name = 'Region'
        ordering = ('geokod',)

    def __str__(self):
        return self.name


class ClassNetwork(models.Model):
    id = models.AutoField(primary_key=True)
    network = InetAddressField(null=False, unique=True, verbose_name='Сеть')
    description = models.CharField(max_length=200, null=True, blank=False, verbose_name='Дескрипшн')
    trash_image = models.CharField(max_length=100, default='/static/Photo/Trash2.png')

    class Meta:
        ordering = ('network',)
        verbose_name = 'Class network'

    def __str__(self):
        return str(self.network)



class VLAN(models.Model):
    id = models.AutoField(primary_key=True)
    vlan_id = models.IntegerField(verbose_name='VLAN')
    description = models.CharField(max_length=100, verbose_name='Описание', null=True, blank=True)
    trash_image = models.CharField(max_length=100, default='/static/Photo/Trash2.png')
    region_reletionship = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион')

    class Meta:
        ordering = ('vlan_id',)
        verbose_name = 'VLAN'
        unique_together = ('vlan_id', 'region_reletionship')

    def __str__(self):
        return str(self.vlan_id)



class Networks(models.Model):
    id = models.AutoField(primary_key=True)
    network = InetAddressField(null=False, unique=True, verbose_name='Сеть')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Описание')
    region_reletionship = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион')
    vlan_reletionship = models.ForeignKey(VLAN, on_delete=models.SET_NULL, null=True, blank=True,
                                             verbose_name='VLAN')
    classNetwork_reletionship = models.ForeignKey(ClassNetwork, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Классовая сеть')
    objects = NetManager()

    class Meta:
        ordering = ('network',)
        verbose_name = 'Network'
        unique_together = ('network',)

    def __str__(self):
        return str(self.network)

    def save(self, *args, **kwargs):
        super(Networks, self).save(*args, **kwargs)
        network_object = Networks.objects.get(id=self.id)
        subnet = ipaddress.ip_network(self.network)
        ip_adresses = list(subnet.hosts())
        for ip_adress in ip_adresses:
            ip_adress = str(ip_adress)
            adress_object = Adress(ip_address=ip_adress)
            adress_object.network_reletionship = network_object
            adress_object.save()



class VPN (models.Model):
    id = models.AutoField(primary_key=True)
    pool = InetAddressField(null=False, unique=True, verbose_name='Пул')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Описание')
    classNetwork_reletionship = models.ForeignKey(ClassNetwork, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Классовая сеть')

    objects = NetManager()

    class Meta:
        ordering = ('pool',)
        verbose_name = 'VPN pool'

    def save(self, *args, **kwargs):
        super(VPN, self).save(*args, **kwargs)
        vpnObject = VPN.objects.get(id=self.id)
        subnet = ipaddress.ip_network(self.pool)
        for ip in subnet:
            ip_address = str(ip)
            address_object = Adress(ip_address=ip_address)
            address_object.vpnPool_reletionship = vpnObject
            address_object.save()

    def __str__(self):
        return str(self.pool)


class Adress(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(null=False, blank=False, unique=True)
    description = models.CharField(max_length=200, null=True, blank=False)
    network_reletionship = models.ForeignKey(Networks, on_delete=models.CASCADE, null=True, blank=False)
    vpnPool_reletionship = models.ForeignKey(VPN, on_delete=models.CASCADE, null=True, blank=True)
    arrow_image = models.CharField(max_length=100, default='/static/Photo/Arrow.png')

    class Meta:
        ordering = ('ip_address',)

    def __str__(self):
        return self.ip_address



class PAT (models.Model):
    geokod = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10, null=False, blank=False)


    class Meta:
        ordering = ('geokod',)

    def __str__(self):
        return self.name

