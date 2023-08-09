from django import template
from utils import functions

register = template.Library()

@register.filter
def formata_preco(val):
    return functions.format_price(val)

@register.filter
def qtd_total(carrinho):
    return functions.cart_total_qtd(carrinho)

@register.filter
def cart_total(carrinho):
    return functions.cart_total(carrinho)


