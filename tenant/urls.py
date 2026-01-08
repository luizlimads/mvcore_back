from django.urls import path
from .views import TenantList, TenantDetail, SistemaIntegradoList, SistemaIntegradoDetail, LojaList, LojaDetail

urlpatterns = [
    path('', TenantList.as_view()),
    path('<uuid:pk>/', TenantDetail.as_view()),
    path('sistema-integrado/', SistemaIntegradoList.as_view()),
    path('sistema-integrado/<uuid:pk>/', SistemaIntegradoDetail.as_view()),
    path('loja/', LojaList.as_view()),
    path('loja/<uuid:pk>/', LojaDetail.as_view()),
]
