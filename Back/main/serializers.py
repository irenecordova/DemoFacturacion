
from .models import *
from rest_framework import serializers

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'

class FacturaDetalleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaDetalleItem
        fields = '__all__'

class CajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caja
        fields = '__all__'

class CobroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobro
        fields = '__all__'