from django import template
from utils.functions import format_price

register = template.Library()

@register.filter
def formata_preco(val):
    return format_price(val)
