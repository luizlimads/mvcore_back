from datetime import date
from integrador.tools import parse_dt, clean_doc, DEFAULT_IMPORT_DATE
from .client import VendaClient
from venda.models import Venda, ItemVenda, FormaPagamento
from produto.models import Produto
from funcionario.models import Funcionario
from funcionario.serializers import FuncionarioSerializer

class VendaImporter:
    BATCH_PAGINAS = 5

    def __init__(self, tenant, token, cnpj, loja, aliquota):
        self.tenant = tenant
        self.loja = loja
        self.aliquota = aliquota
        self.client = VendaClient(token, cnpj)

    def _processar_lote(self, paginas):
        if not paginas:
            return

        vendas_ids = {
            str(venda["id"])
            for pagina in paginas
            for venda in pagina
        }
        vendas_map = {
            str(v.id_origem): v
            for v in Venda.objects.filter(tenant=self.tenant, id_origem__in=vendas_ids).iterator()
        }

        produtos_ids = {
            str(item["produto"]["id"])
            for pagina in paginas
            for venda in pagina
            for item in (venda.get("itens") or [])
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
        vendas_criar_origens = set()
        vendas_atualizar = []
        vendas_excluir_origens = []

        produtos_criar = []
        produtos_atualizar = []

        itens_criar = []
        itens_vendas_ids = set()

        pagamentos_criar = []
        pagamentos_vendas_ids = set()

        for pagina in paginas:
            for sale in pagina:

                # Lê e grava os vendedores
                vendedor = None
                seller = sale.get("funcionario")
                if seller:
                    id_origem_vendedor = str(seller.get("id"))
                    vendedor = vendedores_map.get(id_origem_vendedor)
                    if not vendedor:
                        payload = {
                            "id_origem": id_origem_vendedor,
                            "nome": seller.get("nome"),
                            "cpf": clean_doc(seller.get("cpf")),
                            "funcao": "Vendedor",
                            "loja": self.loja
                        }
                        serializer = FuncionarioSerializer(data=payload, context={"tenant": self.tenant})
                        serializer.is_valid(raise_exception=True)
                        vendedor = serializer.save()
                        vendedores_map[id_origem_vendedor] = vendedor

                # Lê e guarda as vendas
                id_origem_venda = str(sale.get("id"))
                if sale.get("status") != 'ATIVA':
                    vendas_excluir_origens.append(id_origem_venda)
                    continue

                data = sale.get("data")
                hora = sale.get("hora")
                data_venda = parse_dt(f"{data}T{hora}")
                venda_final = vendas_map.get(id_origem_venda)

                if venda_final:
                    venda_final.data = data_venda
                    venda_final.status = "Ativa"
                    venda_final.numero = str(sale.get("numero"))
                    venda_final.valor_bruto = sale.get("valor_bruto") or 0
                    venda_final.acrescimo = sale.get("acrescimo") or 0
                    venda_final.desconto = sale.get("desconto") or 0
                    venda_final.credito_troca = sale.get("credito_troca") or 0
                    venda_final.valor_liquido = sale.get("valor_liquido") or 0
                    venda_final.loja_id = self.loja
                    venda_final.funcionario = vendedor if vendedor else None
                    vendas_atualizar.append(venda_final)
                else:
                    if id_origem_venda not in vendas_criar_origens:
                        venda_final = Venda(
                            id_origem = id_origem_venda,
                            data = data_venda,
                            status = "Ativa",
                            numero = str(sale.get("numero")),
                            valor_bruto = sale.get("valor_bruto") or 0,
                            acrescimo = sale.get("acrescimo") or 0,
                            desconto = sale.get("desconto") or 0,
                            credito_troca = sale.get("credito_troca") or 0,
                            valor_liquido = sale.get("valor_liquido") or 0,
                            tenant_id = self.tenant,
                            loja_id = self.loja,
                            funcionario = vendedor if vendedor else None
                        )
                        vendas_criar.append(venda_final)
                        vendas_criar_origens.add(id_origem_venda)

                itens = sale.get("itens") or []
                for item in itens:

                    # Lê e guarda os produtos
                    produto = item.get("produto") or {}
                    if produto:
                        id_origem_produto = str(produto.get("id"))
                        produto_final = produtos_map.get(id_origem_produto)

                        if produto_final:
                            produto_final.referencia = str(produto.get("referencia"))
                            produto_final.descricao = str(produto.get("descricao"))
                            produto_final.grupo = str(produto.get("grupo"))
                            produto_final.id_grupo_origem = str(produto.get("grupo_id"))
                            produto_final.marca = str(produto.get("grife"))
                            produto_final.id_marca_origem = str(produto.get("grife_id"))
                            produtos_atualizar.append(produto_final)
                        else:
                            produto_final = next(
                                (p for p in produtos_criar if p.id_origem == id_origem_produto),
                                None
                            )
                            if produto_final is None:
                                produto_final = Produto(
                                    id_origem = id_origem_produto,
                                    referencia = produto.get("referencia"),
                                    descricao = produto.get("descricao"),
                                    grupo = produto.get("grupo"),
                                    id_grupo_origem = str(produto.get("grupo_id")),
                                    marca = produto.get("grife"),
                                    id_marca_origem = str(produto.get("grife_id")),
                                    tenant_id = self.tenant
                                )
                                produtos_criar.append(produto_final)

                        # Lê e guarda os itens da venda
                        item_venda_final = ItemVenda(
                            venda=venda_final,
                            produto_id=produto_final.id,
                            id_origem=str(item.get("id")),
                            quantidade=float(item.get("quantidade") or 0),
                            custo=float(item.get("custo") or 0.0),
                            valor_unitario_bruto=float(item.get("valor_unitario_bruto") or 0.0),
                            desconto=float(item.get("desconto") or 0.0),
                            acrescimo=float(item.get("acrescimo") or 0.0),
                            imposto_aliquota=self.aliquota,
                            valor_unitario_liquido=float(item.get("valor_unitario_liquido") or 0.0),
                            valor_total_liquido=float(item.get("valor_total_liquido") or 0.0),
                            tenant_id=self.tenant,
                            funcionario = vendedor if vendedor else None
                        )
                        itens_criar.append(item_venda_final)
                        if venda_final.id not in itens_vendas_ids:
                            itens_vendas_ids.add(venda_final.id)

                # Lê e guarda as formas de pagamento da venda
                payments = sale.get("formas_pagamento") or []
                for payment in payments:
                    pagamento_final = FormaPagamento(
                        venda = venda_final,
                        id_origem = str(payment.get("id")),
                        data = parse_dt(sale.get("data")),
                        valor = float(payment.get("valor") or 0.0),
                        parcelas = payment.get("qtd_parcelas") or 1,
                        descricao = payment.get("forma_pagamento") or "",
                        tenant_id = self.tenant
                    )
                    pagamentos_criar.append(pagamento_final)
                    if venda_final.id not in pagamentos_vendas_ids:
                        pagamentos_vendas_ids.add(venda_final.id)

        # Grava as vendas
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
                    "loja_id","funcionario_id"
                ]
            )

        # Grava os produtos
        if produtos_criar:
            Produto.objects.bulk_create(produtos_criar)

        if produtos_atualizar:
            Produto.objects.bulk_update(
                produtos_atualizar,
                fields = [
                    "referencia",
                    "descricao",
                    "grupo",
                    "id_grupo_origem",
                    "marca",
                    "id_marca_origem"
                ]
            )

        # Grava os itens de vendas
        if itens_criar:
            ItemVenda.objects.filter(tenant=self.tenant, venda_id__in=itens_vendas_ids).delete()
            ItemVenda.objects.bulk_create(itens_criar)

        # Grava os pagamentos das vendas
        if pagamentos_criar:
            FormaPagamento.objects.filter(tenant=self.tenant, venda_id__in=pagamentos_vendas_ids).delete()
            FormaPagamento.objects.bulk_create(pagamentos_criar)

    def executar(self, data_inicio: date | None = None):
        if data_inicio is None:
            data_inicio = DEFAULT_IMPORT_DATE

        buffer_paginas = []

        for pagina in self.client.obter_dados(data_inicio):
            buffer_paginas.append(pagina)

            if len(buffer_paginas) >= self.BATCH_PAGINAS:
                self._processar_lote(buffer_paginas)
                buffer_paginas.clear()

        if buffer_paginas:
            self._processar_lote(buffer_paginas)

        return 0
