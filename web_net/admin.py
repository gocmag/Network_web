from django.contrib import admin
from .models import Networks, Region, VLAN, PAT, VPN, ClassNetwork, TestDB, Adress

admin.site.register([Region, Adress])

# Register your models here.
