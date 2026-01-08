from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Produto, Estoque
from .serializers import ProdutoSerializer, EstoqueSerializer

class ProdutoList(generics.ListCreateAPIView):
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Produto.objects.filter(tenant=self.request.user.tenant)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = self.request.user.tenant
        return context

class ProdutoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Produto.objects.filter(tenant=self.request.user.tenant)

class EstoqueList(generics.ListCreateAPIView):
    serializer_class = EstoqueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Estoque.objects.filter(tenant=self.request.user.tenant)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = self.request.user.tenant
        return context

class EstoqueDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EstoqueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Estoque.objects.filter(tenant=self.request.user.tenant)
