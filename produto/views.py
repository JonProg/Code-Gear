from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View

class ListaProdutos(ListView):
    pass

class DetalheProduto(DetailView):
    pass

class AddCarrinho(View):
    pass

class RemoveCarrinho(View):
    pass

class Carrinho(ListView):
    pass

class Finalizar(View):
    pass
