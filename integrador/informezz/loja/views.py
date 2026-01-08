from integrador.informezz.settings import SISTEMA_INTEGRADO
from integrador.permissions import TenantPertenceAoSistemaPermission
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .importer import LojaImporter
from tenant.models import Loja

class EmptySerializer(serializers.Serializer):
    pass

class LojaView(APIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated, TenantPertenceAoSistemaPermission]
    sistema_integrado = SISTEMA_INTEGRADO

    def post(self, request):
        api_key = request.user.tenant.api_key

        importador = LojaImporter(tenant=request.user.tenant.id, api_key=api_key)
        try:
            importador.executar()

            return Response({"mensagem": "Importação concluída com sucesso."})
        except Exception as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)
