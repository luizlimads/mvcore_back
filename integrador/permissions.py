from rest_framework.permissions import BasePermission

class TenantPertenceAoSistemaPermission(BasePermission):

    def has_permission(self, request, view):
        tenant = request.user.tenant
        sistema_integrado = getattr(view, 'sistema_integrado', None)

        if not sistema_integrado:
            return False

        return tenant.sistema_integrado.nome.lower() == sistema_integrado.lower()
