from django.contrib import admin
from .models import Tenant, SistemaIntegrado

admin.site.register(SistemaIntegrado)
admin.site.register(Tenant)