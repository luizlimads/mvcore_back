from integrador.tools import parse_dt, DEFAULT_IMPORT_DATE
from venda.models import Venda, ItemVenda, FormaPagamento
from funcionario.models import Funcionario
from produto.models import Produto
from tenant.models import Loja
from funcionario.serializers import FuncionarioSerializer
from .client import VendaClient

class VendaImporter:
    BATCH_PAGINAS = 10

    def __init__(self, tenant, api_key):
        self.tenant = tenant
        self.client = VendaClient(api_key)

    def _processar_lote(self, paginas):
        if not paginas:
            return

        lojas_map = {
            str(l.id_origem): l.id
            for l in Loja.objects.filter(tenant=self.tenant).only("id", "id_origem").iterator()
        }

        ids_origem_lote = {
            str(item["id"])
            for pagina in paginas
            for item in pagina
        }
        vendas_map = {
            str(v.id_origem): v
            for v in Venda.objects.filter(tenant=self.tenant, id_origem__in=ids_origem_lote).iterator()
        }

        venda_ids = [v.id for v in vendas_map.values()]
        itens_vendas_map = {
            str(i.id_origem): i
            for i in ItemVenda.objects.filter(tenant=self.tenant, venda_id__in=venda_ids).iterator()
        }

        produtos_ids = {
            str(produto["product"]["productId"])
            for pagina in paginas
            for venda in pagina
            for produto in (venda.get("products") or [])
            if produto.get("product") and produto["product"].get("productId")
        }
        produtos_map = {
            str(p.id_origem): p
            for p in Produto.objects.filter(tenant=self.tenant, id_origem__in=produtos_ids).iterator()
        }

        vendedores_map = {
            str(v.id_origem): v 
            for v in Funcionario.objects.filter(tenant=self.tenant).iterator()
        }

        vendas_criar = []
        vendas_atualizar = []
        vendas_excluir_origens = []

        itens_criar = []
        itens_atualizar = []

        pagamentos_criar = []
        pagamentos_criar_ids = set()

        for pagina in paginas:
            for sale in pagina:

                id_origem_venda = str(sale.get("id"))
                if sale.get("isDeleted"):
                    vendas_excluir_origens.append(id_origem_venda)
                    continue

                loja_id = lojas_map.get(str(sale.get("storeId")))
                data_venda = parse_dt(sale.get("dateTime"))

                venda_final = vendas_map.get(id_origem_venda)

                if venda_final:
                    venda_final.data = data_venda
                    venda_final.status = "Ativa"
                    venda_final.valor_bruto = (sale.get("netValue") or 0) + (sale.get("discount") or 0) - (sale.get("addition") or 0)
                    venda_final.acrescimo = sale.get("addition") or 0
                    venda_final.desconto = sale.get("discount") or 0
                    venda_final.credito_troca = sale.get("creditUsed") or 0
                    venda_final.valor_liquido = sale.get("netValue") or 0
                    venda_final.loja_id = loja_id
                    venda_final.data_atualizacao_origem = data_venda
                    vendas_atualizar.append(venda_final)
                else:
                    venda_final = next(
                        (v for v in vendas_criar if v.id_origem == id_origem_venda),
                        None
                    )
                    if venda_final is None:
                        venda_final = Venda(
                            id_origem = id_origem_venda,
                            data = data_venda,
                            status = "Ativa",
                            valor_bruto = (sale.get("netValue") or 0) + (sale.get("discount") or 0) - (sale.get("addition") or 0),
                            acrescimo = sale.get("addition") or 0,
                            desconto = sale.get("discount") or 0,
                            credito_troca = sale.get("creditUsed") or 0,
                            valor_liquido = sale.get("netValue") or 0,
                            tenant_id = self.tenant,
                            loja_id = loja_id,
                            data_atualizacao_origem = data_venda
                        )
                        vendas_criar.append(venda_final)

                items = sale.get("products") or []
                for item in items:

                    seller = item.get("seller") or {}
                    if seller:
                        vendedor = vendedores_map.get(str(seller.get("id")))
                        if not vendedor:
                            payload = {
                                "id_origem": str(seller.get("id")),
                                "nome": seller.get("name"),
                                "funcao": "Vendedor",
                                "loja": venda_final.loja_id
                            }
                            serializer = FuncionarioSerializer(data=payload, context={"tenant": self.tenant})
                            serializer.is_valid(raise_exception=True)
                            vendedor = serializer.save()
                            vendedores_map[str(seller.get("id"))] = vendedor

                    prod_info = item.get("product") or {}
                    produto = produtos_map.get(str(prod_info.get("productId")))
                    if not produto:
                        continue

                    id_origem_item = str(item.get("id"))
                    item_venda_final = itens_vendas_map.get(id_origem_item)

                    if item_venda_final:
                        item_venda_final.quantidade = float(item.get("quantity") or 0)
                        item_venda_final.custo = float(item.get("cost") or 0.0)
                        item_venda_final.valor_unitario_bruto = float(item.get("price") or 0.0)
                        item_venda_final.desconto = float(item.get("discount") or 0.0)
                        item_venda_final.acrescimo = 0
                        item_venda_final.valor_unitario_liquido = (float(item.get("netValue") or 0.0) / float(item.get("quantity") or 1))
                        item_venda_final.valor_total_liquido = float(item.get("netValue") or 0.0)
                        item_venda_final.tamanho = produto.tamanho
                        item_venda_final.cor = produto.cor
                        item_venda_final.funcionario_id = vendedor.id
                        item_venda_final.trocado = item.get("isExchanged")
                        itens_atualizar.append(item_venda_final)
                    else:
                        item_venda_final = ItemVenda(
                            venda=venda_final,
                            produto_id=produto.id,
                            id_origem=str(item.get("id")),
                            quantidade=float(item.get("quantity") or 0),
                            custo=float(item.get("cost") or 0.0),
                            valor_unitario_bruto=float(item.get("price") or 0.0),
                            desconto=float(item.get("discount") or 0.0),
                            acrescimo=0,
                            imposto_aliquota=0,
                            valor_unitario_liquido=(float(item.get("netValue") or 0.0) / float(item.get("quantity") or 1)),
                            valor_total_liquido=float(item.get("netValue") or 0.0),
                            tamanho=produto.tamanho,
                            cor=produto.cor,
                            tenant_id=self.tenant,
                            funcionario_id = vendedor.id,
                            trocado = item.get("isExchanged")
                        )
                        itens_criar.append(item_venda_final)

                payments = sale.get("payments") or []
                for payment in payments:
                    pagamento_final = FormaPagamento(
                        venda=venda_final,
                        id_origem=str(payment.get("id")),
                        data=parse_dt(sale.get("dateTime")),
                        valor=float(payment.get("amount") or 0.0),
                        parcelas=payment.get("installments") or 1,
                        descricao=payment.get("description") or "",
                        tenant_id=self.tenant
                    )
                    pagamentos_criar.append(pagamento_final)
                    if venda_final.id not in pagamentos_criar_ids:
                        pagamentos_criar_ids.add(venda_final.id)

        if vendas_excluir_origens:
            Venda.objects.filter(tenant=self.tenant, id_origem__in=vendas_excluir_origens).delete()

        if vendas_criar:
            Venda.objects.bulk_create(vendas_criar)

        if vendas_atualizar:
            Venda.objects.bulk_update(
                vendas_atualizar,
                fields=[
                    "data","status","valor_bruto","acrescimo",
                    "desconto","credito_troca","valor_liquido",
                    "loja_id","data_atualizacao_origem"
                ]
            )

        if itens_criar:
            ItemVenda.objects.bulk_create(itens_criar)

        if itens_atualizar:
            ItemVenda.objects.bulk_update(
                itens_atualizar,
                fields=[
                    "quantidade", "custo", "valor_unitario_bruto", "desconto",
                    "acrescimo", "valor_unitario_liquido", "valor_total_liquido",
                    "tamanho", "cor", "funcionario_id"
                ]
            )
        if pagamentos_criar:
            FormaPagamento.objects.filter(tenant=self.tenant, venda_id__in=pagamentos_criar_ids).delete()
            FormaPagamento.objects.bulk_create(pagamentos_criar)

    def executar(self, page_start = 1, page_end = None):
        buffer_paginas = []

        for pagina in self.client.obter_dados(DEFAULT_IMPORT_DATE, page_start, page_end):
            buffer_paginas.append(pagina)

            if len(buffer_paginas) >= self.BATCH_PAGINAS:
                self._processar_lote(buffer_paginas)
                buffer_paginas.clear()

        if buffer_paginas:
            self._processar_lote(buffer_paginas)

        return 0

    def obter_total_paginas(self):
        return self.client.obter_total_paginas(DEFAULT_IMPORT_DATE)