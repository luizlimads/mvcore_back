from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Tenant, SistemaIntegrado, Loja
from .serializers import TenantSerializer, TenantCreateSerializer, SistemaIntegradoSerializer, LojaSerializer

class SistemaIntegradoList(generics.ListCreateAPIView):
    serializer_class = SistemaIntegradoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = SistemaIntegrado.objects.all()

class SistemaIntegradoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SistemaIntegradoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = SistemaIntegrado.objects.all()

class TenantList(generics.ListCreateAPIView):
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TenantCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        sistemaintegrado = self.request.query_params.get('sistema-integrado')
        return Tenant.objects.filter(id_sistema_integrado=sistemaintegrado) if sistemaintegrado else Tenant.objects.all()

class TenantDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TenantCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        sistemaintegrado = self.request.query_params.get('sistema-integrado')
        return Tenant.objects.filter(id_sistema_integrado=sistemaintegrado) if sistemaintegrado else Tenant.objects.all()

class LojaList(generics.ListCreateAPIView):
    serializer_class = LojaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        tenant = self.request.query_params.get('tenant')
        return Loja.objects.filter(tenant=tenant) if tenant else Loja.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = self.request.user.tenant
        return context

class LojaDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LojaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        tenant = self.request.query_params.get('tenant')
        return Loja.objects.filter(tenant=tenant) if tenant else Loja.objects.all()
