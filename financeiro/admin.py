from django.contrib import admin
from .models import InstituicaoFinanceira, ContaFinanceira, CategoriaFinanceira

admin.site.register(InstituicaoFinanceira)
admin.site.register(ContaFinanceira)
admin.site.register(CategoriaFinanceira)
