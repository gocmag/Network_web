import ipaddress
from django.core.exceptions import ValidationError
#from .models import Networks


def validate(region_id, network_object, all_object_network):
   # all_object_network = Networks.objects.all()
    received_subnet = ipaddress.ip_network(str(network_object))
    frozen_received_subnet = set(received_subnet)

    for network_in_table in all_object_network:
        subnet_in_table = ipaddress.ip_network(str(network_in_table))
        frozen_subnet_in_table = set(subnet_in_table)
        difference = frozen_received_subnet & frozen_subnet_in_table
        if not difference:
            print('Значение пустое')
        if difference:
           raise ValidationError('сети пересекаються')
         #  print('Значение не пустое')







