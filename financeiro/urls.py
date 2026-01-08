from django.urls import path
from .views import InstituicaoFinanceiraList, InstituicaoFinanceiraDetail, ContaFinanceiraList, ContaFinanceiraDetail, CategoriaFinanceiraList, CategoriaFinanceiraDetail, LancamentoList, LancamentoDetail, ContaFinanceiraResumo, LancamentoResumoDiarioPeriodo

urlpatterns = [
    path('instituicao-financeira/', InstituicaoFinanceiraList.as_view()),
    path('instituicao-financeira/<uuid:pk>/', InstituicaoFinanceiraDetail.as_view()),
    
    path('conta-financeira/', ContaFinanceiraList.as_view()),
    path('conta-financeira/resumo/', ContaFinanceiraResumo.as_view()),
    path('conta-financeira/<uuid:pk>/', ContaFinanceiraDetail.as_view()),
    
    path('categoria-financeira/', CategoriaFinanceiraList.as_view()),
    path('categoria-financeira/<uuid:pk>/', CategoriaFinanceiraDetail.as_view()),
        
    path('lancamento/', LancamentoList.as_view()),
    path('lancamento/resumo/', LancamentoResumoDiarioPeriodo.as_view()),
    path('lancamento/<uuid:pk>/', LancamentoDetail.as_view()),
    
]
