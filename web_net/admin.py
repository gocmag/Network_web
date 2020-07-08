from django.contrib import admin
from .models import Networks, Region, VLAN

admin.site.register([Networks,Region,VLAN])

# Register your models here.
