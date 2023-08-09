from django import forms
from django.contrib.auth.models import User
from . import models

class PerfilForm(forms.ModelForm):
    class Meta:
        models = models.PerfilUsuario
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'passwword', 'email')
    
    def clean(*args, **kwargs):
        pass