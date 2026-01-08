from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from tenant.models import Tenant
from django.utils import timezone
from .managers import UsuarioManager

class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'tenant']

    objects = UsuarioManager()

    class Meta:
        db_table = "usuario_usuarios"

    def __str__(self):
        return self.nome
