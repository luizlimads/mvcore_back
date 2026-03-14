from django.urls import path
from integrador.sti3powerstock.estoque.views import EstoqueView
from integrador.sti3powerstock.fornecedor.views import FornecedorView
from integrador.sti3powerstock.loja.views import LojaView
from integrador.sti3powerstock.produto.views import ProdutoView
from integrador.sti3powerstock.venda.views import VendaView

urlpatterns = [
    path('estoque/', EstoqueView.as_view()),
    path('fornecedor/', FornecedorView.as_view()),
    path('loja/', LojaView.as_view()),
    path('produto/', ProdutoView.as_view()),
    path('venda/', VendaView.as_view()),
]
