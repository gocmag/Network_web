from django.contrib import admin
from .models import Networks, Region, VLAN, PAT, VPN, ClassNetwork

admin.site.register([Region, Networks, VLAN, PAT, VPN, ClassNetwork])

# Register your models here.
