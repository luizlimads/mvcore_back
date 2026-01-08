from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ProdutoBI, EstoqueBI, VendaBI
from .serializers import ProdutoBISerializer, EstoqueBISerializer, VendaBISerializer

class ProdutosBIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProdutoBISerializer
    def get_queryset(self):
        return ProdutoBI.objects.filter(tenant_id=self.request.user.tenant.id)

class EstoquesBIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EstoqueBISerializer

    def get_queryset(self):
        return EstoqueBI.objects.filter(tenant_id=self.request.user.tenant.id)

class VendasBIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendaBISerializer

    def get_queryset(self):
        return VendaBI.objects.filter(tenant_id=self.request.user.tenant.id)
