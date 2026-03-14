from datetime import datetime
from integrador.tools import clean_doc
from .client import EstoqueClient
from produto.models import Produto, Estoque
from fornecedor.models import Fornecedor

class EstoqueImporter:
    BATCH_PAGINAS = 10

    def __init__(self, tenant, token, empresa, loja):
        self.tenant = tenant
        self.loja = loja
        self.client = EstoqueClient(token=token, empresa=empresa)

    def _processar_lote(self, paginas: list[list[dict]]) -> None:
        if not paginas:
            return

        ids_origem_lote = {str(item["id"]) for pagina in paginas for item in pagina}
        produtos_map = {
            str(p.id_origem): p
            for p in Produto.objects.filter(tenant=self.tenant, id_origem__in=ids_origem_lote).iterator()
        }

        produtos_criar = []
        produtos_atualizar = []
        produtos_criar_origens = set()

        estoque_criar = []

        fornecedores_map = {
            str(f.id_origem): f
            for f in Fornecedor.objects.filter(tenant=self.tenant).iterator()
        }
        fornecedores_criar = []
        fornecedores_atualizar = []

        m2m_relacoes_novos = []
        m2m_relacoes_atualizar = []

        for pagina in paginas:
            for item in pagina:
                id_origem_produto = str(item.get("id"))
                produto_final = produtos_map.get(id_origem_produto)

                if produto_final:
                    produto_final.referencia = item.get("referencia")
                    produto_final.descricao = item.get("descricao")
                    produto_final.grupo = item.get("grupo")
                    produto_final.id_grupo_origem = str(item.get("grupo_id"))
                    produto_final.marca = item.get("grife")
                    produto_final.id_marca_origem = str(item.get("grife_id"))
                    produto_final.preco_custo = item.get("custo")
                    produto_final.cor = item.get("cor")
                    produto_final.tamanho = item.get("tamanho")
                    produtos_atualizar.append(produto_final)
                else:
                    if id_origem_produto not in produtos_criar_origens:
                        produto_final = Produto(
                            id_origem = id_origem_produto,
                            referencia = item.get("referencia"),
                            descricao = item.get("descricao"),
                            grupo = item.get("grupo"),
                            id_grupo_origem = str(item.get("grupo_id")),
                            marca = item.get("grife"),
                            id_marca_origem = str(item.get("grife_id")),
                            cor = item.get("cor"),
                            tamanho = item.get("tamanho"),
                            preco_custo = item.get("custo"),
                            tenant_id = self.tenant
                        )
                        produtos_criar.append(produto_final)
                        produtos_criar_origens.add(id_origem_produto)

                estoque_criar.append(
                    Estoque(
                        produto_id = produto_final.id,
                        quantidade = item.get("estoque_atual"),
                        preco_venda = item.get("preco_venda"),
                        preco_custo = item.get("custo"),
                        cor = item.get("cor"),
                        tamanho = item.get("tamanho"),
                        loja_id = self.loja,
                        tenant_id = self.tenant
                    )
                )

                for fornecedor in item.get("fornecedores"):
                    id_origem_fornecedor = str(fornecedor.get("id"))
                    fornecedor_final = fornecedores_map.get(id_origem_fornecedor)

                    if fornecedor_final:
                        if fornecedor_final not in fornecedores_atualizar:
                            fornecedor_final.documento = clean_doc(fornecedor.get("documento"))
                            fornecedor_final.razao_social = fornecedor.get("razao_social")
                            fornecedor_final.nome_fantasia = fornecedor.get("nome_fantasia")
                            fornecedores_atualizar.append(fornecedor_final)
                        m2m_relacoes_atualizar.append((fornecedor_final, produto_final))
                    else:
                        fornecedor_final = next(
                            (f for f in fornecedores_criar if f.id_origem == id_origem_fornecedor),
                            None
                        )

                        if fornecedor_final is None:
                            fornecedor_final = Fornecedor(
                                tenant_id = self.tenant,
                                id_origem = id_origem_fornecedor,
                                documento = clean_doc(fornecedor.get("documento")),
                                razao_social = fornecedor.get("razao_social"),
                                nome_fantasia = fornecedor.get("nome_fantasia")
                            )
                            fornecedores_criar.append(fornecedor_final)
                        m2m_relacoes_novos.append((fornecedor_final, produto_final))

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
                    "id_marca_origem",
                    "cor",
                    "tamanho"
                ]
            )

        Estoque.objects.bulk_create(estoque_criar)

        if fornecedores_criar:
            Fornecedor.objects.bulk_create(fornecedores_criar)

        if fornecedores_atualizar:
            Fornecedor.objects.bulk_update(
                fornecedores_atualizar,
                fields = ["documento", "razao_social", "nome_fantasia"]
            )

        if fornecedores_criar:
            novos_map = {
                f.id_origem: f
                for f in Fornecedor.objects.filter(
                    tenant=self.tenant,
                    id_origem__in=[f.id_origem for f in fornecedores_criar]
                ).iterator()
            }
        else:
            novos_map = {}

        for fornecedor, produto in m2m_relacoes_novos:
            fornecedor_db = novos_map[fornecedor.id_origem]
            fornecedor_db.produtos.add(produto)

        for fornecedor, produto in m2m_relacoes_atualizar:
            fornecedor.produtos.add(produto)

    def _limpa_mes_atual(self):
        now = datetime.now()
        Estoque.objects.filter(
            tenant=self.tenant,
            data_criacao__year=now.year,
            data_criacao__month=now.month
        ).delete()

    def executar(self):
        self._limpa_mes_atual()

        buffer_paginas = []
        for pagina in self.client.obter_dados():
            buffer_paginas.append(pagina)

            if len(buffer_paginas) >= self.BATCH_PAGINAS:
                self._processar_lote(buffer_paginas)
                buffer_paginas.clear()

        if buffer_paginas:
            self._processar_lote(buffer_paginas)

        return 0
