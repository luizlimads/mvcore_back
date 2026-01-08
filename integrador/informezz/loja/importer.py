from .client import LojaClient
from tenant.models import Loja
from tenant.serializers import LojaSerializer
import re

class LojaImporter:
    def __init__(self, tenant, api_key):
        self.tenant = tenant
        self.client = LojaClient(api_key)

    def normalizar_loja(self, dado):
        return {
            "id_origem": dado["id"],
            "nome": dado["name"],
            "documento": re.sub(r'[^0-9A-Za-z]', '', dado["cnpj"])
        }

    def salvar(self, dado, Model, Serializer):
        objeto = Model.objects.filter(id_origem=dado["id_origem"], tenant=self.tenant).first()
        if not objeto:
            serializer = Serializer(data=dado, context={"tenant": self.tenant})
            serializer.is_valid(raise_exception=True)
            objeto = serializer.save()
        return objeto
    
    def executar(self):
        dados_api = self.client.obter_dados()

        for dado in dados_api:
            json_loja = self.normalizar_loja(dado)
            self.salvar(json_loja, Loja, LojaSerializer)
