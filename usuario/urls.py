from django.urls import path
from .views import *

urlpatterns = [
    path('', UsuarioList.as_view()),
    path('<uuid:pk>/', UsuarioDetail.as_view()),
]


