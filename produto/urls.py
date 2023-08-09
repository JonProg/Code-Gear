from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name="lista"),
    path('produto/<slug:slug>/', views.DetalheProduto.as_view(), name="detalhe"),
    path('add_carrinho/', views.AddCarrinho.as_view(), name="addcarrinho"),
    path('removerdocarrinho/', views.RemoveCarrinho.as_view(), name="removerdocarrinho"),
    path('carrinho/', views.Carrinho.as_view(), name="carrinho"),
    path('resumocompra/', views.ResumoCompra.as_view(), name="resumocompra"),
    
]
