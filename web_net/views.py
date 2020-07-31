import ipaddress
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Region, Networks, VLAN, Adress
from .forms import NetworkForm, RegionForm, VlanForm, ipaddressForm

def choise_page(request, region_id):
    return render(request, 'choise_page.html',{'region_id':region_id})

def networking(request, region_id):
    networks = Networks.objects.all().order_by('network')
    networks_for_region = Networks.objects.filter(region_reletionship=region_id)
    region_object = Region.objects.get(id=region_id)

    form = NetworkForm(initial={'region_reletionship':region_object})

    if request.method == 'POST':
        form = NetworkForm(request.POST)
        if form.is_valid():
            correct_network = form.save(commit=False)
            network_data = form.cleaned_data.get('network')
            correct_network_data_raw = ipaddress.ip_interface(network_data)
            correct_network_data = correct_network_data_raw.network
            correct_network.network = correct_network_data
            print(correct_network_data)

            form.save()

    parametrs = {
                'networks':networks,
                'networks_for_region':networks_for_region,
                'region_id':region_id,
                'form': form
                }

    return render(request, 'Network_page.html', parametrs)

def vlans(request, region_id):
    vlans_for_region = VLAN.objects.filter(region_reletionship=region_id)
    region_object = Region.objects.get(id=region_id)
    form = VlanForm(initial={'region_reletionship':region_object})
    parametrs = {
        'vlans_for_region':vlans_for_region,
        'form':form,
        'region_id':region_id,
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

def from_vlan_to_address (request,region_id,vlan_id):
    network_object = Networks.objects.get(region_reletionship=region_id,vlan_reletionship=vlan_id)
    return redirect('address', region_id=region_id,network_id=network_object.id)

def search_view(request):
    q = request.GET.get('q', None)
    searchNetworkResult = Networks.objects.filter(
        Q(description__icontains=q) | Q(network__icontains=q)
    )
    searchVLANResult = VLAN.objects.filter(
        Q(description__icontains=q) | Q(vlan_id__icontains=q)
    )

    searchAdressResult = Adress.objects.filter(
        Q(description__icontains=q) | Q(ip_address__icontains=q)
    )

    print(searchVLANResult)
    parametrs = {
        'searchNetworkResult':searchNetworkResult,
        'searchVLANResult':searchVLANResult,
        'searchAdressResult':searchAdressResult
    }

    return render(request, 'search_page.html', parametrs)





