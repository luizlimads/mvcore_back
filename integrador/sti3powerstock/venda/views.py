from integrador.sti3powerstock.settings import SISTEMA_INTEGRADO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from integrador.permissions import TenantPertenceAoSistemaPermission
from .importer import VendaImporter

class EmptySerializer(serializers.Serializer):
    pass

class VendaView(APIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated, TenantPertenceAoSistemaPermission]
    sistema_integrado = SISTEMA_INTEGRADO

    def post(self, request):
        try:
            VendaImporter(tenant=request.user.tenant).executar()
            return Response({"status": "Importação concluída com sucesso."})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
