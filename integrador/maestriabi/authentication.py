from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from tenant.models import Tenant

class PowerBIAuthentication(BaseAuthentication):

    def authenticate(self, request):
        api_key = request.headers.get("X-POWERBI-KEY")

        if not api_key:
            return None

        try:
            tenant = Tenant.objects.get(
                bi_api_key=api_key,
                bi_api_key_active=True
            )
        except Tenant.DoesNotExist:
            raise AuthenticationFailed("API Key inválida")

        request.tenant = tenant
        return (None, None)