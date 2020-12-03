from django.db import models
from netfields import InetAddressField, NetManager
import ipaddress
from django.core.validators import RegexValidator

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
    network = models.CharField(max_length=50, validators=[RegexValidator(
        regex='^(([1-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.)(([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){2}([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\/([1-9]|[1-2]\d|3[0-2])$',
        message='Неверный формат сети',
        code='invalid network'
    )])
    network_binary = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, null=True, blank=False, verbose_name='Дескрипшн')
    trash_image = models.CharField(max_length=100, default='/static/Photo/Trash2.png')

    class Meta:
        ordering = ('network_binary',)
        verbose_name = 'Class network'

    def save(self, *args, **kwargs):
        super(ClassNetwork, self).save(*args, **kwargs)
        #Блок проверки от промаха
        network_data = self.network
        correct_network_data_raw = ipaddress.ip_interface(network_data)
        correct_network_data = correct_network_data_raw.network
        self.network = correct_network_data

        #Переменные
        current_object = ClassNetwork.objects.get(id=self.id)
        network = ipaddress.IPv4Network(self.network)
        subnet = ipaddress.ip_network(self.network)
        ip_adresses = list(subnet.hosts())

        #Блок создание идентификатор для сортировки сетей
        for address in network:
            network_binary = bin(int(address))
            finaly_network_bynary = int(network_binary, 2)
            self.network_binary = finaly_network_bynary
            break

        super().save(*args, **kwargs)



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
    network = models.CharField(max_length=50, verbose_name='Сеть', validators=[RegexValidator(
        regex='^(([1-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.)(([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){2}([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\/([1-9]|[1-2]\d|3[0-2])$',
        message='Неверный формат сети',
        code='invalid network'
    )])
    network_binary = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Описание')
    region_reletionship = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион')
    vlan_reletionship = models.ForeignKey(VLAN, on_delete=models.SET_NULL, null=True, blank=True,
                                             verbose_name='VLAN')
    classNetwork_reletionship = models.ForeignKey(ClassNetwork, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Классовая сеть')
    objects = NetManager()

    class Meta:
        ordering = ('network_binary',)
        verbose_name = 'Network'
        unique_together = ('network',)

    def save(self, *args, **kwargs):
        super(Networks, self).save(*args, **kwargs)
        #Блок проверки от промаха
        network_data = self.network
        correct_network_data_raw = ipaddress.ip_interface(network_data)
        correct_network_data = correct_network_data_raw.network
        self.network = correct_network_data

        #Переменные
        current_object = Networks.objects.get(id=self.id)
        network = ipaddress.IPv4Network(self.network)
        subnet = ipaddress.ip_network(self.network)
        ip_adresses = list(subnet.hosts())

        #Блок создание идентификатор для сортировки сетей
        for address in network:
            network_binary = bin(int(address))
            finaly_network_bynary = int(network_binary, 2)
            self.network_binary = finaly_network_bynary
            break
        #Блок создания ip-адресов
        for ip_adress in ip_adresses:
            ip_adress = str(ip_adress)
            adress_object = Adress(ip_address=ip_adress)
            adress_object.network_reletionship = current_object
            adress_object.save()

        super().save(*args, **kwargs)



    def __str__(self):
        return str(self.network)


class VPN (models.Model):
    id = models.AutoField(primary_key=True)
    pool = models.CharField(max_length=50, validators=[RegexValidator(
        regex='^(([1-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.)(([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){2}([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\/([1-9]|[1-2]\d|3[0-2])$',
        message='Неверный формат сети',
        code='invalid network'
    )])
    network_binary = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Описание')
    classNetwork_reletionship = models.ForeignKey(ClassNetwork, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Классовая сеть')

    objects = NetManager()

    class Meta:
        ordering = ('network_binary',)
        verbose_name = 'VPN pool'

 #   def save(self, *args, **kwargs):
 #       super(VPN, self).save(*args, **kwargs)
 #       vpnObject = VPN.objects.get(id=self.id)
 #       subnet = ipaddress.ip_network(self.pool)
 #       for ip in subnet:
 #           ip_address = str(ip)
 #           address_object = Adress(ip_address=ip_address)
 #           address_object.vpnPool_reletionship = vpnObject
 #           address_object.save()
    def save(self, *args, **kwargs):
        super(VPN, self).save(*args, **kwargs)
        #Блок проверки от промаха
        network_data = self.pool
        correct_network_data_raw = ipaddress.ip_interface(network_data)
        correct_network_data = correct_network_data_raw.network
        self.pool = correct_network_data

        #Переменные
        current_object = VPN.objects.get(id=self.id)
        network = ipaddress.IPv4Network(self.pool)
        subnet = ipaddress.ip_network(self.pool)
        ip_adresses = list(subnet.hosts())

        #Блок создание идентификатор для сортировки сетей
        for address in network:
            network_binary = bin(int(address))
            finaly_network_bynary = int(network_binary, 2)
            self.network_binary = finaly_network_bynary
            break
        #Блок создания ip-адресов
        for ip_adress in ip_adresses:
            ip_adress = str(ip_adress)
            adress_object = Adress(ip_address=ip_adress)
            adress_object.vpnPool_reletionship = current_object
            adress_object.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pool)


class PAT (models.Model):
    geokod = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10, null=False, blank=False)


    class Meta:
        ordering = ('geokod',)

    def __str__(self):
        return self.name


class TestDB (models.Model):
    id = models.AutoField(primary_key=True)
    network = models.CharField(max_length=50, validators=[RegexValidator(
        regex='^(([1-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.)(([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){2}([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\/([1-9]|[1-2]\d|3[0-2])$',
        message='Неверный формат сети',
        code='invalid network'
    )])
    network_binary = models.BigIntegerField(blank=True, null=True)

    class Meta:
        ordering = ('network_binary',)


    def save(self, *args, **kwargs):
        super(TestDB, self).save(*args, **kwargs)
        #Блок проверки от промаха
        network_data = self.network
        correct_network_data_raw = ipaddress.ip_interface(network_data)
        correct_network_data = correct_network_data_raw.network
        self.network = correct_network_data

        #Переменные
        current_object = TestDB.objects.get(id=self.id)
        network = ipaddress.IPv4Network(self.network)
        subnet = ipaddress.ip_network(self.network)
        ip_adresses = list(subnet.hosts())

        #Блок создание идентификатор для сортировки сетей
        for address in network:
            network_binary = bin(int(address))
            finaly_network_bynary = int(network_binary, 2)
            self.network_binary = finaly_network_bynary
            break
        #Блок создания ip-адресов
        for ip_adress in ip_adresses:
            ip_adress = str(ip_adress)
            adress_object = Adress(ip_address=ip_adress)
            adress_object.testDB_reletionship = current_object
            adress_object.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.network)


class Adress(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(null=False, blank=False, unique=True)
    network_binary = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, null=True, blank=False)
    network_reletionship = models.ForeignKey(Networks, on_delete=models.CASCADE, null=True, blank=False)
    vpnPool_reletionship = models.ForeignKey(VPN, on_delete=models.CASCADE, null=True, blank=True)
    testDB_reletionship = models.ForeignKey(TestDB, on_delete=models.CASCADE, null=True, blank=False)

    class Meta:
        ordering = ('network_binary',)

    def save(self, *args, **kwargs):
        super(Adress, self).save(*args, **kwargs)

        network = ipaddress.IPv4Network(self.ip_address)

        for address in network:
            network_binary = bin(int(address))
            finaly_network_bynary = int(network_binary, 2)
            self.network_binary = finaly_network_bynary
            break

        super().save(*args, **kwargs)

    def __str__(self):
        return self.ip_address