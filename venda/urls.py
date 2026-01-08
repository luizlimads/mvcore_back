from django.urls import path
from .views import VendaList, VendaDetail

urlpatterns = [
    path('', VendaList.as_view()),
    path('<uuid:pk>/', VendaDetail.as_view())
]
