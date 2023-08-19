from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao


class Pagar(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login (--_--*)'
            )
            return redirect('perfil:create')

        if not self.request.session['carrinho']:
            messages.error(
                self.request,
                'O carrinho está vazio (+_+*)'
            )
            return redirect('produto:lista')

        carrinho = self.request.session.get('carrinho')
        carrinho_variacoes_ids = [v for v in carrinho]
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id__in = carrinho_variacoes_ids)
        )

        for variacao in bd_variacoes:
            vid = variacao.id
            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']

        contexto = {

        }

        return render(self.request, self.template_name, contexto)

class SalvarPedido(View):
    pass

class Detalhe(DetailView):
    pass
