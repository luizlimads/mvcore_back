from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Fornecedor
from .serializers import FornecedorSerializer

class FornecedorList(generics.ListCreateAPIView):
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Fornecedor.objects.filter(tenant=self.request.user.tenant)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = self.request.user.tenant
        return context

class FornecedorDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Fornecedor.objects.filter(tenant=self.request.user.tenant)
