from django.db import transaction
from rest_framework import serializers
from .models import FormaPagamento, Venda, ItemVenda
from common.serializers import TenantSerializerMixin

__all__ = [
    "VendaCreateSerializer"
]

class VendaSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    class ItemVendaSerializer(TenantSerializerMixin, serializers.ModelSerializer):
        produto_descricao = serializers.CharField(source='produto.descricao')
        funcionario_nome = serializers.CharField(source='funcionario.nome', default=None, allow_null=True, required=False)

        class Meta:
            model = ItemVenda
            fields = ['id', 'produto_descricao', 'id_origem', 'quantidade', 'custo', 'valor_unitario_bruto', 'desconto',
                      'acrescimo', 'imposto_aliquota', 'valor_unitario_liquido', 'valor_total_liquido', 'data_criacao',
                      'tamanho', 'cor', 'funcionario_nome']

    class FormaPagamentoSerializer(TenantSerializerMixin, serializers.ModelSerializer):
        class Meta:
            model = FormaPagamento
            fields = ['id', 'id_origem', 'data', 'valor', 'parcelas', 'descricao', 'data_criacao']
        
    formas_pagamento = FormaPagamentoSerializer(many=True, default=None, allow_null=True, required=False)
    itens = ItemVendaSerializer(many=True, default=None, allow_null=True, required=False)    
    funcionario_nome = serializers.CharField(source='funcionario.nome', default=None, allow_null=True, required=False)

    class Meta:
        model = Venda
        fields = ['id', 'id_origem', 'data', 'status', 'numero', 'valor_bruto', 'acrescimo', 'desconto',  'credito_troca', 
                  'valor_liquido', 'funcionario_nome', 'loja', 'data_criacao', 'formas_pagamento', 'itens']

class VendaCreateSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    class ItemVendaCreateSerializer(TenantSerializerMixin, serializers.ModelSerializer):
        class Meta:
            model = ItemVenda
            fields = ['produto', 'id_origem', 'quantidade', 'custo', 'valor_unitario_bruto', 'desconto',
                      'acrescimo', 'imposto_aliquota', 'valor_unitario_liquido', 'valor_total_liquido', 
                      'tamanho', 'cor', 'funcionario']
                
    class FormaPagamentoCreateSerializer(TenantSerializerMixin, serializers.ModelSerializer):
        class Meta:
            model = FormaPagamento
            fields = ['id_origem', 'data', 'valor', 'parcelas', 'descricao']

    formas_pagamento = FormaPagamentoCreateSerializer(many=True)
    itens = ItemVendaCreateSerializer(many=True)

    class Meta:
        model = Venda
        fields = ['id', 'id_origem', 'data', 'status', 'numero', 'valor_bruto', 'acrescimo', 'desconto',
                  'credito_troca', 'valor_liquido', 'funcionario', 'loja', 'formas_pagamento', 'itens']

    def create(self, validated_data):
        itens = validated_data.pop('itens')
        formas_pagamento = validated_data.pop('formas_pagamento')

        tenant = self.get_tenant_instance()
        validated_data['tenant'] = tenant

        with transaction.atomic():
            venda = Venda.objects.create(**validated_data)

            for item in itens:
                ItemVenda.objects.create(venda=venda, tenant=venda.tenant, **item)

            for pagamento in formas_pagamento:
                FormaPagamento.objects.create(venda=venda, tenant=venda.tenant, **pagamento)

        return venda
