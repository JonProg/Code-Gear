from django.contrib import admin
from perfil import models

@admin.register(models.Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = 'get_first_name','cep',

    def get_first_name(self, obj):
        return obj.perfil_usuario.usuario.first_name

class EnderecoInline(admin.StackedInline):
    model = models.Endereco
    extra = 1

@admin.register(models.PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = 'usuario',
    inlines = [
        EnderecoInline
    ]

