import ipaddress
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Region, Networks, VLAN, Adress, PAT
from .forms import NetworkForm, RegionForm, VlanForm, ipaddressForm, changeNetwork, changeLocationNetwork, changeVlan
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def choise_page(request, region_id):
    return render(request, 'choise_page.html',{'region_id':region_id})

@login_required(login_url='/accounts/login/')
def networking(request, region_id):
    networks = Networks.objects.all().order_by('network')
    networks_for_region = Networks.objects.filter(region_reletionship=region_id)
    region_object = Region.objects.get(id=region_id)
    form = NetworkForm(region_id, initial={'region_reletionship':region_object})

    if request.method == 'POST':
        form = NetworkForm(region_id, request.POST)
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
                'region_object':region_object,
                'form': form,
                }

    return render(request, 'Network_page.html', parametrs)

@login_required(login_url='/accounts/login/')
def vlans(request, region_id):
    vlans_for_region = VLAN.objects.filter(region_reletionship=region_id)
    region_object = Region.objects.get(id=region_id)
    form = VlanForm(initial={'region_reletionship':region_object})
    parametrs = {
        'vlans_for_region':vlans_for_region,
        'form':form,
        'region_id':region_id,
        'region_object':region_object
                }

    if request.method == 'POST':
        form = VlanForm(request.POST)
        if form.is_valid():
            form.save()

    if "trashButton" in request.POST:
        currentVlanID = int(request.POST.get('currentVlanID'))
        VLAN.objects.get(id=currentVlanID).delete()

    return render(request, 'vlans_page.html', parametrs)


@login_required(login_url='/accounts/login/')
def region(request):
    regions_core = Region.objects.filter(region_type='core')
    regions_pat = Region.objects.filter(region_type='pat')
    regions_other = Region.objects.filter(region_type='other')
    regions_geokod = PAT.objects.all()
    form = RegionForm()
    parametrs = {
        'regions_core': regions_core,
        'regions_pat': regions_pat,
        'regions_other': regions_other,
        'regions_geokod': regions_geokod,
        'form': form
    }
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'region_page.html', parametrs)

@login_required(login_url='/accounts/login/')
def address(request, region_id, network_id):
    network_object = Networks.objects.get(id=network_id)
    current_network_objects = Networks.objects.filter(id=network_id)
    current_network_object = Networks.objects.get(id=network_id)
    address_for_network = Adress.objects.filter(network_reletionship=network_id)
    resetPage = redirect('address', region_id=network_object.region_reletionship_id, network_id=network_id)
    form = ipaddressForm()
    changeNetworkForm = changeNetwork(current_network_object)
    changeLocationForm = changeLocationNetwork()
    changeVlanForm = changeVlan(region_id)

    parametrs = {'address_for_network': address_for_network,
                 'network_object': network_object,
                 'region_id': region_id,
                 'changeNetworkForm': changeNetworkForm,
                 'changeLocationForm': changeLocationForm,
                 'changeVlanForm': changeVlanForm,
                 'form': form}

    if 'delNetButton' in request.POST:
        network_object.delete()
        return redirect('network', region_id=region_id)
    if request.method == 'POST' and 'Test' in request.POST:
        result = request.POST['Test']
        form = ipaddressForm(request.POST)
        if form.is_valid():
            new_description = form.cleaned_data.get('description')
            Adress.objects.filter(id=result).update(description=new_description)

    if 'changeLocationFormSubmit' in request.POST:
        changeLocationForm = changeLocationNetwork(request.POST)
        if changeLocationForm.is_valid():
            newLoaction = request.POST['region_reletionship']
            current_network_objects.update(region_reletionship=newLoaction)
            return resetPage

    if 'changeVlanFormSubmit' in request.POST:
        changeVlanForm = changeVlan(region_id, request.POST)
        if changeVlanForm.is_valid():
            newVlan = request.POST['vlan_reletionship']
            current_network_objects.update(vlan_reletionship=newVlan)
            return resetPage

    if 'changeNetworkFormSubmit' in request.POST:
        changeNetworkForm = changeNetwork(current_network_object, request.POST)
        if changeNetworkForm.is_valid():
            new_network = request.POST['network']
            correct_network = changeNetworkForm.save(commit=False)
            network_data = changeNetworkForm.cleaned_data.get('network')
            correct_network_data_raw = ipaddress.ip_interface(network_data)
            correct_network_data = correct_network_data_raw.network
            correct_network.network = correct_network_data

            current_network_objects.update(network=correct_network_data)
            return resetPage
          #  changeNetworkForm.save()

    return render(request, 'ip_address_page.html', parametrs)

@login_required(login_url='/accounts/login/')
def from_vlan_to_address (request,region_id,vlan_id):
    network_object = Networks.objects.get(region_reletionship=region_id, vlan_reletionship=vlan_id)
    return redirect('address', region_id=region_id, network_id=network_object.id)

@login_required(login_url='/accounts/login/')
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


    parametrs = {
        'searchNetworkResult':searchNetworkResult,
        'searchVLANResult':searchVLANResult,
        'searchAdressResult':searchAdressResult
    }

    return render(request, 'search_page.html', parametrs)





