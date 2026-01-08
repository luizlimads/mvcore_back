from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer

class UsuarioList(generics.ListCreateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UsuarioCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Usuario.objects.all()

class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UsuarioCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Usuario.objects.all()
        return Usuario.objects.filter(id=self.request.user.id)
