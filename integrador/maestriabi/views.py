from rest_framework import generics
from .authentication import PowerBIAuthentication
from .models import ProdutoBI, EstoqueBI, VendaBI
from .serializers import ProdutoBISerializer, EstoqueBISerializer, VendaBISerializer

class ProdutosBIView(generics.ListAPIView):
    authentication_classes = [PowerBIAuthentication]
    permission_classes = []
    serializer_class = ProdutoBISerializer
    def get_queryset(self):
        return ProdutoBI.objects.filter(tenant_id=self.request.tenant.id)

class EstoquesBIView(generics.ListAPIView):
    authentication_classes = [PowerBIAuthentication]
    permission_classes = []
    serializer_class = EstoqueBISerializer

    def get_queryset(self):
        return EstoqueBI.objects.filter(tenant_id=self.request.tenant.id)

class VendasBIView(generics.ListAPIView):
    authentication_classes = [PowerBIAuthentication]
    permission_classes = []
    serializer_class = VendaBISerializer

    def get_queryset(self):
        return VendaBI.objects.filter(tenant_id=self.request.tenant.id)
