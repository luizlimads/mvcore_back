from django.db import models
import uuid
from tenant.models import Tenant
from venda.models import Venda
from fornecedor.models import Fornecedor

__all__ = [
    "TipoCategoriaChoices",
    "TipoLancamentoChoices",
    "InstituicaoFinanceira",
    "ContaFinanceira",
    "CategoriaFinanceira",
    "Lancamento"
]

class TipoCategoriaChoices(models.TextChoices):
    NAO_IDENTIFICADO = 'Não identificado'
    ENTRADAS = 'Entradas'
    SAIDAS = 'Saídas'

class TipoLancamentoChoices(models.TextChoices):
    NAO_IDENTIFICADO = 'Não identificado'
    CREDITO = 'Crédito'
    DEBITO = 'Débito'

class InstituicaoFinanceira(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=255, null=True, blank=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    id_origem = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "financeiro_instituicoes"

    def __str__(self):
        return self.nome
    
class ContaFinanceira(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_origem = models.CharField(max_length=50)
    agencia = models.CharField(max_length=255, null=True, blank=True)
    conta = models.CharField(max_length=255, null=True, blank=True)
    digito_verificador = models.CharField(max_length=10, null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    instituicao_financeira = models.ForeignKey(InstituicaoFinanceira, null=True, blank=True, on_delete=models.RESTRICT)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "financeiro_contas"

    def __str__(self):
        return f'Conta {self.agencia} - {self.conta}'

class CategoriaFinanceira(models.Model):  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_origem = models.CharField(max_length=50)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=20, null=True, blank=True, choices=TipoCategoriaChoices.choices)
    categoria_pai = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "financeiro_categorias"

    def __str__(self):
        return self.descricao

class Lancamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_origem = models.CharField(max_length=50)
    data_competencia = models.DateTimeField(null=True, blank=True)
    data_lancamento = models.DateTimeField(null=True, blank=True)
    valor = models.FloatField(null=True, blank=True)
    tipo = models.CharField(max_length=20, null=True, blank=True, choices=TipoLancamentoChoices.choices)
    descricao = models.TextField(null=True, blank=True)
    venda = models.ForeignKey(Venda, null=True, blank=True, on_delete=models.CASCADE)
    conta = models.ForeignKey(ContaFinanceira, null=True, blank=True, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaFinanceira, null=True, blank=True, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, null=True, blank=True, on_delete=models.DO_NOTHING)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "financeiro_lancamentos"

    def __str__(self):
        return self.descricao