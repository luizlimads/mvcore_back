from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Venda
from .serializers import VendaSerializer, VendaCreateSerializer

class VendaList(generics.ListCreateAPIView):
    serializer_class = VendaSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VendaCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Venda.objects.prefetch_related('itens__produto', 'formas_pagamento').filter(tenant=self.request.user.tenant)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = self.request.user.tenant
        return context

class VendaDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VendaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Venda.objects.filter(tenant=self.request.user.tenant)
