from integrador.tools import parse_dt, DEFAULT_IMPORT_DATE
from decimal import Decimal
from django.db.models import Max
from datetime import timedelta
from venda.models import Venda, ItemVenda, FormaPagamento
from tenant.models import Loja
from funcionario.models import Funcionario
from produto.models import Produto
from .client import VendaClient

class VendaImporter:
    def __init__(self, tenant):
        self.tenant = tenant

    def _processar_vendas(self, vendas):
        if not vendas:
            return

        lojas_map = {
            str(l.id_origem): l
            for l in Loja.objects.filter(tenant=self.tenant.id).iterator()
        }

        funcionarios_map = {
            str(f.id_origem): f
            for f in Funcionario.objects.filter(tenant=self.tenant).iterator()
        }

        venda_ids = [
            str(venda["id_origem"])
            for venda in vendas
        ]
        vendas_map = {
            str(v.id_origem): v
            for v in Venda.objects.filter(id_origem__in=venda_ids, tenant=self.tenant.id).iterator()
        }

        vendas_criar = []
        vendas_atualizar = []

        for venda in vendas:
            loja = lojas_map.get(str(venda["loja"]))
            funcionario = funcionarios_map.get(str(venda["funcionario"]))

            venda_final = vendas_map.get(str(venda["id_origem"]))
            if venda_final:
                venda_final.data = parse_dt(venda["data"])
                venda_final.status = venda["status"]
                venda_final.numero = venda["numero"]
                venda_final.valor_bruto = Decimal(venda["valor_bruto"])
                venda_final.acrescimo = Decimal(venda["acrescimo"])
                venda_final.desconto = Decimal(venda["desconto"])
                venda_final.valor_liquido = Decimal(venda["valor_liquido"])
                venda_final.funcionario_id = funcionario.id
                venda_final.loja_id = loja.id
                venda_final.data_atualizacao_origem = parse_dt(venda["data"])
                vendas_atualizar.append(venda_final)
            else:
                vendas_criar.append(Venda(
                    id_origem = venda["id_origem"],
                    data = parse_dt(venda["data"]),
                    status = venda["status"],
                    numero = venda["numero"],
                    valor_bruto = Decimal(venda["valor_bruto"]),
                    acrescimo = Decimal(venda["acrescimo"]),
                    desconto = Decimal(venda["desconto"]),
                    valor_liquido = Decimal(venda["valor_liquido"]),
                    funcionario_id = funcionario.id,
                    tenant = self.tenant,
                    loja_id = loja.id,
                    data_atualizacao_origem = parse_dt(venda["data"])
                ))

        if vendas_criar:
            Venda.objects.bulk_create(vendas_criar, batch_size=500)

        if vendas_atualizar:
            Venda.objects.bulk_update(
                vendas_atualizar,
                ["data","status","numero","valor_bruto","acrescimo","desconto",
                 "valor_liquido","funcionario", "loja", "data_atualizacao_origem"
                ]
                ,batch_size=500
            )

    def _processar_vendas_itens(self, itens):
        if not itens:
            return

        venda_ids = [
            str(item["venda"])
            for item in itens
        ]
        vendas_map = {
            str(v.id_origem): v
            for v in Venda.objects.filter(id_origem__in=venda_ids, tenant=self.tenant.id).iterator()
        }

        produto_ids = [
            str(item["produto"])
            for item in itens
        ]
        produtos_map = {
            str(p.id_origem): p
            for p in Produto.objects.filter(id_origem__in=produto_ids, tenant=self.tenant.id).iterator()
        }

        item_ids = [
            str(item["id_origem"])
            for item in itens
        ]
        itens_map = {
            str(i.id_origem): i
            for i in ItemVenda.objects.filter(id_origem__in=item_ids, tenant=self.tenant.id).iterator()
        }

        itens_criar = []
        itens_atualizar = []
        itens_deletar = []

        for item in itens:
            if item.get("cancelado"):
                itens_deletar.append(str(item.get("id_origem")))
                continue

            venda = vendas_map.get(str(item.get("venda")))
            if not venda:
                continue

            produto = produtos_map.get(str(item.get("produto")))
            if not produto:
                continue

            item_final = itens_map.get(str(item.get("id_origem")))
            if item_final:
                item_final.quantidade = item.get("quantidade")
                item_final.custo = item.get("custo")
                item_final.valor_unitario_bruto = item.get("valor_unitario_bruto")
                item_final.desconto = item.get("desconto")
                item_final.acrescimo = item.get("acrescimo")
                item_final.valor_unitario_liquido = item.get("valor_unitario_liquido")
                item_final.valor_total_liquido = item.get("valor_total_liquido")
                item_final.tamanho = item.get("tamanho")
                item_final.cor = item.get("cor")
                itens_atualizar.append(item_final)
            else:
                itens_criar.append(ItemVenda(
                    produto_id = produto.id,
                    venda_id = venda.id,
                    id_origem = str(item.get("id_origem")),
                    quantidade = item.get("quantidade"),
                    custo = item.get("custo"),
                    valor_unitario_bruto = item.get("valor_unitario_bruto"),
                    desconto = item.get("desconto"),
                    acrescimo = item.get("acrescimo"),
                    valor_unitario_liquido = item.get("valor_unitario_liquido"),
                    valor_total_liquido = item.get("valor_total_liquido"),
                    tamanho = item.get("tamanho"),
                    cor = item.get("cor"),
                    tenant_id = self.tenant.id
                ))

        if itens_deletar:
            ItemVenda.objects.filter(id_origem__in=itens_deletar, tenant=self.tenant.id).delete()

        if itens_criar:
            ItemVenda.objects.bulk_create(itens_criar, batch_size=500)

        if itens_atualizar:
            ItemVenda.objects.bulk_update(
                itens_atualizar,
                ["quantidade","custo","valor_unitario_bruto","desconto","acrescimo",
                 "valor_unitario_liquido","valor_total_liquido", "tamanho", "cor"
                ],
                batch_size=500
            )

    def _processar_vendas_pagamentos(self, pagamentos):
        if not pagamentos:
            return

        venda_ids = [
            str(pagamento["venda"])
            for pagamento in pagamentos
        ]
        vendas_map = {
            str(v.id_origem): v
            for v in Venda.objects.filter(id_origem__in=venda_ids, tenant=self.tenant.id).iterator()
        }

        pagamento_ids = [
            str(pagamento["id_origem"])
            for pagamento in pagamentos
        ]
        pagamentos_map = {
            str(p.id_origem): p
            for p in FormaPagamento.objects.filter(id_origem__in=pagamento_ids, tenant=self.tenant.id).iterator()
        }

        pagamentos_criar = []
        pagamentos_atualizar = []

        for pagamento in pagamentos:
            venda = vendas_map.get(str(pagamento.get("venda")))
            if not venda:
                continue

            pagamento_final = pagamentos_map.get(str(pagamento.get("id_origem")))
            if pagamento_final:
                pagamento_final.data = parse_dt(pagamento.get("data"))
                pagamento_final.valor = pagamento.get("valor")
                pagamento_final.parcelas = pagamento.get("parcelas")
                pagamento_final.descricao = pagamento.get("descricao")
                pagamentos_atualizar.append(pagamento_final)
            else:
                pagamentos_criar.append(FormaPagamento(
                    id_origem = str(pagamento.get("id_origem")),
                    data = parse_dt(pagamento.get("data")),
                    valor = pagamento.get("valor"),
                    parcelas = pagamento.get("parcelas"),
                    descricao = pagamento.get("descricao"),
                    venda_id = venda.id,
                    tenant_id = self.tenant.id
                ))

        if pagamentos_criar:
            FormaPagamento.objects.bulk_create(pagamentos_criar, batch_size=500)

        if pagamentos_atualizar:
            FormaPagamento.objects.bulk_update(
                pagamentos_atualizar,
                ["data","valor","parcelas","descricao"],
                batch_size=500
            )

    def executar(self):
        max_date = Venda.objects.filter(tenant=self.tenant.id).aggregate(max_dt=Max("data_atualizacao_origem"))["max_dt"]
        start_date = max_date-timedelta(days=365*2) if max_date else DEFAULT_IMPORT_DATE

        with VendaClient(self.tenant) as client:
            vendas = client.fetch_vendas(start_date)
            self._processar_vendas(vendas)

            venda_ids = [str(venda["id_origem"]) for venda in vendas]
            self._processar_vendas_itens(client.fetch_itens_por_vendas(venda_ids))
            self._processar_vendas_pagamentos(client.fetch_pagamentos_por_vendas(venda_ids))
        return 0