from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('', views.Pagar.as_view(), name='pagar'),
    path('lista/', views.Lista.as_view(), name='lista'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('detalhe/<int:id>', views.Detalhe.as_view(), name='detalhe'),
]
