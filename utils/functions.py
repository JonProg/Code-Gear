def format_price(valor):
    return f'R$ {valor:.2f}'.replace('.',',')

def cart_total_qtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])