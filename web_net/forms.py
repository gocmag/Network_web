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
        print(frozen_received_subnet)
        for network_in_table in all_object_network:
            subnet_in_table = ipaddress.ip_network(str(network_in_table))
            frozen_subnet_in_table = set(subnet_in_table)
            difference = frozen_received_subnet & frozen_subnet_in_table
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
    def __init__(self,current_network_object,*args,**kwargs):
        super(changeNetwork, self).__init__(*args,**kwargs)
        self.old_nentwork = current_network_object

    def clean_network(self):
        network_object = self.cleaned_data['network']
        all_object_network = Networks.objects.all()
        current_network_object = self.old_nentwork
        old_subnet = self.old_nentwork
        all_old_address_network = Adress.objects.filter(network_reletionship=old_subnet.id)
        dict_old_addressDescription = {}
        try:
            new_subnet = ipaddress.ip_network(str(network_object))
        except ValueError:
            correct_network_data_raw_new = ipaddress.ip_interface(str(network_object))
            new_subnet = correct_network_data_raw_new.network

        try:
            old_subnet = ipaddress.ip_network(str(old_subnet))
        except ValueError:
            correct_network_data_raw_old = ipaddress.ip_interface(str(old_subnet))
            old_subnet = correct_network_data_raw_old.network

        all_new_ipAdress = set(new_subnet)
        all_old_ipAdress = set(old_subnet)

        diff_ipAddress = all_new_ipAdress.difference(all_old_ipAdress)
        same_ipAddress = all_new_ipAdress & all_old_ipAdress

        for network_in_table in all_object_network:
            if str(network_in_table) == str(old_subnet):
                continue
            subnet_in_table = ipaddress.ip_network(str(network_in_table))
            frozen_subnet_in_table = set(subnet_in_table)
            difference = all_new_ipAdress & frozen_subnet_in_table
            if difference:
                print(f'Сеть пересекается с сетью {network_in_table}')
                raise ValidationError(f'Сеть пересекается с сетью {network_in_table}')


            for old_address in all_old_address_network:
                if type(old_address.description) != type(None):
                    dict_old_addressDescription[old_address.ip_address] = old_address.description

        all_old_address_network.delete()
        new_ip_adresses = list(new_subnet.hosts())
        for ip_adress in new_ip_adresses:
            ip_adress = str(ip_adress)
            adress_object = Adress(ip_address=ip_adress)
            adress_object.network_reletionship = current_network_object
            if ip_adress in dict_old_addressDescription:
                adress_object.description = dict_old_addressDescription.pop(ip_adress)
            adress_object.save()

        return network_object

    class Meta:
        model = Networks
        fields = ['network',]
        labels = {'network':''}




class changeLocationNetwork(forms.ModelForm):

    class Meta:
        model = Networks
        fields = ['region_reletionship',]
        labels = {'region_reletionship':''}

class changeVlan(forms.ModelForm):
    def __init__(self,region_id,*args,**kwargs):
        super(changeVlan, self).__init__(*args,**kwargs)
        self.fields['vlan_reletionship'].queryset = VLAN.objects.filter(region_reletionship=region_id)


    class Meta:
        model = Networks
        fields = ['vlan_reletionship',]
        labels = {'vlan_reletionship':''}



