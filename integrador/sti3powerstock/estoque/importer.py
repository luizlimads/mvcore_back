from integrador.tools import parse_dt
from datetime import datetime
from decimal import Decimal
from tenant.models import Loja
from produto.models import Produto, Estoque
from .client import EstoqueClient

class EstoqueImporter:
    def __init__(self, tenant):
        self.tenant = tenant
        self.batch_size = 1000

    def _processar_estoques(self, estoques):
        if not estoques:
            return

        lojas_map = {
            str(l.id_origem): l
            for l in Loja.objects.filter(tenant=self.tenant.id).iterator()
        }

        ids_produtos = [
            str(estoque["produto"])
            for estoque in estoques
        ]
        produtos_map = {
            str(f.id_origem): f
            for f in Produto.objects.filter(id_origem__in=ids_produtos, tenant=self.tenant.id).iterator()
        }

        estoques_criar = []
        for estoque in estoques:

            loja = lojas_map.get(str(estoque.get("loja")))
            if not loja:
                continue

            produto = produtos_map.get(str(estoque.get("produto")))
            if not produto:
                continue

            estoques_criar.append(Estoque(
                produto_id = produto.id,
                quantidade = Decimal(estoque.get("quantidade")),
                preco_venda = Decimal(estoque.get("preco_venda")),
                preco_custo = Decimal(estoque.get("preco_custo")),
                tenant_id = self.tenant.id,
                loja_id = loja.id,
                tamanho = estoque.get("tamanho"),
                cor = estoque.get("cor"),
                data_atualizacao_origem = parse_dt(estoque.get("data_atualizacao_origem"))
            ))

            if len(estoques_criar) >= self.batch_size:
                Estoque.objects.bulk_create(estoques_criar)
                estoques_criar.clear()

        if estoques_criar:
            Estoque.objects.bulk_create(estoques_criar)

    def _limpar_mes_corrente(self):
        now = datetime.now()
        Estoque.objects.filter(
            tenant=self.tenant.id,
            data_criacao__year=now.year,
            data_criacao__month=now.month
        ).delete()

    def executar(self):
        self._limpar_mes_corrente()

        with EstoqueClient(self.tenant) as client:
            self._processar_estoques(client.fetch_estoques())
        return 0
