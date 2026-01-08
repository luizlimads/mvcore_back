from django.contrib import admin
from .models import FormaPagamento, Venda, ItemVenda

admin.site.register(FormaPagamento)
admin.site.register(Venda)
admin.site.register(ItemVenda)
