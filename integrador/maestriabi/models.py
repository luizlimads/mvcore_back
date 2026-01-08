from django.db import models

class ProdutoBI(models.Model):
    id = models.AutoField(primary_key=True)
    cod_produto = models.CharField(max_length=255)
    desc_produto = models.TextField(max_length=255)
    categoria = models.CharField(max_length=255, null=True)
    fornecedor = models.CharField(max_length=255, null=True)
    nivel_1 = models.CharField(max_length=255, null=True)
    nivel_2 = models.CharField(max_length=255, null=True)
    nivel_3 = models.CharField(max_length=255, null=True)
    tenant_id = models.UUIDField()

    class Meta:
        managed = False
        db_table = "vw_maestriabi_produtos"


class EstoqueBI(models.Model):
    id = models.AutoField(primary_key=True)
    loja = models.CharField(max_length=255)
    mes = models.CharField(max_length=3)
    ano = models.IntegerField()
    codigo = models.CharField(max_length=255)
    imposto = models.DecimalField(max_digits=18, decimal_places=6)
    estoque_custo_unit = models.DecimalField(max_digits=18, decimal_places=6)
    estoque_pecas = models.DecimalField(max_digits=18, decimal_places=6)
    custo_total = models.DecimalField(max_digits=18, decimal_places=6)
    estoque_vlr = models.DecimalField(max_digits=18, decimal_places=6)
    data = models.DateField()
    tenant_id = models.UUIDField()

    class Meta:
        managed = False
        db_table = "vw_maestriabi_estoques"


class VendaBI(models.Model):
    id = models.AutoField(primary_key=True)
    loja = models.CharField(max_length=255)
    mes = models.CharField(max_length=3)
    ano = models.IntegerField()
    codigo = models.CharField(max_length=255)
    custo_total = models.DecimalField(max_digits=18, decimal_places=6)
    venda_qnt = models.DecimalField(max_digits=18, decimal_places=6)
    venda_vlr = models.DecimalField(max_digits=18, decimal_places=6)
    descontos = models.DecimalField(max_digits=18, decimal_places=6)
    venda = models.CharField(max_length=255)
    vendas = models.DecimalField(max_digits=18, decimal_places=6)
    lucro_bruto = models.DecimalField(max_digits=18, decimal_places=6)
    data = models.DateField()
    tenant_id = models.UUIDField()

    class Meta:
        managed = False
        db_table = "vw_maestriabi_vendas"
