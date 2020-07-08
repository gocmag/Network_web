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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
