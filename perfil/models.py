from django.db import models
from utils.states import estados
from django.contrib.auth.models import User

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

    def __str__(self) -> str:
        return f'{self.usuario.first_name} {self.usuario.last_name}'

    def clean(self):
        pass

class Endereco(models.Model):
    perfil_usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
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
        return f'Endereço {self.nome}'

