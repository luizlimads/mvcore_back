from integrador.tools import parse_dt, DEFAULT_IMPORT_DATE
from django.db.models import Max
from produto.models import Produto
from .client import ProdutoClient

class ProdutoImporter:
    def __init__(self, tenant):
        self.tenant = tenant

    def _processar_produtos(self, produtos):
        if not produtos:
            return

        ids_origem = [
            str(produto["id_origem"])
            for produto in produtos
        ]
        produtos_map = {
            str(p.id_origem): p
            for p in Produto.objects.filter(id_origem__in=ids_origem, tenant=self.tenant.id).iterator()
        }
        produtos_criar = []
        produtos_atualizar = []

        for produto in produtos:
            produto_final = produtos_map.get(str(produto["id_origem"]))
            if produto_final:
                produto_final.referencia = produto.get("referencia")
                produto_final.descricao = produto.get("descricao")
                produto_final.grupo = produto.get("grupo")
                produto_final.id_grupo_origem = str(produto.get("id_grupo_origem"))
                produto_final.marca = produto.get("marca")
                produto_final.id_marca_origem = str(produto.get("id_marca_origem"))
                produto_final.data_atualizacao_origem = parse_dt(produto.get("data_atualizacao_origem"))
                produtos_atualizar.append(produto_final)
            else:
                produtos_criar.append(Produto(
                    id_origem = str(produto["id_origem"]),
                    referencia = produto.get("referencia"),
                    descricao = produto.get("descricao"),
                    grupo = produto.get("grupo"),
                    id_grupo_origem = str(produto.get("id_grupo_origem")),
                    marca = produto.get("marca"),
                    id_marca_origem = str(produto.get("id_marca_origem")),
                    tenant_id = self.tenant.id,
                    data_atualizacao_origem = parse_dt(produto.get("data_atualizacao_origem"))
                ))

        if produtos_criar:
            Produto.objects.bulk_create(produtos_criar, batch_size=500)

        if produtos_atualizar:
            Produto.objects.bulk_update(
                produtos_atualizar,
                ["referencia","descricao","grupo","id_grupo_origem",
                 "marca","id_marca_origem","data_atualizacao_origem"
                ],
                batch_size=500
            )

    def executar(self):
        start_date = Produto.objects.filter(tenant=self.tenant.id).aggregate(max_dt=Max("data_atualizacao_origem"))["max_dt"] or DEFAULT_IMPORT_DATE

        with ProdutoClient(self.tenant) as client:
            self._processar_produtos(client.fetch_produtos(start_date))
        return 0
