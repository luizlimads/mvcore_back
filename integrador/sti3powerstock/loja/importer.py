from .client import LojaClient
from tenant.models import Loja
from funcionario.models import Funcionario

class LojaImporter:
    def __init__(self, tenant):
        self.tenant = tenant

    def _processar_lojas(self, lojas):
        if not lojas:
            return

        lojas_map = {
            str(l.id_origem): l
            for l in Loja.objects.filter(tenant=self.tenant).iterator()
        }
        lojas_criar = []
        lojas_atualizar = []

        for loja in lojas:
            loja_final = lojas_map.get(str(loja.get("id_origem")))

            if loja_final:
                loja_final.nome = loja.get("nome")
                loja_final.documento = loja.get("documento")
                lojas_atualizar.append(loja_final)
            else:
                loja_final = Loja(
                    tenant_id = self.tenant.id,
                    id_origem = str(loja.get("id_origem")),
                    nome = loja.get("nome"),
                    documento = loja.get("documento")
                )
                lojas_criar.append(loja_final)

        if lojas_criar:
            Loja.objects.bulk_create(lojas_criar)

        if lojas_atualizar:
            Loja.objects.bulk_update(
                lojas_atualizar,
                fields=["nome","documento"]
            )

    def _processar_funcionarios(self, funcionarios):
        if funcionarios is None:
            return

        funcionarios_map = {
            str(f.id_origem): f
            for f in Funcionario.objects.filter(tenant=self.tenant).iterator()
        }
        funcionarios_criar = []
        funcionarios_atualizar = []

        for funcionario in funcionarios:
            funcionario_final = funcionarios_map.get(str(funcionario.get("id_origem")))

            if funcionario_final:
                funcionario_final.nome = funcionario.get("nome")
                funcionario_final.funcao = funcionario.get("funcao")
                funcionarios_atualizar.append(funcionario_final)
            else:
                funcionario_final = Funcionario(
                    tenant_id = self.tenant.id,
                    id_origem = str(funcionario.get("id_origem")),
                    nome = funcionario.get("nome"),
                    funcao = funcionario.get("funcao")
                )
                funcionarios_criar.append(funcionario_final)

        if funcionarios_criar:
            Funcionario.objects.bulk_create(funcionarios_criar)

        if funcionarios_atualizar:
            Funcionario.objects.bulk_update(
                funcionarios_atualizar,
                fields=["nome","funcao"]
            )

    def executar(self):
        with LojaClient(self.tenant) as client:
            self._processar_lojas(client.fetch_lojas())
            self._processar_funcionarios(client.fetch_funcionarios())
        return 0
