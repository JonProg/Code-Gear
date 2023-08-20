from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao
from utils import functions
from .models import Pedido, ItemPedido


class Pagar(View):
    pass


class SalvarPedido(View):
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
            vid = str(variacao.id)
            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']
            error_msg = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unt_promo

                error_msg = 'Estoque insuficiente para alguns produtos do seu carrinho (ಥ﹏ಥ). '\
                    'Reduzimos a quantidade desses produtos. Por favor, verifique '\
                    'quais produtos foram afetados a seguir.'

            if error_msg:
                messages.error(
                    self.request,
                    error_msg
                )
                self.request.session.save()
                return redirect('produto:carrinho')
            
            qtd_total_carrinho = functions.cart_total_qtd(carrinho)
            valor_total_carrinho = functions.cart_total(carrinho)

            pedido = Pedido(
                usuario = self.request.user,
                total = valor_total_carrinho,
                qtd_total = qtd_total_carrinho,
                status = 'C',
            )

            pedido.save()

            ItemPedido.objects.bulk_create(
                [
                    ItemPedido(
                        pedido = pedido,
                        produto = v['produto_nome'],
                        produto_id = v['produto_id'],
                        variacao = v['variacao_nome'],
                        variacao_id = v['variacao_id'],
                        preco = v['preco_quantitativo'],
                        preco_promocional = v['preco_quantitativo_promocional'],
                        quantidade = v['quantidade'],
                        imagem = v['imagem'],

                    ) for v in carrinho.values()
                ]
            )

        del self.request.session.get['carrinho']
        #return render(self.request, self.template_name)
        #redendizar pagina de pagamento via pix ou boleto
        return redirect('pedido:pagar')

class Lista(View):
    pass

class Detalhe(DetailView):
    pass
