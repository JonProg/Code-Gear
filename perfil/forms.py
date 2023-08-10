from django import forms
from django.contrib.auth.models import User
from . import models

class PerfilForm(forms.ModelForm):
    class Meta:
        models = models.PerfilUsuario
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget= forms.PasswordInput(),
        label = 'Senha',
    )

    password2 = forms.CharField(
        required=True,
        widget= forms.PasswordInput(),
        label = 'Confirmação senha',
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'passwword', 'password2', 'email')
    
    def clean(self,*args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        usuario_db = User.objects.filter(username = usuario_data).first()
        email_db = User.objects.filter(email = email_data).first()

        error_msg_user_exists = 'Usúario já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As duas senhas não conferem.'
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres'

        if self.usuario:
            pass
        else:
            pass


