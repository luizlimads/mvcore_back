from django.urls import path
from integrador.ssotica.estoque.views import EstoqueView
from integrador.ssotica.financeiro.views import FinanceiroView
from integrador.ssotica.venda.views import VendaView

urlpatterns = [
    path('estoque/', EstoqueView.as_view()),
    path('financeiro/', FinanceiroView.as_view()),
    path('venda/', VendaView.as_view()),
]
