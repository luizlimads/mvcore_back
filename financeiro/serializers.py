from rest_framework import serializers
from .models import InstituicaoFinanceira, ContaFinanceira, CategoriaFinanceira, Lancamento
from common.serializers import TenantSerializerMixin

__all__ = [
    "InstituicaoFinanceiraSerializer",
    "ContaFinanceiraSerializer",
    "CategoriaFinanceiraSerializer",
    "LancamentoSerializer"
]

class InstituicaoFinanceiraSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = InstituicaoFinanceira
        fields = ['id', 'codigo', 'nome', 'data_criacao', 'id_origem']

class ContaFinanceiraSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ContaFinanceira
        fields = ['id', 'id_origem', 'agencia', 'conta', 'digito_verificador', 'descricao', 'instituicao_financeira', 'data_criacao']

class CategoriaFinanceiraSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = CategoriaFinanceira
        fields = ['id', 'id_origem', 'descricao', 'tipo', 'categoria_pai', 'data_criacao']

class LancamentoSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Lancamento
        fields = ['id', 'id_origem', 'data_competencia', 'data_lancamento', 'valor', 'tipo', 
                  'descricao', 'venda', 'conta', 'categoria', 'fornecedor', 'data_criacao']

class LancamentoDetailSerializer(LancamentoSerializer):
    conta = ContaFinanceiraSerializer(read_only=True)
    categoria = CategoriaFinanceiraSerializer(read_only=True)
    class Meta:
        model = Lancamento
        fields = ['id', 'id_origem', 'data_competencia', 'data_lancamento', 'valor', 'tipo', 
                  'descricao', 'venda', 'conta', 'categoria', 'fornecedor', 'data_criacao']