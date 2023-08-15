from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import copy
from . import models
from . import forms


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self,*args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho',{}))

        self.contexto = {
            'userform': forms.UserForm(
                data = self.request.POST or None,
            ),
            'perfilform': forms.PerfilForm(
                data = self.request.POST or None,
            ),
            'enderecoform':forms.EnderecoForm(
                data = self.request.POST or None
            ),
        }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']
        self.enderecoform = self.contexto['enderecoform']
        
        self.renderizar = render(
            self.request, self.template_name, self.contexto
            )
        
    def get(self, *args, **kwargs):
        return self.renderizar

class Create(BasePerfil):
    def post(self, *args, **kwargs):
        if not all([self.userform.is_valid(), self.perfilform.is_valid(), self.enderecoform.is_valid()]):
            return self.renderizar
        
        password = self.userform.cleaned_data.get('password')

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
        return self.renderizar

class Update(BasePerfil):
    pass

class Delete(View):
    pass

class Login(View):
    pass

class Logout(View):
    pass


