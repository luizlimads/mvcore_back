from datetime import date
from integrador.tools import parse_dt, DEFAULT_IMPORT_DATE
from .client import FinanceiroClient
from financeiro.models import *
from financeiro.serializers import *
from venda.models import Venda
from fornecedor.models import Fornecedor

class FinanceiroImporter:
    BATCH_PAGINAS = 5

    def __init__(self, tenant, token, cnpj):
        self.tenant = tenant
        self.client = FinanceiroClient(token, cnpj)

    def _processar_lote(self, paginas):
        if not paginas:
            return

        bancos_map = {
            b.codigo: b
            for b in InstituicaoFinanceira.objects.filter(tenant=self.tenant).iterator()
        }

        contas_map = {
            str(c.id_origem): c
            for c in ContaFinanceira.objects.filter(tenant=self.tenant).iterator()
        }

        categorias_map = {
            str(t.id_origem): t
            for t in CategoriaFinanceira.objects.filter(tenant=self.tenant).iterator()
        }

        lancamentos_ids = {
            str(lancamento["id"])
            for pagina in paginas
            for lancamento in pagina
        }
        lancamentos_map = {
            str(l.id_origem): l
            for l in Lancamento.objects.filter(tenant=self.tenant, id_origem__in=lancamentos_ids).iterator()
        }

        vendas_ids = {
            str(lancamento["venda"]["id"])
            for pagina in paginas
            for lancamento in pagina
            if lancamento.get("venda") and lancamento["venda"].get("id")
        }
        vendas_map = {
            str(v.id_origem): v.id
            for v in Venda.objects.filter(tenant=self.tenant, id_origem__in=vendas_ids).iterator()
        }

        fornecedor_map = {
            str(f.id_origem): f.id
            for f in Fornecedor.objects.filter(tenant=self.tenant).iterator()
        }

        lancamentos_criar = []
        lancamentos_criar_origens = set()
        lancamentos_atualizar = []

        for pagina in paginas:
            for item in pagina:

                # Processa contas
                account = item.get("conta") or {}
                if account:
                    # Lê e grava os bancos
                    bank = account.get("banco") or {}
                    if bank:
                        banco_final = bancos_map.get(bank.get("codigo"))

                        if not banco_final:
                            payload = {
                                "codigo": bank.get("codigo"),
                                "nome": bank.get("nome")
                            }

                            serializer = InstituicaoFinanceiraSerializer(data=payload, context={"tenant": self.tenant})
                            serializer.is_valid(raise_exception=True)
                            banco_final = serializer.save()
                            bancos_map[bank.get("codigo")] = banco_final

                    # Lê e grava as contas
                    conta_final = contas_map.get(str(account.get("id")))

                    if not conta_final:
                        payload = {
                            "id_origem": str(account.get("id")),
                            "descricao": account.get("descricao"),
                            "agencia": account.get("agencia"),
                            "conta": account.get("conta"),
                            "digito_verificador": account.get("digito_conta"),
                            "instituicao_financeira": banco_final.id if banco_final else None
                        }

                        serializer = ContaFinanceiraSerializer(data=payload, context={"tenant": self.tenant})
                        serializer.is_valid(raise_exception=True)
                        conta_final = serializer.save()
                        contas_map[str(account.get("id"))] = conta_final

                # Processa categorias
                categoria_final = None
                category = item.get("categoria") or {}
                if category:

                    # Lê e grava a categoria pai
                    top_category = category.get("conta_pai") or {}
                    if top_category:
                        categoria_pai_final = categorias_map.get(str(top_category.get("id")))
                        if not categoria_pai_final:
                            if top_category.get("tipo") == None: tipo = TipoCategoriaChoices.NAO_IDENTIFICADO
                            elif top_category.get("tipo") == "CREDITO": tipo = TipoCategoriaChoices.ENTRADAS
                            elif top_category.get("tipo") == 'DEBITO': tipo = TipoCategoriaChoices.SAIDAS

                            payload = {
                                "id_origem": str(top_category.get("id")),
                                "descricao": top_category.get("descricao"),
                                "tipo": tipo
                            }

                            serializer = CategoriaFinanceiraSerializer(data=payload, context={"tenant": self.tenant})
                            serializer.is_valid(raise_exception=True)
                            categoria_pai_final = serializer.save()
                            categorias_map[str(top_category.get("id"))] = categoria_pai_final

                    # Lê e grava a categoria principal
                    categoria_final = categorias_map.get(str(category.get("id")))

                    if not categoria_final:
                        if category.get("tipo") == None: tipo = TipoCategoriaChoices.NAO_IDENTIFICADO
                        elif category.get("tipo") == "CREDITO": tipo = TipoCategoriaChoices.ENTRADAS
                        elif category.get("tipo") == 'DEBITO': tipo = TipoCategoriaChoices.SAIDAS

                        payload = {
                            "id_origem": str(category.get("id")),
                            "descricao": category.get("descricao"),
                            "tipo": tipo,
                            "categoria_pai": categoria_pai_final.id
                        }

                        serializer = CategoriaFinanceiraSerializer(data=payload, context={"tenant": self.tenant})
                        serializer.is_valid(raise_exception=True)
                        categoria_final = serializer.save()
                        categorias_map[str(category.get("id"))] = categoria_final

                # Lê e guarda os lançamentos
                venda_final = None
                sale = item.get("venda") or {}
                if sale:
                    venda_final = vendas_map.get(str(sale.get("id")))

                fornecedor_final = None
                supplier = item.get("fornecedor") or {}
                if supplier:
                    fornecedor_final = fornecedor_map.get(str(supplier.get("id")))

                if item.get("tipo") == None: tipo = TipoLancamentoChoices.NAO_IDENTIFICADO
                elif item.get("tipo") == "CREDITO": tipo = TipoLancamentoChoices.CREDITO
                elif item.get("tipo") == 'DEBITO': tipo = TipoLancamentoChoices.DEBITO

                id_origem_lancamento = str(item.get("id"))
                lancamento_final = lancamentos_map.get(id_origem_lancamento)

                if lancamento_final:
                    lancamento_final.data_competencia = parse_dt(item.get("data_operacao"))
                    lancamento_final.data_lancamento = parse_dt(item.get("data_credito"))
                    lancamento_final.valor = item.get("valor")
                    lancamento_final.tipo = tipo
                    lancamento_final.descricao = item.get("descricao")
                    lancamento_final.venda_id = venda_final if venda_final else None
                    lancamento_final.conta = conta_final
                    lancamento_final.categoria = categoria_final
                    lancamento_final.fornecedor_id = fornecedor_final if fornecedor_final else None
                    lancamentos_atualizar.append(lancamento_final)
                else:
                    if id_origem_lancamento not in lancamentos_criar_origens:
                        lancamentos_criar.append(
                            Lancamento(
                                id_origem = id_origem_lancamento,
                                data_competencia = parse_dt(item.get("data_operacao")),
                                data_lancamento = parse_dt(item.get("data_credito")),
                                valor = item.get("valor"),
                                tipo = tipo,
                                descricao = item.get("descricao"),
                                venda_id = venda_final if venda_final else None,
                                conta = conta_final,
                                categoria = categoria_final,
                                fornecedor_id = fornecedor_final if fornecedor_final else None,
                                tenant_id = self.tenant
                            )
                        )
                        lancamentos_criar_origens.add(id_origem_lancamento)

        # Grava os lançamentos
        if lancamentos_criar:
            Lancamento.objects.bulk_create(lancamentos_criar)

        if lancamentos_atualizar:
            Lancamento.objects.bulk_update(
                lancamentos_atualizar,
                fields = [
                    "data_competencia", "data_lancamento", "valor",
                    "tipo", "descricao", "venda_id", "conta",
                    "categoria", "fornecedor_id"
                ]
            )

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