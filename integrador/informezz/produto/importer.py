from .client import ProdutoClient
from produto.models import Produto
from fornecedor.models import Fornecedor
from integrador.tools import clean_doc, deep_get

class ProdutoImporter:
    BATCH_PAGINAS = 10

    def __init__(self, tenant, api_key):
        self.tenant = tenant
        self.client = ProdutoClient(api_key)

    def _processar_lote(self, paginas):
        if not paginas:
            return

        ids_origem_lote = {
            str(product["productId"])
            for pagina in paginas
            for item in pagina
            for product in (item.get("products") or [])
        }
        produtos_map = {
            str(p.id_origem): p 
            for p in Produto.objects.filter(tenant=self.tenant, id_origem__in=ids_origem_lote).iterator()
        }
        produtos_criar = []
        produtos_criar_origens = set()
        produtos_atualizar = []

        fornecedores_map = {
            str(f.id_origem): f 
            for f in Fornecedor.objects.filter(tenant=self.tenant).iterator()
        }
        fornecedores_criar = []
        fornecedores_atualizar = []
        
        m2m_relacoes_novos = []
        m2m_relacoes_atualizar = []

        for pagina in paginas:
            for dado in pagina:
                produtos = dado.get("products") or []
                supplier = dado.get("supplier") or {}

                for produto in produtos:
                    produto_final = produtos_map.get(str(produto.get("productId")))

                    if produto_final:
                        produto_final.referencia = dado.get("reference")
                        produto_final.descricao = dado.get("description")
                        produto_final.grupo = deep_get(dado, "item.description")
                        produto_final.id_grupo_origem = deep_get(dado, "item.id")
                        produto_final.marca = deep_get(dado, "brand.description")
                        produto_final.id_marca_origem = deep_get(dado, "brand.id")
                        produto_final.tamanho = deep_get(produto, "size.description")
                        produto_final.cor = deep_get(dado, "color.description")
                        produto_final.departamento = deep_get(dado, "item.department.description")
                        produto_final.preco_custo = produto.get("cost")
                        produto_final.colecao = deep_get(dado, "collection.description")
                        produto_final.id_colecao_origem = deep_get(dado, "collection.id")

                        produtos_atualizar.append(produto_final)
                    else:
                        if str(produto.get("productId")) not in produtos_criar_origens:
                            produto_final = Produto(
                                tenant_id = self.tenant,
                                id_origem = str(produto.get("productId")),
                                referencia = dado.get("reference"),
                                descricao = dado.get("description"),
                                grupo = deep_get(dado, "item.description"),
                                id_grupo_origem = deep_get(dado, "item.id"),
                                marca = deep_get(dado, "brand.description"),
                                id_marca_origem = deep_get(dado, "brand.id"),
                                tamanho = deep_get(produto, "size.description"),
                                cor = deep_get(dado, "color.description"),
                                departamento = deep_get(dado, "item.department.description"),
                                preco_custo = produto.get("cost"),
                                colecao = deep_get(dado, "collection.description"),
                                id_colecao_origem = deep_get(dado, "collection.id")
                            )
                            produtos_criar.append(produto_final)
                            produtos_criar_origens.add(produto_final.id_origem)

                    if not supplier or not str(supplier.get("id")):
                        continue

                    fornecedor_final = fornecedores_map.get(str(supplier.get("id")))

                    if fornecedor_final:     
                        if fornecedor_final not in fornecedores_atualizar:
                            fornecedor_final.documento = clean_doc(supplier.get("cnpj"))
                            fornecedor_final.razao_social = supplier.get("name")
                            fornecedor_final.nome_fantasia = supplier.get("name")
                            fornecedores_atualizar.append(fornecedor_final)
                        
                        m2m_relacoes_atualizar.append((fornecedor_final, produto_final))
                    else:
                        fornecedor_final = next(
                            (f for f in fornecedores_criar if f.id_origem == str(supplier.get("id"))),
                            None
                        )

                        if fornecedor_final is None:
                            fornecedor_final = Fornecedor(
                                tenant_id = self.tenant,
                                id_origem = str(supplier.get("id")),
                                documento = clean_doc(supplier.get("cnpj")),
                                razao_social = supplier.get("name"),
                                nome_fantasia = supplier.get("name")
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
                    "tamanho",
                    "cor",
                    "departamento",
                    "preco_custo"
                ]
            )

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

    def executar(self, page_start = 1, page_end = None):
        buffer_paginas = []
        
        for pagina in self.client.obter_dados(page_start, page_end):
            buffer_paginas.append(pagina)

            if len(buffer_paginas) >= self.BATCH_PAGINAS:
                self._processar_lote(buffer_paginas)
                buffer_paginas.clear()

        if buffer_paginas:
            self._processar_lote(buffer_paginas)
        
        return 0

    def obter_total_paginas(self):
        return self.client.obter_total_paginas()
