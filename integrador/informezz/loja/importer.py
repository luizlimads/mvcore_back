from integrador.tools import clean_doc
from .client import LojaClient
from tenant.models import Loja

class LojaImporter:
    def __init__(self, tenant, api_key):
        self.tenant = tenant
        self.client = LojaClient(api_key)

    def _processar_lote(self, stores):
        lojas_map = {
            str(l.id_origem): l
            for l in Loja.objects.filter(tenant=self.tenant).iterator()
        }

        lojas_criar = []
        lojas_atualizar = []

        for store in stores:
            id_origem_loja = str(store.get("id"))
            loja_final = lojas_map.get(id_origem_loja)

            if loja_final:
                loja_final.nome = store.get("name")
                loja_final.documento = clean_doc(store.get("cnpj"))
                lojas_atualizar.append(loja_final)
            else:
                loja_final = Loja(
                    tenant_id = self.tenant,
                    id_origem = id_origem_loja,
                    nome = store.get("name"),
                    documento = clean_doc(store.get("cnpj"))
                )
                lojas_criar.append(loja_final)

        if lojas_criar:
            Loja.objects.bulk_create(lojas_criar)

        if lojas_atualizar:
            Loja.objects.bulk_update(
                lojas_atualizar,
                fields=["nome","documento"]
            )

    def executar(self):
        self._processar_lote(self.client.obter_dados())

        return 0
