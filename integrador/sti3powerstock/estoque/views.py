from integrador.sti3powerstock.settings import SISTEMA_INTEGRADO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from integrador.permissions import TenantPertenceAoSistemaPermission
from .importer import EstoqueImporter

class EmptySerializer(serializers.Serializer):
    pass

class EstoqueView(APIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated, TenantPertenceAoSistemaPermission]
    sistema_integrado = SISTEMA_INTEGRADO

    def post(self, request):
        conf = {
            "host": request.user.tenant.db_host,
            "port": request.user.tenant.db_port,
            "user": request.user.tenant.db_user,
            "password": request.user.tenant.db_pass,
            "database": request.user.tenant.db_name,
        }
        importador = EstoqueImporter(tenant=request.user.tenant.id)

        try:
            importador.executar(conf)
            return Response({"status": "Importação concluída com sucesso."})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
