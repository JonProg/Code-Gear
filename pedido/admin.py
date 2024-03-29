from django.contrib import admin
from pedido.models import Pedido, ItemPedido

class ItemPedidoInline(admin.StackedInline):
    model = ItemPedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [ItemPedidoInline]
