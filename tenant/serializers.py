from django.db import transaction
from rest_framework import serializers
from .models import Tenant, SistemaIntegrado, Loja
from common.serializers import TenantSerializerMixin

class SistemaIntegradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SistemaIntegrado
        fields = ['id', 'nome', 'data_criacao']

class LojaSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = Loja
        fields = ['id', 'nome', 'documento', 'imposto_aliquota_padrao', 'data_criacao', 'id_origem']

class TenantSerializer(serializers.ModelSerializer):
    lojas = LojaSerializer(many=True, default=None, allow_null=True, required=False)

    class Meta:
        model = Tenant
        fields = ['id', 'documento', 'razao_social', 'nome_fantasia', 'sistema_integrado', 'api_document', 'api_user', 'api_token', 'api_key',
                  'data_criacao', 'lojas', 'db_host', 'db_port', 'db_user', 'db_pass', 'db_name']

class TenantCreateSerializer(serializers.ModelSerializer):
    lojas = LojaSerializer(many=True)

    class Meta:
        model = Tenant
        fields = ['id', 'documento', 'razao_social', 'nome_fantasia', 'sistema_integrado', 'api_document', 'api_user', 'api_token', 'api_key',
                  'data_criacao', 'lojas', 'db_host', 'db_port', 'db_user', 'db_pass', 'db_name']

    def create(self, validated_data):
        lojas = validated_data.pop('lojas')
        with transaction.atomic():
            tenant = Tenant.objects.create(**validated_data)

            for loja in lojas:
                Loja.objects.create(tenant=tenant, **loja)

        return tenant

    def update(self, instance, validated_data):
        lojas = validated_data.pop('lojas', [])

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            for loja in lojas:
                loja_id = loja.get("id")

                if loja_id:
                    try:
                        loja_instance = Loja.objects.get(id=loja_id, tenant=instance)

                        loja_serializer = LojaSerializer(loja_instance, data=loja, partial=True)
                        loja_serializer.is_valid(raise_exception=True)
                        loja_serializer.save()

                    except Loja.DoesNotExist:
                        raise serializers.ValidationError(f"Loja com ID {loja_id} não encontrada.")
                else:
                    Loja.objects.create(tenant=instance, **loja)

        return instance