from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.region, name='region_page'),
    path('choise/<int:region_id>', views.choise_page, name='choise_page'),
    path('network/<int:region_id>', views.networking, name='network'),
    path('network/<int:region_id>/<int:network_id>/address',views.address, name='address'),
    path('vlans/<int:region_id>', views.vlans, name='vlans'),
    path('redirect_from_vlan_to_address/<int:region_id>/<int:vlan_id>', views.from_vlan_to_address, name='from_vlan_to_address'),
    path('search_page/', views.search_view, name='search_view'),
    path('all_networks/', views.all_networks_page, name='all_networks_url'),
    path('vpnpool/', views.vpnPool, name='vpnPool'),
    path('vpnpool/<int:vpn_id>', views.vpnPoolAddress, name='vpnPoolAddress'),
    path('ajax/', views.testAjax, name='ajax'),
    path('changeDescription/', views.changeDescription, name='changeDescription'),
    path('classNetworks/', views.class_network, name='classNetworks'),
    path('changeClassNetwork/', views.changeClassNetwork, name='changeClassNetwork'),
    path('changeClassNetworkDescription/', views.changeClassNetworkDescription, name='changeClassNetworkDescription'),
    path('changeVlanDescription/', views.changeVlanDescription, name='changeVlanDescription'),
    path('configGenerate/', views.configGenerate, name='configGenerate')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
