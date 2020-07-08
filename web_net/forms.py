from django import forms
from  .models import Networks, Region, VLAN, Adress


class NetworkForm(forms.ModelForm):
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