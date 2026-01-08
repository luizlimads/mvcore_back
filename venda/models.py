from django.db import models
import uuid
from tenant.models import Tenant, Loja
from produto.models import Produto
from funcionario.models import Funcionario

__all__ = [
    "Venda",
    "ItemVenda",
    "FormaPagamento",
    "StatusChoices"
]

class StatusChoices(models.TextChoices):
    NAO_IDENTIFICADO = 'Não identificado'
    ATIVA = 'Ativa'
    CANCELADA = 'Cancelada'

class Venda(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_origem = models.CharField(max_length=50)
    data = models.DateTimeField()
    status =  models.CharField(max_length=20, choices=StatusChoices.choices)
    numero = models.CharField(max_length=50, null=True, blank=True)
    valor_bruto = models.FloatField(null=True, blank=True)
    acrescimo = models.FloatField(null=True, blank=True)
    desconto = models.FloatField(null=True, blank=True)
    credito_troca = models.FloatField(null=True, blank=True)
    valor_liquido = models.FloatField(null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='funcionario')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao_origem = models.DateTimeField(null=True, blank=True)

    produtos = models.ManyToManyField(Produto, through="ItemVenda", related_name='vendas')

    class Meta:
        db_table = "venda_vendas"

    def __str__(self):
        return self.numero

class ItemVenda(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    id_origem = models.CharField(max_length=50)
    quantidade = models.FloatField()
    custo = models.FloatField()
    valor_unitario_bruto = models.FloatField()
    desconto = models.FloatField()
    acrescimo = models.FloatField()
    imposto_aliquota = models.FloatField(default=0)
    valor_unitario_liquido = models.FloatField()
    valor_total_liquido = models.FloatField()
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    tamanho = models.CharField(max_length=10,null=True, blank=True)
    cor = models.CharField(max_length=30,null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='funcionario_item')
    trocado = models.BooleanField(default=False)

    class Meta:
        db_table = "venda_itens"

    def __str__(self):
        return self.id_produto.descricao

class FormaPagamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='formas_pagamento')
    id_origem = models.CharField(max_length=50)
    data = models.DateTimeField()
    valor = models.FloatField()
    parcelas = models.IntegerField()
    descricao = models.CharField(max_length=255)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "venda_pagamentos"

    def __str__(self):
        return self.descricao
