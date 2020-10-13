import ipaddress
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Region, Networks, VLAN, Adress, PAT
from .forms import NetworkForm, RegionForm, VlanForm, ipaddressForm, changeNetwork, changeLocationNetwork, changeVlan, changeDescriptionNetwork
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
            form.save()
            messages.success(request, f"Сеть {correct_network_data} успешно создана")
        else:
            messages.error(request, "Не удалось создать сеть")

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

    if "vlanButton" in request.POST:
        form = VlanForm(request.POST)
        vlan_id_inForm = request.POST.get('vlan_id')
        if form.is_valid():
            form.save()
            messages.success(request, f"Успешно создан VLAN {vlan_id_inForm}")
        else:
            messages.error(request, f"Не удалось создать VLAN {vlan_id_inForm}")

    if "trashButton" in request.POST:
        currentVlanID = int(request.POST.get('currentVlanID'))
        VLAN.objects.get(id=currentVlanID).delete()
        messages.success(request, "VLAN успешно удалён")

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
    current_network = current_network_object.network
    current_network_region = current_network_object.region_reletionship
    resetPage = redirect('address', region_id=network_object.region_reletionship_id, network_id=network_id)
    form = ipaddressForm()
    changeNetworkForm = changeNetwork(current_network_object)
    changeLocationForm = changeLocationNetwork()
    changeDescriptionForm = changeDescriptionNetwork()
    changeVlanForm = changeVlan(region_id)

    parametrs = {'address_for_network': address_for_network,
                 'network_object': network_object,
                 'region_id': region_id,
                 'changeNetworkForm': changeNetworkForm,
                 'changeLocationForm': changeLocationForm,
                 'changeDescriptionNetwork': changeDescriptionNetwork,
                 'changeVlanForm': changeVlanForm,
                 'form': form}

    if 'delNetButton' in request.POST:
        network_object.delete()
        messages.success(request, f"Сеть {current_network_object.network} успешно удалена")
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
            messages.success(request, f"Сеть {current_network} успешно переехала на {Region.objects.get(id=newLoaction).name}")
            return resetPage
        else:
            messages.error(request, f"Смена локации сети {current_network} на локацию {current_network_region} не удалась")
            return resetPage

    if 'changeVlanFormSubmit' in request.POST:
        changeVlanForm = changeVlan(region_id, request.POST)
        if changeVlanForm.is_valid():
            newVlan = request.POST['vlan_reletionship']
            current_network_objects.update(vlan_reletionship=newVlan)
            messages.success(request, f"Сети {current_network} успешно назначен VLAN {newVlan}")
            return resetPage
        else:
            messages.error(request, f'Сети {current_network} не удалось назначить VLAN')
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

            messages.success(request, f"Сеть {current_network} изменена на сеть {correct_network_data}")
            return resetPage
        else:
            messages.error(request, f"Не удалось изменить сеть {current_network}")

    if 'changeDescriptionFormSubmit' in request.POST:
        changeDescriptionForm = changeDescriptionNetwork(request.POST)
        if changeDescriptionForm.is_valid():
            newNetworkDescription = request.POST['description']
            current_network_objects.update(description=newNetworkDescription)
            messages.success(request, f'Дескрипшн сети {current_network} успешно изменён')
        else:
            messages.error(request, f'Не удалось сменить дескрипшн сети {current_network}')
    return render(request, 'ip_address_page.html', parametrs)

def all_networks_page(request):
    all_networks = Networks.objects.all()

    parametrs = {'all_networks':all_networks}
    return render(request, 'all_network_page.html', parametrs)

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





