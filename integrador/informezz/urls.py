from django.urls import path
from integrador.informezz.estoque.views import EstoqueView
from integrador.informezz.loja.views import LojaView
from integrador.informezz.produto.views import ProdutoView
from integrador.informezz.venda.views import VendaView

urlpatterns = [
    path('estoque/', EstoqueView.as_view()),
    path('loja/', LojaView.as_view()),
    path('produto/', ProdutoView.as_view()),
    path('venda/', VendaView.as_view()),
]
