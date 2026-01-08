from rest_framework import serializers
from .models import ProdutoBI, EstoqueBI, VendaBI

class ProdutoBISerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoBI
        exclude = ['id', 'tenant_id']

class EstoqueBISerializer(serializers.ModelSerializer):
    class Meta:
        model = EstoqueBI
        exclude = ['id', 'tenant_id']

class VendaBISerializer(serializers.ModelSerializer):
    class Meta:
        model = VendaBI
        exclude = ['id', 'tenant_id']
