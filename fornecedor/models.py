from django.db import models
import uuid
from tenant.models import Tenant
from produto.models import Produto
from django.utils import timezone

__all__ = [
    "Fornecedor"
]

class Fornecedor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_origem = models.CharField(max_length=50)
    documento = models.CharField(max_length=20, null=True, blank=True)
    razao_social = models.CharField(max_length=255, null=True, blank=True)
    nome_fantasia = models.CharField(max_length=255, null=True, blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(default=timezone.now)

    produtos = models.ManyToManyField(Produto, related_name='fornecedores')

    class Meta:
        db_table = "fornecedor_fornecedores"

    def __str__(self):
        return self.nome_fantasia
