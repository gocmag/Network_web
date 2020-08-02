from django.contrib import admin
from .models import Networks, Region, VLAN, PAT, Tunnels

admin.site.register([Networks,Region,VLAN, PAT, Tunnels])

# Register your models here.
