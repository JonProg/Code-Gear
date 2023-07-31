from django.views.generic import ListView, DetailView
from django.views import View
from . import models

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista_produtos.html'
    context_object_name = 'produtos'
    paginate_by = 10

class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AddCarrinho(View):
    pass

class RemoveCarrinho(View):
    pass

class Carrinho(ListView):
    pass

class Finalizar(View):
    pass
