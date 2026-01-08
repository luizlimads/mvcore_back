from .client import LojaClient
from tenant.models import Loja
from tenant.serializers import LojaSerializer
from fornecedor.models import Fornecedor
from fornecedor.serializers import FornecedorSerializer
from funcionario.models import Funcionario
from funcionario.serializers import FuncionarioSerializer

class LojaImporter:
    def __init__(self, tenant):
        self.tenant = tenant

    def salvar(self, dado, Model, Serializer):
        objeto = Model.objects.filter(tenant=self.tenant, id_origem=dado["id_origem"]).first()

        if not objeto:
            serializer = Serializer(data=dado, context={"tenant": self.tenant})
            serializer.is_valid(raise_exception=True)
            objeto = serializer.save(tenant=self.tenant)
        return objeto

    def importar_lojas(self, conf):
        with LojaClient(conf) as client:
            lojas = client.fetch_lojas()

        for loja in lojas:
            self.salvar(loja, Loja, LojaSerializer)

    def importar_fornecedores(self, conf):
        with LojaClient(conf) as client:
            fornecedores = client.fetch_fornecedores()

        for fornecedor in fornecedores:
            self.salvar(fornecedor, Fornecedor, FornecedorSerializer)

    def importar_funcionarios(self, conf):
        with LojaClient(conf) as client:
            funcionarios = client.fetch_funcionarios()

        for funcionario in funcionarios:
            self.salvar(funcionario, Funcionario, FuncionarioSerializer)

    def executar(self, conf):
        self.importar_lojas(conf)
        self.importar_fornecedores(conf)
        self.importar_funcionarios(conf)
