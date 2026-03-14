from produto.models import Produto
from .client import FornecedorClient
from fornecedor.models import Fornecedor

class FornecedorImporter:
    def __init__(self, tenant):
        self.tenant = tenant

    def _processar_fornecedores(self, fornecedores):
        if not fornecedores:
            return
        
        fornecedores_map = {
            str(f.id_origem): f
            for f in Fornecedor.objects.filter(tenant=self.tenant.id).iterator()
        }
        fornecedores_criar = []
        fornecedores_atualizar = []

        for fornecedor in fornecedores:
            fornecedor_final = fornecedores_map.get(str(fornecedor["id_origem"]))
            if fornecedor_final:
                fornecedor_final.documento = fornecedor.get("documento")
                fornecedor_final.razao_social = fornecedor.get("razao_social")
                fornecedor_final.nome_fantasia = fornecedor.get("nome_fantasia")
                fornecedores_atualizar.append(fornecedor_final)
            else:
                fornecedores_criar.append(Fornecedor(
                    id_origem = str(fornecedor["id_origem"]),
                    documento = fornecedor.get("documento"),
                    razao_social = fornecedor.get("razao_social"),
                    nome_fantasia = fornecedor.get("nome_fantasia"),
                    tenant_id = self.tenant.id
                ))

        if fornecedores_criar:
            Fornecedor.objects.bulk_create(fornecedores_criar, batch_size=500)

        if fornecedores_atualizar:
            Fornecedor.objects.bulk_update(
                fornecedores_atualizar,
                ["documento","razao_social","nome_fantasia"],
                batch_size=500
            )

    def _processar_fornecedores_produtos(self, tuplas):
        if not tuplas:
            return

        ids_produtos = [
            str(tupla["produto"])
            for tupla in tuplas
        ]
        produtos_map = {
            str(p.id_origem): p
            for p in Produto.objects.filter(id_origem__in=ids_produtos, tenant=self.tenant.id)
        }

        ids_fornecedores = [
            str(tupla["fornecedor"])
            for tupla in tuplas
        ]
        fornecedores_map = {
            str(f.id_origem): f
            for f in Fornecedor.objects.filter(id_origem__in=ids_fornecedores, tenant=self.tenant.id)
        }        

        for tupla in tuplas:
            produto = produtos_map.get(str(tupla.get("produto")))
            if not produto:
                continue

            fornecedor = fornecedores_map.get(str(tupla.get("fornecedor")))
            if fornecedor:
                fornecedor.produtos.add(produto)

    def executar(self):
        with FornecedorClient(self.tenant) as client:
            self._processar_fornecedores(client.fetch_fornecedores())
            self._processar_fornecedores_produtos(client.fetch_produtos_fornecedores())
        return 0