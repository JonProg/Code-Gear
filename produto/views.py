from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from . import models

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista_produtos.html'
    context_object_name = 'produtos'

    def get_context_data(self,**kwargs):

        return super().get_context_data(**kwargs)

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
