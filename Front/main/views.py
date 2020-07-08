from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from django.http import JsonResponse

import requests
import json

# Create your views here.

class ItemList(View):

	def get(self, request):
		req = requests.request('GET', settings.API_ROOT_DIR+'items/')
		result = req.json()
		context = {
			'result': result['data']
		}
		return JsonResponse(result)

class FacturaCreate(View):

	def post(self, request):
		data = request.POST
        
		datos_documento = {}
		factura = {
			"fecha_emision": data['fecha_emision'],
			"cliente": data['cliente'],
			"vendedor": data['vendedor'],
			"descripcion": data['descripcion_documento'],
			"secuencial": data['secuencial']
        }

		datos_documento['factura'] = factura
        
		tamanio = len(data.getlist('item'))
		detalles_items = []
		for i in range(0, tamanio):
			if data.getlist('item')[i] != "" and data.getlist('cantidad')[i] != "" and data.getlist('precio_unitario')[i] != "" and data.getlist('descuento_porcentaje')[i] != "" and data.getlist('descuento_dolares')[i] != "":
				detalle={					
					"item":data.getlist('item')[i],
					"cantidad":data.getlist('cantidad')[i],
					"precio_unitario":data.getlist('precio_unitario')[i],
					"descuento_porcentaje":data.getlist('descuento_porcentaje')[i],
					"descuento_dolares":data.getlist('descuento_dolares')[i],
					"ice_porcentaje":data.getlist('ice_porcentaje')[i],
					"iva_porcentaje":data.getlist('iva_porcentaje')[i],
				}
				detalles_items.append(detalle)
		datos_documento['detalles_items'] = detalles_items

		req = requests.request('POST', settings.API_ROOT_DIR+'facturas/', json=datos_documento)
		result = req.json()
		return JsonResponse(result)

	def get(self, request):
		context = {
			'accion': 'Registrar'
		}
		return render(request, 'main/factura_form.html', context)

class FacturaDetail(View):

    def get(self, request, pk):
        
        req = requests.request('GET', settings.API_ROOT_DIR+'facturas/'+str(pk)+'/')
        result = req.json()
        factura = result.get('data')
        print(result['data'])
        context = {
            "factura": factura,
            "accion": "Ver"
        }

        if (factura):
            return render(request, 'main/factura_form.html', context=context)
        return redirect('factura-nuevo')

class FacturaCobrar(View):

	def post(self, request):
		data = request.POST
		req = requests.request('POST', settings.API_ROOT_DIR+'facturas/'+str(pk)+'/cobrar/', data=data)
		result = req.json()
		return JsonResponse(result)

	def get(self, request):
		context = {
			'accion': 'Registrar'
		}
		return render(request, 'main/factura_form.html', context)


class CajaCreate(View):
	def post(self, request):
		data = request.POST
		req = requests.request('POST', settings.API_ROOT_DIR+'cajas/', data=data)
		result = req.json()
		return JsonResponse(result)

	def get(self, request):
		return render(request, 'main/abrir_caja.html')

class CajaCerrar(View):
	def post(self, request):
		data = request.POST
		req = requests.request('POST', settings.API_ROOT_DIR+'cajas/cerrar_caja/', data=data)
		result = req.json()
		return JsonResponse(result)

	def get(self, request):
		return render(request, 'main/cerrar_caja.html')