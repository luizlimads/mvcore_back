from integrador.ssotica.settings import SISTEMA_INTEGRADO
from integrador.permissions import TenantPertenceAoSistemaPermission
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .importer import VendaImporter
from tenant.models import Loja

class EmptySerializer(serializers.Serializer):
    pass

class VendaView(APIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated, TenantPertenceAoSistemaPermission]
    sistema_integrado = SISTEMA_INTEGRADO
    
    def post(self, request):
        loja = Loja.objects.filter(tenant=request.user.tenant.id).first()
        importador = VendaImporter(
            tenant=request.user.tenant.id,
            token=request.user.tenant.api_token,
            loja=loja.id,
            cnpj=request.user.tenant.api_document,
            aliquota=loja.imposto_aliquota_padrao)
        try:
            importador.executar()
            return Response({"mensagem": "Importação Venda concluída com sucesso."})
        except Exception as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)
