from django.contrib import admin
from .models import Networks, Region, VLAN, PAT, VPN

admin.site.register([Networks, Region, VLAN, PAT, VPN])

# Register your models here.
