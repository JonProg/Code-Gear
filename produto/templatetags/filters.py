from django import template
from utils.functions import format_price, cart_total_qtd

register = template.Library()

@register.filter
def formata_preco(val):
    return format_price(val)

@register.filter
def qtd_total(carrinho):
    return cart_total_qtd(carrinho)
