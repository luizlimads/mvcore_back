from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from venda.models import Venda, ItemVenda, FormaPagamento
from tenant.models import Loja
from funcionario.models import Funcionario
from produto.models import Produto
from .client import VendaClient

class VendaImporter:
    def __init__(self, tenant):
        self.tenant = tenant

    def executar(self, conf):
        fim_periodo = datetime.now()

        max_data = (
            Venda.objects.filter(tenant=self.tenant)
            .aggregate(max_dt=Max("data_atualizacao_origem"))
            .get("max_dt")
        )

        if max_data:
            inicio_periodo = max_data
        else:
            inicio_periodo = datetime(2015, 1, 1)

        with VendaClient(conf) as client:
            vendas = client.fetch_vendas(inicio_periodo, fim_periodo)
            if not vendas:
                print("Nenhuma venda encontrada nesse período.")
                return

            venda_ids = [v["id_origem"] for v in vendas]

            itens = client.fetch_itens_por_vendas(venda_ids)
            pagamentos = client.fetch_pagamentos_por_vendas(venda_ids)

        lojas_qs = Loja.objects.filter(tenant=self.tenant)
        funcionarios_qs = Funcionario.objects.filter(tenant=self.tenant)
        produtos_qs = Produto.objects.filter(tenant=self.tenant)

        lojas_map = {str(l.id_origem): l.id for l in lojas_qs}
        funcionarios_map = {str(f.id_origem): f.id for f in funcionarios_qs}
        produtos_map = {str(p.id_origem): p.id for p in produtos_qs}

        vendas_dict = {}
        for v in vendas:
            key = str(v["id_origem"])
            vendas_dict[key] = {
                "id_origem": key,
                "data": v["data"],
                "status": v.get("status"),
                "numero": v.get("numero"),
                "valor_bruto": v.get("valor_bruto"),
                "acrescimo": v.get("acrescimo"),
                "desconto": v.get("desconto"),
                "valor_liquido": v.get("valor_liquido"),
                "funcionario": funcionarios_map.get(str(v.get("funcionario"))) if v.get("funcionario") is not None else None,
                "loja": lojas_map.get(str(v.get("loja"))) if v.get("loja") is not None else None,
                "data_atualizacao_origem": v.get("data"),
                "itens": [],
                "pagamentos": [],
            }

        item_ids_to_delete = set()
        all_item_ids = []
        for it in itens:
            venda_key = str(it["venda"])
            if venda_key not in vendas_dict:
                continue
            id_origem = str(it["id_origem"])
            if it.get("cancelado"):
                item_ids_to_delete.add(id_origem)
                continue
            item_normalizado = {
                "id_origem": id_origem,
                "produto": produtos_map.get(str(it.get("produto"))),
                "quantidade": it.get("quantidade"),
                "custo": it.get("custo"),
                "valor_unitario_bruto": it.get("valor_unitario_bruto"),
                "desconto": it.get("desconto"),
                "acrescimo": it.get("acrescimo"),
                "valor_unitario_liquido": it.get("valor_unitario_liquido"),
                "valor_total_liquido": it.get("valor_total_liquido"),
                "tamanho": it.get("tamanho"),
                "cor": it.get("cor"),
            }
            vendas_dict[venda_key]["itens"].append(item_normalizado)
            all_item_ids.append(id_origem)

        all_pagamento_ids = []
        for p in pagamentos:
            venda_key = str(p["venda"])
            if venda_key not in vendas_dict:
                continue
            pag_norm = {
                "id_origem": str(p["id_origem"]),
                "data": p.get("data"),
                "valor": p.get("valor"),
                "parcelas": p.get("parcelas"),
                "descricao": p.get("descricao"),
            }
            vendas_dict[venda_key]["pagamentos"].append(pag_norm)
            all_pagamento_ids.append(str(p["id_origem"]))

        vendas_list = list(vendas_dict.values())
        self._persistir_upsert(vendas_list, item_ids_to_delete, all_item_ids, all_pagamento_ids)

    def _persistir_upsert(self, vendas, item_ids_to_delete, all_item_ids, all_pagamento_ids):
        tenant = self.tenant

        ids_origem = [v["id_origem"] for v in vendas]

        existentes_qs = Venda.objects.filter(id_origem__in=ids_origem, tenant=tenant)
        existentes_map = {str(v.id_origem): v for v in existentes_qs}

        vendas_para_update = []
        vendas_para_create = []

        for v in vendas:
            exist = existentes_map.get(v["id_origem"])
            if exist:
                exist.data = v.get("data") or exist.data
                exist.status = v.get("status") or exist.status
                exist.numero = v.get("numero") or exist.numero
                exist.valor_bruto = v.get("valor_bruto") if v.get("valor_bruto") is not None else exist.valor_bruto
                exist.acrescimo = v.get("acrescimo") if v.get("acrescimo") is not None else exist.acrescimo
                exist.desconto = v.get("desconto") if v.get("desconto") is not None else exist.desconto
                exist.valor_liquido = v.get("valor_liquido") if v.get("valor_liquido") is not None else exist.valor_liquido
                exist.funcionario_id = v.get("funcionario") or exist.funcionario_id
                exist.loja_id = v.get("loja") or exist.loja_id
                exist.data_atualizacao_origem = v.get("data_atualizacao_origem") or exist.data_atualizacao_origem
                vendas_para_update.append(exist)
            else:
                vendas_para_create.append(
                    Venda(
                        id_origem=v["id_origem"],
                        data=v.get("data"),
                        status=v.get("status"),
                        numero=v.get("numero"),
                        valor_bruto=v.get("valor_bruto"),
                        acrescimo=v.get("acrescimo"),
                        desconto=v.get("desconto"),
                        valor_liquido=v.get("valor_liquido"),
                        funcionario_id=v.get("funcionario"),
                        loja_id=v.get("loja"),
                        tenant_id=tenant,
                        data_atualizacao_origem=v.get("data"),
                    )
                )

        with transaction.atomic():
            if vendas_para_create:
                Venda.objects.bulk_create(vendas_para_create, batch_size=500)

            if vendas_para_update:
                Venda.objects.bulk_update(
                    vendas_para_update,
                    [
                        "data",
                        "status",
                        "numero",
                        "valor_bruto",
                        "acrescimo",
                        "desconto",
                        "valor_liquido",
                        "funcionario_id",
                        "loja_id",
                        "data_atualizacao_origem",
                    ],
                    batch_size=500,
                )

            todas_vendas = {
                str(v.id_origem): v
                for v in Venda.objects.filter(id_origem__in=ids_origem, tenant=tenant)
            }

            if item_ids_to_delete:
                ItemVenda.objects.filter(id_origem__in=list(item_ids_to_delete), tenant=tenant).delete()

            existing_items_qs = ItemVenda.objects.filter(id_origem__in=all_item_ids, tenant=tenant)
            existing_items_map = {str(it.id_origem): it for it in existing_items_qs}

            items_to_create = []
            items_to_update = []

            for v in vendas:
                venda_obj = todas_vendas.get(v["id_origem"])
                if not venda_obj:
                    continue

                for it in v.get("itens", []):
                    if it.get("produto") is None:
                        continue

                    exist_it = existing_items_map.get(it["id_origem"])
                    if exist_it:
                        exist_it.venda = venda_obj
                        exist_it.produto_id = it["produto"]
                        exist_it.quantidade = it.get("quantidade") or 0
                        exist_it.custo = it.get("custo") or 0.0
                        exist_it.valor_unitario_bruto = it.get("valor_unitario_bruto") or 0.0
                        exist_it.desconto = it.get("desconto") or 0.0
                        exist_it.acrescimo = it.get("acrescimo") or 0.0
                        exist_it.valor_unitario_liquido = it.get("valor_unitario_liquido") or 0.0
                        exist_it.valor_total_liquido = it.get("valor_total_liquido") or 0.0
                        exist_it.tamanho = it["tamanho"]
                        exist_it.cor = it["cor"]
                        items_to_update.append(exist_it)
                    else:
                        items_to_create.append(
                            ItemVenda(
                                venda=venda_obj,
                                produto_id=it["produto"],
                                id_origem=it["id_origem"],
                                quantidade=it.get("quantidade") or 0,
                                custo=it.get("custo") or 0.0,
                                valor_unitario_bruto=it.get("valor_unitario_bruto") or 0.0,
                                desconto=it.get("desconto") or 0.0,
                                acrescimo=it.get("acrescimo") or 0.0,
                                imposto_aliquota=it.get("imposto_aliquota") or 0.0,
                                valor_unitario_liquido=it.get("valor_unitario_liquido") or 0.0,
                                valor_total_liquido=it.get("valor_total_liquido") or 0.0,
                                tamanho=it["tamanho"],
                                cor=it["cor"],
                                tenant_id=tenant,
                            )
                        )

            if items_to_create:
                ItemVenda.objects.bulk_create(items_to_create, batch_size=1000)
            if items_to_update:
                ItemVenda.objects.bulk_update(
                    items_to_update,
                    [
                        "venda",
                        "produto_id",
                        "quantidade",
                        "custo",
                        "valor_unitario_bruto",
                        "desconto",
                        "acrescimo",
                        "valor_unitario_liquido",
                        "valor_total_liquido",
                        "tamanho",
                        "cor"
                    ],
                    batch_size=1000,
                )

            existing_pags_qs = FormaPagamento.objects.filter(id_origem__in=all_pagamento_ids, tenant=tenant)
            existing_pags_map = {str(p.id_origem): p for p in existing_pags_qs}

            pags_to_create = []
            pags_to_update = []

            for v in vendas:
                venda_obj = todas_vendas.get(v["id_origem"])
                if not venda_obj:
                    continue
                for p in v.get("pagamentos", []):
                    exist_p = existing_pags_map.get(p["id_origem"])
                    if exist_p:
                        exist_p.venda = venda_obj
                        exist_p.data = p.get("data") or exist_p.data
                        exist_p.valor = p.get("valor") or exist_p.valor
                        exist_p.parcelas = p.get("parcelas") or exist_p.parcelas
                        exist_p.descricao = p.get("descricao") or exist_p.descricao
                        pags_to_update.append(exist_p)
                    else:
                        pags_to_create.append(
                            FormaPagamento(
                                venda=venda_obj,
                                id_origem=p["id_origem"],
                                data=p.get("data"),
                                valor=p.get("valor") or 0.0,
                                parcelas=p.get("parcelas") or 1,
                                descricao=p.get("descricao") or "",
                                tenant_id=tenant,
                            )
                        )

            if pags_to_create:
                FormaPagamento.objects.bulk_create(pags_to_create, batch_size=500)
            if pags_to_update:
                FormaPagamento.objects.bulk_update(
                    pags_to_update, ["venda", "data", "valor", "parcelas", "descricao"], batch_size=500
                )

        return {
            "vendas_processadas": len(vendas),
            "itens_deletados": len(item_ids_to_delete),
            "itens_criados": len(items_to_create),
            "itens_atualizados": len(items_to_update),
            "pagamentos_criados": len(pags_to_create),
            "pagamentos_atualizados": len(pags_to_update),
            "vendas_criadas": len(vendas_para_create),
            "vendas_atualizadas": len(vendas_para_update),
        }
