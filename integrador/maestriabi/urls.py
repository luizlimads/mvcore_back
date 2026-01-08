from django.urls import path
from .views import ProdutosBIView, EstoquesBIView, VendasBIView

urlpatterns = [
    path("produtos/", ProdutosBIView.as_view()),
    path("estoques/", EstoquesBIView.as_view()),
    path("vendas/", VendasBIView.as_view()),
]
