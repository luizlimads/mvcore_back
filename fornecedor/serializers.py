from rest_framework import serializers
from .models import Fornecedor
from common.serializers import TenantSerializerMixin

__all__ = [
    "FornecedorSerializer"
]

class FornecedorSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ['id', 'id_origem', 'documento', 'razao_social', 'nome_fantasia', 'data_criacao']
