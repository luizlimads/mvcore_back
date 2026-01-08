from tenant.models import Tenant
from rest_framework import serializers

class TenantSerializerMixin:
    def get_tenant_instance(self):
        tenant = self.context.get("tenant")
        if not isinstance(tenant, Tenant):
            tenant = Tenant.objects.get(id=tenant)
        return tenant

    def create(self, validated_data):
        validated_data["tenant"] = self.get_tenant_instance()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["tenant"] = self.get_tenant_instance()
        return super().update(instance, validated_data)
