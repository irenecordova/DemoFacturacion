from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Caja)
admin.site.register(Cobro)
admin.site.register(Factura)
admin.site.register(FacturaDetalleItem)
