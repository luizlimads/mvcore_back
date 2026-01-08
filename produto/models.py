from django.db import models
import uuid
from tenant.models import Tenant, Loja
from django.utils import timezone

__all__ = [
    "Produto",
    "Estoque"
]

class Produto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_origem = models.CharField(max_length=50)
    referencia = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)
    grupo = models.CharField(max_length=255,null=True, blank=True)
    id_grupo_origem = models.CharField(max_length=50,null=True, blank=True)
    marca = models.CharField(max_length=255,null=True, blank=True)
    id_marca_origem = models.CharField(max_length=50,null=True, blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_atualizacao_origem = models.DateTimeField(null=True, blank=True)
    tamanho = models.CharField(max_length=10,null=True, blank=True)
    cor = models.CharField(max_length=30,null=True, blank=True)
    departamento = models.CharField(max_length=50,null=True, blank=True)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    colecao = models.CharField(max_length=255,null=True, blank=True)
    id_colecao_origem = models.CharField(max_length=50,null=True, blank=True)

    class Meta:
        db_table = "produto_produtos"

    def __str__(self):
        return self.referencia

class Estoque(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    tamanho = models.CharField(max_length=10,null=True, blank=True)
    cor = models.CharField(max_length=30,null=True, blank=True)
    data_atualizacao_origem = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "produto_estoques"

    def __str__(self):
        return self.produto.referencia
