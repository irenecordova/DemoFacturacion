from django.urls import path
from . import views


urlpatterns = [
    path('items/json', views.ItemList.as_view(), name='items/json'),
    path('factura/nuevo/', views.FacturaCreate.as_view(), name='factura-nuevo'),
    path('factura/<int:pk>', views.FacturaDetail.as_view(), name='factura-detalle'),
    path('factura/<int:pk>/cobrar', views.FacturaCobrar.as_view(), name='factura-cobrar'),
    path('caja/nuevo', views.CajaCreate.as_view(), name='caja-nuevo'),
    path('caja/cerrar', views.CajaCerrar.as_view(), name='caja-cerrar'),
]
