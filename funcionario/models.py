from django.db import models
import uuid
from tenant.models import Tenant, Loja

__all__ = [
    "Funcionario"
]

class Funcionario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_origem = models.CharField(max_length=50)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=15, null=True, blank=True)
    funcao = models.CharField(max_length=255)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "funcionario_funcionarios"

    def __str__(self):
        return self.nome
