from rest_framework import serializers
from .models import Usuario
from tenant.serializers import TenantSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer()

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'password', 'is_active', 'is_superuser', 'last_login', 'tenant']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
        }

class UsuarioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'is_active', 'tenant', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        user = Usuario(
            nome=validated_data['nome'],
            email=validated_data['email'],
            tenant=validated_data['tenant'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        campos_permitidos = ['nome', 'tenant', 'is_active']

        for attr in campos_permitidos:
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])

        senha = validated_data.pop('password', None)
        if senha:
            instance.set_password(senha)

        instance.save()
        return instance
