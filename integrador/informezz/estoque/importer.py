from datetime import date, datetime
from integrador.tools import parse_dt, DEFAULT_IMPORT_DATE
from decimal import Decimal
from tenant.models import Loja
from produto.models import Produto, Estoque
from .client import EstoqueClient

class EstoqueImporter:
    BATCH_PAGINAS = 10

    def __init__(self, tenant, api_key):
        self.tenant = tenant
        self.api_key = api_key
        self.client = EstoqueClient(api_key)

    def _processar_lote(self, paginas):
        if not paginas:
            return

        ids_origem_lote = {
            str(item["productId"])
            for pagina in paginas
            for item in pagina
        }
        produtos_map = {
            str(p.id_origem): p
            for p in Produto.objects.filter(tenant=self.tenant, id_origem__in=ids_origem_lote).only(
                "id", "id_origem", "preco_custo", "tamanho", "cor"
            ).iterator()
        }

        lojas_map = {
            str(l.id_origem): l.id
            for l in Loja.objects.filter(tenant=self.tenant).only("id", "id_origem").iterator()
        }

        estoques_criar = []
        for pagina in paginas:
            for item in pagina:
                produto = produtos_map.get(str(item.get("productId")))
                if not produto:
                    continue

                price_map = {
                    str(p.get("storeId")): p.get("price")
                    for p in (item.get("prices") or [])
                }

                for store in (item.get("stores") or []):
                    loja_id = lojas_map.get(str(store.get("storeId")))
                    if not loja_id:
                        continue

                    movimentations = store.get("movimentations")
                    data_atualizacao = parse_dt(movimentations[-1].get("stockMovimentationDate")) if movimentations else parse_dt(str(datetime.now()))

                    quantidade = Decimal(str(store.get("amount") or 0))
                    preco_venda = Decimal(str(price_map.get(str(store.get("storeId")), "0")))

                    estoques_criar.append(
                        Estoque(
                            produto_id = produto.id,
                            quantidade = quantidade,
                            preco_venda = preco_venda,
                            preco_custo = produto.preco_custo,
                            tenant_id = self.tenant,
                            loja_id = loja_id,
                            tamanho = produto.tamanho,
                            cor = produto.cor,
                            data_atualizacao_origem = data_atualizacao
                        )
                    )

        if estoques_criar:
            Estoque.objects.bulk_create(estoques_criar)

    def limpar_mes_corrente(self):
        now = datetime.now()
        Estoque.objects.filter(
            tenant=self.tenant,
            data_criacao__year=now.year,
            data_criacao__month=now.month
        ).delete()

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