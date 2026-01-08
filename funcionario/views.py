from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Funcionario
from .serializers import FuncionarioSerializer

class FuncionarioList(generics.ListCreateAPIView):
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Funcionario.objects.filter(tenant=self.request.user.tenant)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = self.request.user.tenant
        return context

class FuncionarioDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Funcionario.objects.filter(tenant=self.request.user.tenant)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = self.request.user.tenant
        return context
    
