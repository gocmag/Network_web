import ipaddress
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Region, Networks, VLAN, Adress, PAT, VPN, ClassNetwork
from .forms import NetworkForm, RegionForm, VlanForm, ipaddressForm, changeNetwork, changeLocationNetwork, \
    changeVlan, changeDescriptionNetwork, vpnForm, changeDescriptionVPN, changeNetworkVPN, changeClassNetworkReletionship, \
    addClassNetwork, addConfigGenerate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .functions import binary

defaultValue = '---'

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
                'networks': networks,
                'networks_for_region': networks_for_region,
                'region_id': region_id,
                'region_object': region_object,
                'form': form,
                }

    return render(request, 'Network_page.html', parametrs)

@login_required(login_url='/accounts/login/')
def vlans(request, region_id):
    vlans_for_region = VLAN.objects.filter(region_reletionship=region_id)
    region_object = Region.objects.get(id=region_id)
    form = VlanForm(initial={'region_reletionship':region_object})
    resetPage = redirect('vlans', region_id)

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
            messages.success(request, f"VLAN Успешно создан VLAN")
            return resetPage
        else:
            messages.error(request, f"Не удалось создать VLAN")

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
    changeClassNetworkReletionshipForm = changeClassNetworkReletionship()
    changeVlanForm = changeVlan(region_id)

    parametrs = {'address_for_network': address_for_network,
                 'network_object': network_object,
                 'region_id': region_id,
                 'changeNetworkForm': changeNetworkForm,
                 'changeLocationForm': changeLocationForm,
                 'changeDescriptionNetwork': changeDescriptionNetwork,
                 'changeVlanForm': changeVlanForm,
                 'changeClassNetworkReletionshipForm': changeClassNetworkReletionshipForm,
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

            current_network_objects.update(network=correct_network_data, network_binary=binary(correct_network_data))

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
            return resetPage
        else:
            messages.error(request, f'Не удалось сменить дескрипшн сети {current_network}')

    if 'changeClassNetworkFormSubmit' in request.POST:
        changeClassNetworkReletionshipForm = changeClassNetworkReletionship(request.POST)
        if changeClassNetworkReletionshipForm.is_valid():
            newClassNetwork = request.POST['classNetwork_reletionship']
            current_network_objects.update(classNetwork_reletionship=newClassNetwork)
            messages.success(request, 'Классовая сеть успешно добавлена')
            return resetPage
        else:
            messages.error(request, 'Не удалось добавить классовую сеть')
    return render(request, 'ip_address_page.html', parametrs)

def vpnPool(request):
    all_vpnPool = VPN.objects.all()
    form_vpnPool = vpnForm()
    form_changeDescriptionNetwork = changeDescriptionNetwork()
    parametrs = {'all_vpnPool': all_vpnPool,
                 'form_vpnPool': form_vpnPool,
                 'form_changeDescriptionNetwork': form_changeDescriptionNetwork,
                 }

    if 'addPoolButton' in request.POST:
        form_vpnPool = vpnForm(request.POST)
        if form_vpnPool.is_valid():
            correct_network = form_vpnPool.save(commit=False)
            network_data = form_vpnPool.cleaned_data.get('pool')
            correct_network_data_raw = ipaddress.ip_interface(network_data)
            correct_network_data = correct_network_data_raw.network
            correct_network.pool = correct_network_data
            form_vpnPool.save()
            messages.success(request, f"Пул {correct_network_data} успешно создан")
        else:
            messages.error(request, "Не удалось создать пул")



    return render(request, 'vpnPool_page.html', parametrs)

def vpnPoolAddress(requst, vpn_id):
    network_object = VPN.objects.get(id=vpn_id)
    network_objects = VPN.objects.filter(id=vpn_id)
    address_for_network = Adress.objects.filter(vpnPool_reletionship=vpn_id)
    network_object_pool = network_object.pool
    changeDescriptionNetwork = changeDescriptionVPN()
    changeNetworkForm = changeNetworkVPN(network_object)
    changeClassNetworkReletionshipForm = changeClassNetworkReletionship()
    resetPage = redirect('vpnPoolAddress', vpn_id)


    if 'delNetButton' in requst.POST:
        network_object.delete()
        messages.success(requst, f"Сеть {network_object.pool} успешно удалена")
        return redirect('vpnPool')

    if 'changeDescriptionFormSubmit' in requst.POST:
        changeDescriptionForm = changeDescriptionVPN(requst.POST)
        if changeDescriptionForm.is_valid():
            newNetworkDescription = requst.POST['description']
            network_objects.update(description=newNetworkDescription)
            messages.success(requst, f'Дескрипшн сети {network_object} успешно изменён')
            return resetPage
        else:
            messages.error(requst, f'Не удалось сменить дескрипшн сети {network_object}')
            return resetPage

    if 'changeNetworkFormSubmit' in requst.POST:
        changeNetworkForm = changeNetworkVPN(network_object, requst.POST)
        new_network = requst.POST['pool']
        if changeNetworkForm.is_valid():
            print('asdasdasdasd')
            correct_network = changeNetworkForm.save(commit=False)
            network_data = changeNetworkForm.cleaned_data.get('pool')
            correct_network_data_raw = ipaddress.ip_interface(network_data)
            correct_network_data = correct_network_data_raw.network
            correct_network.network = correct_network_data

            network_objects.update(pool=correct_network_data, network_binary=binary(correct_network_data))

            messages.success(requst, f"Сеть {network_object_pool} изменена на сеть {correct_network_data}")
            return resetPage
        else:
            messages.error(requst, f"Не удалось изменить сеть {network_object_pool}")

    if 'changeClassNetworkFormSubmit' in requst.POST:
        changeClassNetworkReletionshipForm = changeClassNetworkReletionship(requst.POST)
        if changeClassNetworkReletionshipForm.is_valid():
            newClassNetwork = requst.POST['classNetwork_reletionship']
            network_objects.update(classNetwork_reletionship=newClassNetwork)
            messages.success(requst, 'Классовая сеть успешно добавлена')
            return resetPage
        else:
            messages.error(requst, 'Не удалось добавить классовую сеть')


    parametrs = {'network_object': network_object,
                 'address_for_network': address_for_network,
                 'changeDescriptionNetwork': changeDescriptionNetwork,
                 'changeNetworkForm': changeNetworkForm,
                 'changeClassNetworkReletionshipForm': changeClassNetworkReletionshipForm,
                 }

    return render(requst, 'vpnPool_address_page.html', parametrs)

def class_network(request):
    allClassNetworksObject = ClassNetwork.objects.all()
    addClassNetworkForm = addClassNetwork()

    if "trashButton" in request.POST:
        currentClassNetworkID = int(request.POST.get('currentClassNetworkID'))
        ClassNetwork.objects.get(id=currentClassNetworkID).delete()
        messages.success(request, "Классовая сеть успешно удалена")

    if "classNetworkButton" in request.POST:
        addClassNetworkForm = addClassNetwork(request.POST)
        newClassNetwork = request.POST['network']
        if addClassNetworkForm.is_valid():
            addClassNetworkForm.save()
            messages.success(request, f'Классовая сеть {newClassNetwork} успешно добавлена')
        else:
            messages.error(request, f'Не удалось добавить сеть {newClassNetwork}')

    context = {'allClassNetworksObject': allClassNetworksObject,
               'addClassNetworkForm': addClassNetworkForm}
    return render(request, 'class_network_page.html', context)

def all_networks_page(request):
    all_networks = Networks.objects.all()

    parametrs = {'all_networks': all_networks}
    return render(request, 'all_network_page.html', parametrs)

def testAjax(request):
    if request.is_ajax():
        response = {'first-text': "AJAX работает!"}
        print("AJAAAAAAAAAAAAAX!!!!!!!!!")
        return JsonResponse(response)
    else:
        raise Http404

def changeDescription(request):
    if request.is_ajax() and request.method == 'POST':
        result = request.POST['test']
        newDescription = request.POST['newDescription']
        print(newDescription)
        addressObject = Adress.objects.filter(id=result)
        if newDescription:
            addressObject.update(description=newDescription)
            response = {'newDescription': newDescription}
        else:
            addressObject.update(description=defaultValue)
            response = {'newDescription': defaultValue}

        return JsonResponse(response)

def changeClassNetwork(request):
    if request.is_ajax() and request.method == 'POST':
        objectId = request.POST['objectId']
        newClassNetwork = request.POST['newClassNetwork']
        classNetworkObject = ClassNetwork.objects.filter(id=objectId)
        network = ipaddress.IPv4Network(newClassNetwork)
        classNetworkObject.update(network=newClassNetwork, network_binary=binary(network))
        response = {'newClassNetwork': newClassNetwork}
        return JsonResponse(response)

def changeClassNetworkDescription(request):
    if request.is_ajax() and request.method == 'POST':
        objectId = request.POST['objectId']
        newClassNetworkDescription = request.POST['newClassNetworkDescription']
        classNetworkObject = ClassNetwork.objects.filter(id=objectId)
        if newClassNetworkDescription:
            classNetworkObject.update(description=newClassNetworkDescription)
            response = {'newClassNetworkDescription': newClassNetworkDescription}
        else:
            classNetworkObject.update(description=defaultValue)
            response = {'newClassNetworkDescription': defaultValue}
        return JsonResponse(response)

def changeVlanDescription(request):
    if request.is_ajax() and request.method == 'POST':
        objectId = request.POST['objectId']
        newVlanDescription = request.POST['newDescription']
        VlanObject = VLAN.objects.filter(id=objectId)
        if newVlanDescription:
            VlanObject.update(description=newVlanDescription)
            response = {'newDescription': newVlanDescription}
        else:
            VlanObject.update(description=defaultValue)
            response = {'newDescription': defaultValue}
        return JsonResponse(response)

def configGenerate (request):
    configGenerateForm = addConfigGenerate()



    if request.method == 'POST':
        configGenerateForm = addConfigGenerate(request.POST)
        if configGenerateForm.is_valid():
            number_bo = configGenerateForm.cleaned_data['number_bo']
            PAT_inet_address = configGenerateForm.cleaned_data['PAT_inet_address'].split(',')
            internetIPaddress = configGenerateForm.cleaned_data['internetIPaddress']
            if len(str(number_bo)) == 2:
                number_bo_for_description = '0' + str(number_bo)
            else:
                number_bo_for_description = number_bo

            if internetIPaddress != 'dhcp':
                internetIPaddress_raw = internetIPaddress.split(' ')
                internetIPaddress_without_mask = internetIPaddress_raw[:1]
                for i in internetIPaddress_without_mask:
                    internetIPaddress_without_mask = i
            else:
                internetIPaddress_without_mask = ''


            context2 = {
                        'Pat_geokod': configGenerateForm.cleaned_data['Pat_geokod'],
                        'number_bo': configGenerateForm.cleaned_data['number_bo'],
                        'PAT_inet_address': PAT_inet_address,
                        'logicalAddressTunnel0': configGenerateForm.cleaned_data['logicalAddressTunnel0'],
                        'physicalAddressTunnel0': configGenerateForm.cleaned_data['physicalAddressTunnel0'],
                        'logicalAddressTunnel1': configGenerateForm.cleaned_data['logicalAddressTunnel1'],
                        'interfaceISP1': configGenerateForm.cleaned_data['inetfaceISP1'],
                        'interfaceInternet': configGenerateForm.cleaned_data['interfaceInternet'],
                        'interfaceLAN': configGenerateForm.cleaned_data['interfaceLAN'],
                        'internetProviderName': configGenerateForm.cleaned_data['internetProviderName'],
                        'internetIPaddress': internetIPaddress,
                        'defaultIPaddress': configGenerateForm.cleaned_data['defaultIPaddress'],
                        'PatNumberForACL': configGenerateForm.cleaned_data['PatNumberForACL'],
                        'namePAT': configGenerateForm.cleaned_data['namePAT'],
                        'number_bo_for_description': number_bo_for_description,
                        'internetIPaddress_without_mask': internetIPaddress_without_mask}
            return render(request, 'config.html', context2)
    context = {'configGenerateForm': configGenerateForm}
    return render(request, 'config_generate.html', context)

@login_required(login_url='/accounts/login/')
def from_vlan_to_address(request, region_id, vlan_id):
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





