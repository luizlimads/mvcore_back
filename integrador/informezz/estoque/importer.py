from datetime import datetime
from integrador.tools import parse_dt
from decimal import Decimal
from tenant.models import Loja
from produto.models import Produto, Estoque
from .client import EstoqueClient

class EstoqueImporter:
    def __init__(self, tenant, api_key):
        self.tenant = tenant
        self.api_key = api_key
        self.client = EstoqueClient(api_key)

    def processar_lote(self, paginas):
        if not paginas:
            return

        produtos_map = {
            str(p.id_origem): p
            for p in Produto.objects.filter(tenant=self.tenant).only(
                "id", "id_origem", "preco_custo", "tamanho", "cor"
            ).iterator()
        }

        lojas_map = {
            str(l.id_origem): l.id
            for l in Loja.objects.filter(tenant=self.tenant).only("id", "id_origem").iterator()
        }

        novos = []
        append_novo = novos.append

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

                    append_novo(
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

        if novos:
            Estoque.objects.bulk_create(novos)
    
    def executar(self):
        now = datetime.now()
        Estoque.objects.filter(
            tenant=self.tenant,
            data_criacao__year=now.year,
            data_criacao__month=now.month
        ).delete()        

        buffer_paginas = []
        for pagina in self.client.obter_dados():
            buffer_paginas.append(pagina)

            if len(buffer_paginas) == 30:
                lote = buffer_paginas
                buffer_paginas = []
                self.processar_lote(lote)

        if buffer_paginas:
            lote = buffer_paginas
            self.processar_lote(lote)
        return