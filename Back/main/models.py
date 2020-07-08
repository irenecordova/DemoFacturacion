from django.db import models

# Create your models here.
class Caja(models.Model):
	fecha_apertura = models.DateTimeField(auto_now_add=True, null=False, blank=False)
	fecha_cierre = models.DateTimeField(null=True, blank=True)
	saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
	saldo_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	total_cierre = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	efectivo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	tarjeta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	cheque = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	cerrada = models.BooleanField(null=False, default=False)

	def to_dict(self):
		return {
			"id": self.pk,
			"fecha_apertura": self.fecha_apertura,
			"fecha_cierre": str(self.fecha_cierre),
			"efectivo": str(self.efectivo),
			"tarjeta": str(self.tarjeta),
			"cheque": str(self.cheque),
			"saldo_inicial": str(self.saldo_inicial),
			"saldo_final": str(self.saldo_final),
			"total_cierre": str(self.total_cierre)
		}

class Factura(models.Model):
	fecha_emision = models.DateField()
	secuencial = models.CharField(max_length=100, blank=True, null=True, default='')
	cliente = models.CharField(max_length=200, blank=True, null=True, default='')
	vendedor = models.CharField(max_length=200, blank=True, null=True, default='')
	descripcion = models.CharField(max_length=400, blank=True, null=True)
	caja = models.ForeignKey(Caja, on_delete=models.SET_NULL, blank=True, null=True, related_name='facturas')
	fecha_registro = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.secuencial

	@property
	def detalles_items_dict(self):
		return [d.to_dict() for d in self.detalles_items.all().order_by("id")]


	def to_dict(self):
	
		result = {
			"id": self.pk,
			"documento_no": self.secuencial,
			'fecha_emision': self.fecha_emision,
			"cliente": str(self.cliente),
			"vendedor": str(self.vendedor),
			"descripcion": self.descripcion,
			"items": self.detalles_items_dict,
		}
		
class FacturaDetalleItem(models.Model):
	factura = models.ForeignKey(Factura, on_delete = models.CASCADE, related_name="detalles_items" )

	item = models.CharField(max_length=200)
	cantidad = models.DecimalField(max_digits=14, decimal_places=6, default=0)
	precio_unitario = models.DecimalField(max_digits=14, decimal_places=6, default=0)
	descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	descuento_dolares = models.DecimalField(max_digits=14, decimal_places=6, default=0)
	ice_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)


	def __str__(self):
		return '{} - {}'.format(self.factura, self.item)

	@property
	def subtotal_no_descuento(self):
		return self.precio_unitario * self.cantidad

	@property
	def subtotal(self):
		return self.subtotal_no_descuento - self.descuento_dolares

	@property
	def ice_dolares(self):
		return (self.subtotal * self.ice_porcentaje) / 100

	@property
	def subtotal_con_ice(self):
		return self.subtotal + self.ice_dolares

	@property
	def iva_dolares(self):
		return (self.subtotal_con_ice * self.iva_porcentaje) / 100

	@property
	def total(self):
		return self.subtotal + self.ice_dolares + self.iva_dolares

	def to_dict(self):
		
		return {
			"id": self.pk,
			"item": self.item,
			"cantidad": str(self.cantidad),
			"precio_unitario": str(self.precio_unitario),
			"descuento_dolares": str(self.descuento_dolares),
			"descuento_porcentaje": str(self.descuento_porcentaje),
			"ice_porcentaje": str(self.ice_porcentaje),
			"iva_porcentaje": str(self.iva_porcentaje),
			"subtotal": str(self.subtotal)
		}

class Cobro(models.Model):
	TIPOCOBRO = (( 'CH', 'Cheque'), ( 'EF', 'Efectivo'), ( 'TC', 'Tarjeta de crédito'))

	fecha_cobro = models.DateField()	
	tipo_cobro = models.CharField(max_length = 2, choices = TIPOCOBRO, default = 'N')
	monto = models.DecimalField(max_digits=14, decimal_places=6, default=0)
	factura = models.ForeignKey(Factura, on_delete = models.CASCADE, related_name="cobros" )
	fecha_registro = models.DateField(auto_now_add=True, blank=True)