from django.shortcuts import render, redirect
from .models import Region, Networks, VLAN, Adress
from .forms import NetworkForm, RegionForm, VlanForm, ipaddressForm

def choise_page(request, region_id):
    return render(request, 'choise_page.html',{'region_id':region_id})

def networking(request, region_id):
    networks = Networks.objects.all().order_by('network')
    networks_for_region = Networks.objects.filter(region_reletionship=region_id)
    form = NetworkForm()
    parametrs = {
                'networks':networks,
                'networks_for_region':networks_for_region,
                'region_id':region_id,
                'form': form
                }
    if request.method == 'POST':
        form = NetworkForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'Network_page.html', parametrs)

def vlans(request, region_id):
    vlans_for_region = VLAN.objects.filter(region_reletionship=region_id)
    form = VlanForm
    parametrs = {
        'vlans_for_region':vlans_for_region,
        'form':form
                }

    if request.method == 'POST':
        form = VlanForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'vlans_page.html', parametrs)

def region(request):
    regions = Region.objects.all()
    form = RegionForm()
    parametrs = {
        'regions': regions,
        'form': form
    }
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'region_page.html', parametrs)

def address(request, region_id, network_id):
    network_object = Networks.objects.get(id=network_id)
    address_for_network = Adress.objects.filter(network_reletionship=network_id)
    form = ipaddressForm()

    parametrs = {'address_for_network': address_for_network, 'form':form}
    if 'delNetButton' in request.POST:
        print("Получен запрос")
        network_object.delete()
        return redirect('network', region_id=region_id)
    if request.method == 'POST' and 'Test' in request.POST:
        result = request.POST['Test']
        form = ipaddressForm(request.POST)
        if form.is_valid():
            new_description = form.cleaned_data.get('description')
            Adress.objects.filter(id=result).update(description=new_description)



    return render(request, 'ip_address_page.html', parametrs)


