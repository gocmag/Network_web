import ipaddress
from django import forms
from  .models import Networks, Region, VLAN, Adress
from django.core.exceptions import ValidationError

class NetworkForm(forms.ModelForm):

    def __init__(self,region_id,*args,**kwargs):
        super(NetworkForm, self).__init__(*args,**kwargs)
        self.fields['vlan_reletionship'].queryset = VLAN.objects.filter(region_reletionship=region_id)

    def clean_network(self):
        network_object = self.cleaned_data['network']
        all_object_network = Networks.objects.all()
        try:
            received_subnet = ipaddress.ip_network(str(network_object))
        except ValueError:
            correct_network_data_raw = ipaddress.ip_interface(str(network_object))
            received_subnet = correct_network_data_raw.network
        frozen_received_subnet = set(received_subnet)
        for network_in_table in all_object_network:
            subnet_in_table = ipaddress.ip_network(str(network_in_table))
            frozen_subnet_in_table = set(subnet_in_table)
            difference = frozen_received_subnet & frozen_subnet_in_table
            if not difference:
                print('Значение пустое')
            if difference:
                print('Значение не пустое')
                raise ValidationError(f'Сеть пересекается с сетью {network_in_table}')
        return network_object


    class Meta:
        model = Networks
        fields = '__all__'


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'

class VlanForm(forms.ModelForm):
    class Meta:
        model = VLAN
        fields = '__all__'

class ipaddressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = ['description',]
        labels = {"description":""}

class changeNetwork(forms.ModelForm):
    class Meta:
        model = Networks
        fields = ['network',]
        labels = {'network':''}

class changeLocationNetwork(forms.ModelForm):
    class Meta:
        model = Networks
        fields = ['region_reletionship',]
        labels = {'region_reletionship':''}



