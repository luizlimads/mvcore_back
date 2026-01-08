from django.urls import path
from .views import ProdutoList, ProdutoDetail, EstoqueList, EstoqueDetail

urlpatterns = [
    path('', ProdutoList.as_view()),
    path('<uuid:pk>/', ProdutoDetail.as_view()),
    path('estoque/', EstoqueList.as_view()),
    path('estoque/<uuid:pk>/', EstoqueDetail.as_view()),
]
