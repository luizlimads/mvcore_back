from django.urls import path
from .views import FuncionarioList, FuncionarioDetail

urlpatterns = [
    path('', FuncionarioList.as_view()),
    path('<uuid:pk>/', FuncionarioDetail.as_view()),
]
