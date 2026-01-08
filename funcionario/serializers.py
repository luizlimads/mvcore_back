from rest_framework import serializers
from .models import Funcionario
from common.serializers import TenantSerializerMixin

__all__ = [
    "FuncionarioSerializer"
]

class FuncionarioSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id', 'id_origem', 'nome','cpf', 'funcao', 'loja', 'data_criacao']
