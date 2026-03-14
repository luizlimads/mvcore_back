from django.db import models
from django.utils import timezone
import uuid
from common.constants import ADMIN_SYSTEM_ID, ADMIN_TENANT_ID

class SistemaIntegrado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255, unique=True)
    data_criacao = models.DateTimeField(default=timezone.now)

    def delete(self, *args, **kwargs):
        if self.id == ADMIN_SYSTEM_ID:
            raise Exception("O sistema ADMIN não pode ser removido.")
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = "tenant_sistemas"
        
    def __str__(self):
        return self.nome

class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.CharField(max_length=15, unique=True)
    razao_social = models.CharField(max_length=255, null=True, blank=True)
    nome_fantasia = models.CharField(max_length=255, null=True, blank=True)
    sistema_integrado = models.ForeignKey(SistemaIntegrado, on_delete=models.RESTRICT, related_name='tenants')
    api_document = models.CharField(max_length=50, null=True, blank=True)
    api_user = models.CharField(max_length=50, null=True, blank=True)
    api_token = models.CharField(max_length=70, null=True, blank=True)
    api_key = models.CharField(max_length=50, null=True, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    db_host = models.CharField(max_length=20, null=True, blank=True)
    db_port = models.IntegerField(null=True, blank=True)
    db_user = models.CharField(max_length=30, null=True, blank=True)
    db_pass = models.CharField(max_length=50, null=True, blank=True)
    db_name = models.CharField(max_length=30, null=True, blank=True)
    bi_api_key = models.CharField(max_length=100, unique=True, null=True, blank=True)
    bi_api_key_active = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if self.id == ADMIN_TENANT_ID:
            raise Exception("O tenant ADMIN não pode ser removido.")
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = "tenant_tenants"

    def __str__(self):
        return self.razao_social

class Loja(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    documento = models.CharField(max_length=15)
    imposto_aliquota_padrao = models.FloatField(default=0)
    tenant = models.ForeignKey(Tenant, on_delete=models.RESTRICT, related_name='lojas')
    data_criacao = models.DateTimeField(default=timezone.now)
    id_origem = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "tenant_lojas"

    def __str__(self):
        return self.nome
