from django.views.generic import ListView, DetailView
from django.shortcuts import resolve_url, redirect, get_object_or_404, render
from django.contrib import messages
from django.views import View
from perfil.models import PerfilUsuario
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
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            resolve_url('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)
        
        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        produto = variacao.produto
        variacao_estoque = variacao.estoque

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no'
                    f'produto "{produto_nome}". Adicionamos {variacao_estoque}x'
                    f'no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque
            
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho

            carrinho[variacao_id]['preco_quantitativo'] = quantidade_carrinho * \
                preco_unitario
            carrinho[variacao_id]['preco_quantitativo_promocinal'] = preco_unitario_promocional * \
                preco_unitario

        else:
            carrinho[variacao_id] = {
                'produto_id' : produto_id,
                'produto_nome' : produto_nome,
                'variacao_nome' : variacao_nome,
                'variacao_id' : variacao_id,
                'preco_unitario' : preco_unitario,
                'preco_unitario_promocional' : preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade' : 1,
                'slug' : slug,
                'imagem' : imagem,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu '
            f'carrinho {carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)
        

class RemoveCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            resolve_url('produto:lista')
        )

        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)
        
        if not self.request.session.get('carrinho'):
            return redirect(http_referer) 
        
        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        produto = self.request.session['carrinho'][variacao_id]

        messages.info(
            self.request,
            f'Produto {produto["produto_nome"]} {produto["variacao_nome"]} '
            f'removido do seu carrinho'
        )

        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)


class Carrinho(ListView):
    def get(self, *args,**kwargs):
        context = {
            'carrinho':self.request.session.get('carrinho', {})
            }
        return render(self.request, 'produto/carrinho.html', context)

class ResumoCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:create')
        
        perfil = PerfilUsuario.objects.filter(usuario = self.request.user).exists()

        if not perfil:
            messages.error(
                self.request,
                'Usuário sem perfil (-_-*)'
            )
            return redirect('perfil:create')
        
        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio (-_-*)'
            )
            return redirect('produto:lista')

        contexto = {
            'usuario': self.request.user,
            'endereco_user': self.request.user.perfilusuario.endereco_set.first(),
            'carrinho': self.request.session['carrinho'],
        }

        return render(self.request, 'produto/resumo_compra.html', contexto)
