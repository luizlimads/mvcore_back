from datetime import datetime
from decimal import Decimal
from django.db import transaction
from django.db.models import Max
from tenant.models import Loja
from produto.models import Produto, Estoque
from fornecedor.models import Fornecedor
from .client import EstoqueClient

class EstoqueImporter:
    def __init__(self, tenant):
        self.tenant = tenant

    def executar_produtos(self, conf):
        now = datetime.now()
        produto_max = Produto.objects.filter(tenant=self.tenant).aggregate(max_dt=Max("data_atualizacao_origem"))["max_dt"]
        inicio_prod = produto_max or datetime(1970,1,1)
        fim_prod = now
        with EstoqueClient(conf) as client:
            produtos = client.fetch_produtos(inicio_prod, fim_prod)
        ids = [str(p["id_origem"]) for p in produtos]
        existing_produtos = Produto.objects.filter(id_origem__in=ids, tenant=self.tenant)
        existing_map = {str(p.id_origem): p for p in existing_produtos}
        produtos_to_create = []
        produtos_to_update = []
        for p in produtos:
            key = str(p["id_origem"])
            if key in existing_map:
                prod = existing_map[key]
                prod.referencia = p.get("referencia") or prod.referencia
                prod.descricao = p.get("descricao") or prod.descricao
                prod.grupo = p.get("grupo") or prod.grupo
                prod.id_grupo_origem = str(p.get("id_grupo_origem")) if p.get("id_grupo_origem") is not None else prod.id_grupo_origem
                prod.marca = p.get("marca") or prod.marca
                prod.id_marca_origem = str(p.get("id_marca_origem")) if p.get("id_marca_origem") is not None else prod.id_marca_origem
                prod.data_atualizacao_origem = p.get("data_atualizacao_origem") or prod.data_atualizacao_origem
                produtos_to_update.append(prod)
            else:
                produtos_to_create.append(Produto(
                    id_origem=key,
                    referencia=p.get("referencia") or "",
                    descricao=p.get("descricao") or "",
                    grupo=p.get("grupo"),
                    id_grupo_origem=str(p.get("id_grupo_origem")) if p.get("id_grupo_origem") is not None else None,
                    marca=p.get("marca"),
                    id_marca_origem=str(p.get("id_marca_origem")) if p.get("id_marca_origem") is not None else None,
                    tenant_id=self.tenant,
                    data_atualizacao_origem=p.get("data_atualizacao_origem")
                ))
        with transaction.atomic():
            if produtos_to_create:
                Produto.objects.bulk_create(produtos_to_create, batch_size=500)
            if produtos_to_update:
                Produto.objects.bulk_update(produtos_to_update, ["referencia","descricao","grupo","id_grupo_origem","marca","id_marca_origem","data_atualizacao_origem"], batch_size=500)

    def executar_estoques(self, conf):
        now = datetime.now()
        with EstoqueClient(conf) as client:
            estoques = client.fetch_estoques()
        lojas_qs = Loja.objects.filter(tenant=self.tenant)
        lojas_map = {str(l.id_origem): l.id for l in lojas_qs}
        produtos_qs = Produto.objects.filter(tenant=self.tenant)
        produtos_map = {str(p.id_origem): p.id for p in produtos_qs}
        grouped = {}
        for e in estoques:
            produto_key = str(e.get("produto"))
            loja_key = str(e.get("loja"))
            tamanho = e.get("tamanho") or ""
            cor = e.get("cor") or ""
            dt = e.get("data_atualizacao_origem") or datetime.now()
            if produto_key not in produtos_map:
                continue
            pk = (produto_key, loja_key, tamanho, cor)
            current = grouped.get(pk)
            if not current or dt > current["data_atualizacao_origem"]:
                grouped[pk] = {
                    "produto": produtos_map[produto_key],
                    "loja": lojas_map.get(loja_key),
                    "tamanho": tamanho,
                    "cor": cor,
                    "quantidade": e.get("quantidade"),
                    "preco_venda": e.get("preco_venda"),
                    "preco_custo": e.get("preco_custo"),
                    "data_atualizacao_origem": dt
                }
        if not grouped:
            pass
        month = now.month
        year = now.year
        with transaction.atomic():
            Estoque.objects.filter(tenant=self.tenant, data_criacao__year=year, data_criacao__month=month).delete()
            to_create = []
            for v in grouped.values():
                quantidade = v["quantidade"]
                preco_venda = v["preco_venda"]
                preco_custo = v["preco_custo"]
                try:
                    quantidade = Decimal(str(quantidade)) if quantidade is not None else Decimal("0")
                except:
                    quantidade = Decimal("0")
                try:
                    preco_venda = Decimal(str(preco_venda)) if preco_venda is not None else Decimal("0")
                except:
                    preco_venda = Decimal("0")
                try:
                    preco_custo = Decimal(str(preco_custo)) if preco_custo is not None else Decimal("0")
                except:
                    preco_custo = Decimal("0")
                to_create.append(Estoque(
                    produto_id=v["produto"],
                    quantidade=quantidade,
                    preco_venda=preco_venda,
                    preco_custo=preco_custo,
                    tenant_id=self.tenant,
                    loja_id=v["loja"],
                    tamanho=v["tamanho"],
                    cor=v["cor"],
                    data_atualizacao_origem=v["data_atualizacao_origem"]
                ))
            if to_create:
                Estoque.objects.bulk_create(to_create, batch_size=1000)

    def executar_fornecedores(self, conf):
        with EstoqueClient(conf) as client:
            fornecedores = client.fetch_produtos_fornecedores()
        if fornecedores:
            produtos_qs = Produto.objects.filter(tenant=self.tenant)
            produtos_map = {str(p.id_origem): p for p in produtos_qs}
            for pf in fornecedores:
                produto_origem = str(pf.get("produto"))
                fornecedor_origem = str(pf.get("fornecedor"))
                produto_obj = produtos_map.get(produto_origem)
                if not produto_obj:
                    continue
                try:
                    f = Fornecedor.objects.get(id_origem=fornecedor_origem, tenant=self.tenant)
                    f.produtos.add(produto_obj)
                except Fornecedor.DoesNotExist:
                    continue

    def executar(self, conf):
        self.executar_produtos(conf)
        self.executar_estoques(conf)
        self.executar_fornecedores(conf)