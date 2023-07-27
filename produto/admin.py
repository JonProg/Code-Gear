from django.contrib import admin
from produto.models import Produto, Variacao

@admin.register(Variacao)
class VaricaoAdmin(admin.ModelAdmin):
    list_display = 'nome', 'preco', 'estoque',
    ordering = '-id',
    list_filter = 'preco',

class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']
    list_display = 'id','nome', 'is_published',
    list_display_links = 'nome',
    list_per_page = 10
    ordering = '-id',
    list_filter = 'preco_marketing', 'is_published',
    list_editable = 'is_published',
    prepopulated_fields = {
        "slug": ('nome',),
    }
    inlines = [
        VariacaoInline
    ]



