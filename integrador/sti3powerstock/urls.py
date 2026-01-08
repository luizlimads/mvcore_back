from django.urls import path
from integrador.sti3powerstock.loja.views import LojaView
from integrador.sti3powerstock.estoque.views import EstoqueView
from integrador.sti3powerstock.venda.views import VendaView

urlpatterns = [
    path('loja/', LojaView.as_view()),
    path('estoque/', EstoqueView.as_view()),
    path('venda/', VendaView.as_view()),
]
