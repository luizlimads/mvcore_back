from django.contrib.auth.models import BaseUserManager
from tenant.models import Tenant

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password, tenant, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório.")

        if not tenant:
            raise ValueError("O tenant é obrigatório.")
        else:
            try:
                tenant = Tenant.objects.get(id=tenant)
            except Tenant.DoesNotExist:
                raise ValueError("O tenant fornecido não é válido.")

        email = self.normalize_email(email)
        user = self.model(email=email, tenant=tenant, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, tenant, **extra_fields):
        user = self.create_user(email, password, tenant, **extra_fields)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
