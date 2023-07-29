from django.contrib import admin
from perfil.models import Endereco, PerfilUsuario
    
class EnderecoInline(admin.StackedInline):
    model = Endereco
    extra = 1

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = 'usuario','data_nascimento',
    inlines = [
        EnderecoInline
    ]

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = 'perfil_usuario','cep',

