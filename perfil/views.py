from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy
from . import models
from . import forms


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self,*args, **kwargs):
        super().setup(*args, **kwargs)

        self.perfil = None
        self.endereco = None
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho',{}))

        if self.request.user.is_authenticated:
            self.perfil = models.PerfilUsuario.objects.filter(
                usuario = self.request.user
            ).first()

            self.endereco = models.Endereco.objects.filter(
                perfil_usuario = self.perfil
            ).first()

            self.contexto = {
                'userform': forms.UserForm(
                    data = self.request.POST or None,
                    usuario = self.request.user,
                    instance = self.request.user,
                ),

                'perfilform': forms.PerfilForm(
                    data = self.request.POST or None,
                    instance = self.perfil,
                ),

                'enderecoform':forms.EnderecoForm(
                    data = self.request.POST or None,
                    instance = self.endereco,
                ),
            }

        else:
            self.contexto = {
                'userform': forms.UserForm(
                    data = self.request.POST or None
                ),

                'perfilform': forms.PerfilForm(
                    data = self.request.POST or None
                ),

                'enderecoform':forms.EnderecoForm(
                    data = self.request.POST or None
                ),
            }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']
        self.enderecoform = self.contexto['enderecoform']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'
        
        self.renderizar = render(
            self.request, self.template_name, self.contexto
            )
        
    def get(self, *args, **kwargs):
        return self.renderizar

class Create(BasePerfil):
    def post(self, *args, **kwargs):
        if not all([self.userform.is_valid(), self.perfilform.is_valid(), self.enderecoform.is_valid()]):
            messages.error(
            self.request,
            'Existem erros no formulário de cadastro. Verifique se todos os campos foram prenchidos corretamente.'
            )
            return self.renderizar
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                User, username = self.request.user.username
            )

            usuario.username = username

            if password:
                usuario.set_password(password)
            
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            if not self.perfil:
                self.perfilform.cleaned_data['usuario'] = usuario
                perfil = models.PerfilUsuario(**self.perfilform.cleaned_data)
                perfil.save()

            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

            if not self.endereco:
                self.enderecoform.cleaned_data['perfil_usuario'] = perfil
                endereco = models.Endereco(**self.enderecoform.cleaned_data)
                endereco.save()
            
            else:
                endereco = self.enderecoform.save(commit=False)
                endereco.perfil_usuario = self.perfil
                endereco.save()


        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

            endereco = self.enderecoform.save(commit=False)
            endereco.perfil_usuario = perfil
            endereco.save()
            
        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password,
            )

            if autentica:
                login(self.request, user=usuario)
        
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        
        messages.success(
            self.request,
            'Seu cadastro foi criado com sucesso \(0_0*)/'
        )

        return redirect('produto:carrinho')

class Login(View):
    def post(self,*args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        usuario = authenticate(
                self.request,
                username=username,
                password=password,
            )

        if not username or not password or not usuario:
            messages.error(
            self.request,
            'Usuário ou senha inválidos.'
            )
            return redirect('perfil:create')
        
        login(self.request, user=usuario)

        messages.success(
            self.request,
            'Você fez login e pode concluir sua compra.'
        )

        return redirect('produto:carrinho')
        
class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho',{}))
        logout(self.request)
        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        return redirect('produto:lista')


class Enderecos(ListView):
    def get(self, *args,**kwargs):
        perfil = models.PerfilUsuario.objects.get(usuario__username=self.request.user)
        context = {
            'enderecos': models.Endereco.objects.filter(perfil_usuario = perfil)
            }
        return render(self.request, 'perfil/lista_enderecos.html', context)


class EnderecoUpdate(DetailView):
    template_name = 'perfil/endereco_update.html'

    def setup(self,*args, **kwargs):
        super().setup(*args, **kwargs)

        self.pk = kwargs['pk']
        self.endereco = models.Endereco.objects.filter(
            pk = self.pk
        ).first()

        self.contexto = {
            'enderecoform':forms.EnderecoForm(
                data = self.request.POST or None,
                instance = self.endereco,
            ),
            'mode':'Atualizar',
        }

        self.enderecoform = self.contexto['enderecoform']

        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )
    
    def post(self, *args, **kwargs):

        if not self.enderecoform.is_valid():
            messages.error(
            self.request,
            'Existem erros no formulário de endereço. Verifique se todos os campos foram prenchidos corretamente.'
            )
            return self.renderizar

        self.endereco = self.enderecoform.save(commit=False)
        self.endereco.save()

        messages.success(
            self.request,
            f'{self.endereco} atualizado com sucesso !'
        )
        return redirect('perfil:adress')


    def get(self,*args, **kwargs):
        return self.renderizar


class EnderecoCreate(View):
    template_name = 'perfil/endereco_update.html'

    def setup(self,*args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'enderecoform':forms.EnderecoForm(
                data = self.request.POST or None,
            ),
            'mode':'Criar',

        }

        self.enderecoform = self.contexto['enderecoform']

        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )


    def post(self, *args, **kwargs):

        if not self.enderecoform.is_valid():
            messages.error(
            self.request,
            'Existem erros no formulário de cadastro. Verifique se todos os campos foram prenchidos corretamente.'
            )
            return self.renderizar

        self.perfil = models.PerfilUsuario.objects.filter(
            usuario = self.request.user
        ).first()

        endereco = self.enderecoform.save(commit=False)
        endereco.perfil_usuario = self.perfil
        endereco.save()

        messages.success(
            self.request,
            f'{endereco} criado com sucesso !'
        )
        return redirect('perfil:adress')
    

    def get(self,*args, **kwargs):
        return self.renderizar

class EnderecoDelete(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            resolve_url('perfil:adress')
        )

        adress_id = self.request.GET.get('vid')

        self.endereco = models.Endereco.objects.filter(
            pk = adress_id
        ).first()

        if models.Endereco.objects.first() == self.endereco:
            messages.error(
                self.request,
                f'O {self.endereco} não pode ser excluido'
            )

        if not adress_id:
            return redirect(http_referer)
        
        self.endereco.delete()

        messages.info(
            self.request,
            f'{self.endereco} excluido dos seus endereços'
        )

        return redirect(http_referer)


