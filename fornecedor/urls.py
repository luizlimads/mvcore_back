from django.urls import path
from .views import FornecedorList, FornecedorDetail

urlpatterns = [
    path('', FornecedorList.as_view()),
    path('<uuid:pk>/', FornecedorDetail.as_view()),
]
