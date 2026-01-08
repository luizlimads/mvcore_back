from rest_framework import serializers
from .models import Produto, Estoque
from common.serializers import TenantSerializerMixin

__all__ = [
    "ProdutoSerializer",
    "EstoqueSerializer"
]

class ProdutoSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'id_origem', 'referencia', 'descricao', 'grupo', 'id_grupo_origem', 
                  'marca', 'id_marca_origem', 'data_criacao', 'data_atualizacao_origem',
                  'colecao', 'id_colecao_origem']

class EstoqueSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = ['id', 'produto', 'quantidade', 'preco_venda', 'preco_custo', 'loja',
                  'data_criacao', 'tamanho', 'cor', 'data_atualizacao_origem']
