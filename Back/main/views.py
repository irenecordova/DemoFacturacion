from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db import transaction
from django.db.models import Sum

from .models import *
from .serializers import *

import requests
import json
from decimal import *

# Create your views here.

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

    def list(self, request):
        queryset = Factura.objects.all()
        return Response({'data': queryset, 'error': 0, 'detail': 'Búsqueda realizada exitosamente'})

    def create(self, request):
        try:
            with transaction.atomic():
                data = request.data
                factura = data['factura']
                detalles_items = data['detalles_items']

                if not Caja.objects.filter(cerrada=False):
                    raise Exception("No existe una caja abierta.")

                caja = Caja.objects.filter(cerrada=False).first()
                factura['caja'] = caja.pk

                factura_serializer = FacturaSerializer(data=factura)
                if factura_serializer.is_valid():
                    factura_serializer.save()
                else:
                    raise Exception(factura_serializer.errors)

                for detalle_item in detalles_items:
                    detalle_item['factura'] = factura_serializer.data['id']
                    factura_detalle_serializer = FacturaDetalleItemSerializer(data=detalle_item)
                    if factura_detalle_serializer.is_valid():
                        factura_detalle_serializer.save()
                    else:
                        raise Exception(factura_detalle_serializer.errors)
                
                return Response({'data': factura_serializer.data['id'], 'detail': 'La factura fue creada exitosamente.', 'error':0})

        except Exception as e:
            return Response({'detail': 'No se registró factura. Error: '+str(e), 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        try:
            factura = self.get_object()
            return Response({'data': factura.to_dict(), 'error': 0})
        except Exception as e:
            print(e)
            return Response({'detail': 'No se puede ver la afctura. Error: '+str(e), 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'])
    def cobrar(self, request, pk=None):
        try:
            with transaction.atomic():
                factura = self.get_object()
                data = request.data.copy()
                data['factura'] = factura.pk

                cobro_serializer = CobroSerializer(data=data)
                if cobro_serializer.is_valid():
                    cobro_serializer.save()
                else:
                    raise Exception(cobro_serializer.errors)
                
        except Exception as e:
            return Response({'detail': 'No se registró el cobro. Error: '+str(e), 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

class ItemViewSet(viewsets.ModelViewSet):

    def list(self, request):
        
        headers = {
        'x-api-key': '0d518993ba024ef6b1e3267ac9da6bd0'
        }
        datil_api_url = "https://api.datil.co/catalog/products?page_size=3"
        products = requests.get(datil_api_url, headers=headers).json()
        print(products)
        return Response({'data': queryset, 'error': 0, 'detail': 'Búsqueda realizada exitosamente'})

class CajaViewSet(viewsets.ModelViewSet):
    queryset = Caja.objects.all()
    serializer_class = CajaSerializer
    
    def create(self, request):
        try:
            with transaction.atomic():
                data = request.data

                if Caja.objects.filter(cerrada=False):
                    raise Exception("Ya existe una caja abierta.")
                
                caja_serializar = CajaSerializer(data=data)
                if caja_serializar.is_valid():
                    caja_serializar.save()
                else:
                    raise Exception(caja_serializar.errors)
                return Response({'error': 0, 'detail': 'Se abrió caja exitosamente'})
        
        except Exception as e:
            return Response({'detail': 'No se puedo abrir caja. Error: '+str(e), 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=False, methods=['post'])
    def cerrar_caja(self, request):
        try:
            with transaction.atomic():
                data = request.data

                if not Caja.objects.filter(cerrada=False):
                    raise Exception("No existe una caja abierta.")

                caja = Caja.objects.filter(cerrada=False).first()
                tarjeta = Cobro.objects.filter(factura__caja=caja, tipo_cobro='TC').aggregate(subtotal__sum=Sum( ('monto') ))['subtotal__sum']
                if not tarjeta:
                    tarjeta = 0
                cheque = Cobro.objects.filter(factura__caja=caja, tipo_cobro='CH').aggregate(subtotal__sum=Sum( ('monto') ))['subtotal__sum']
                if not cheque:
                        cheque = 0
                efectivo = Cobro.objects.filter(factura__caja=caja, tipo_cobro='EF').aggregate(subtotal__sum=Sum( ('monto') ))['subtotal__sum']
                if not efectivo:
                    efectivo = 0

                data_caja = {
                    "fecha_apertura": caja.fecha_apertura,
                    "fecha_cierre": caja.fecha_cierre,
                    "efectivo": efectivo,
                    "tarjeta": tarjeta,
                    "cheque": cheque,
                    "saldo_inicial": caja.saldo_inicial,
                    "saldo_final": Decimal(data['saldo_final']),
                    "total_cierre": Decimal(data['saldo_final']) - Decimal(caja.saldo_inicial),
                    "cerrada": True,
                }

                caja_serializar = CajaSerializer(caja, data=data_caja)
                if caja_serializar.is_valid():
                    caja_serializar.save()
                else:
                    raise Exception(caja_serializar.errors)

                return Response({'error': 0, 'detail': 'Se cerró caja exitosamente'})
        
        except Exception as e:
            return Response({'detail': 'No se puedo cerrar caja. Error: '+str(e), 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):

        cajas = Caja.objects.objects.all()
        result = []
        for caja in cajas:
            result.append(caja.to_dict())
        return Response({'data': result, 'error': 0, 'detail': 'Búsqueda realizada exitosamente'})
