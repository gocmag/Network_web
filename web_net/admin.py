from django.contrib import admin
from .models import Networks, Region, VLAN, PAT, VPN, ClassNetwork, TestDB

admin.site.register([TestDB,])

# Register your models here.
