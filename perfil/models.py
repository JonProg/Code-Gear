import re
from django.db import models
from utils.states import estados
from django.contrib.auth.models import User
from utils.validador_cpf import valida_cpf
from django.forms import ValidationError


class PerfilUsuario(models.Model):
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.usuario}'
    
    def clean(self):
        error_perfil = {}

        cpf_enviado = self.cpf or None
        cpf_salvo = None
        perfil = PerfilUsuario.objects.filter(cpf = cpf_enviado)

        if perfil:
            cpf_salvo = perfil.cpf

            if cpf_salvo is not None and self.pk != perfil.pk:
                error_perfil['cpf'] = 'CPF já existe.'

        if not valida_cpf(self.cpf):
            error_perfil['cpf'] = 'Digite um CPF válido'
        
        if error_perfil:
            raise ValidationError(error_perfil)

        return super().clean()


class Endereco(models.Model):
    perfil_usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        choices = estados
    )

    def __str__(self):
        return f'Endereço {self.numero}'
    
    def clean(self):
        error_endereco = {}

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_endereco['cep'] = 'CEP inválido, digite os 8 digitos do CEP'

        if error_endereco:
            raise ValidationError(error_endereco)

        return super().clean()

