from django.contrib import admin
from perfil import models


class EnderecoInline(admin.TabularInline):
    model = models.Endereco
    extra = 1

@admin.register(models.PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = 'usuario', 
    inlines = [
        EnderecoInline
    ]

