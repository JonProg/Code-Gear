from django.shortcuts import render
from django.views import View
from . import forms

class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self,*args, **kwargs):
        super().setup(*args, **kwargs)

        if self.request.user.is_authenticated:
            self.contexto = {
                'userform': forms.UserForm(
                    data = self.request.POST or None,
                    usuario = self.request.user,
                    instance = self.request.user,
                ),
                'perfilform': forms.PerfilForm(
                    data = self.request.POST or None,
                ),
            }

        else:
            self.contexto = {
                'userform': forms.UserForm(
                    data = self.request.POST or None,
                ),
                'perfilform': forms.PerfilForm(
                    data = self.request.POST or None
                )
            }
        
        self.renderizar = render(
            self.request, self.template_name, self.contexto
            )
        
    def get(self, *args, **kwargs):
        return self.renderizar

class Create(BasePerfil):
    def post(self, *args, **kwargs):
        return self.renderizar

class Update(View):
    pass

class Delete(View):
    pass

class Login(View):
    pass

class Logout(View):
    pass


