# A08: assinaturas de apoio; traga sua implementação anterior.
def quantidade(texto):
    limpo = texto.strip()
    if not (limpo.isascii() and limpo.isdigit()):
        raise ValueError("Quantidade: informe um número inteiro de 1 a 999.")
    valor = int(limpo)
    if valor < 1 or valor > 999:
        raise ValueError("Quantidade: use um valor de 1 a 999.")
    return valor


def formatar(centavos):
    reais, resto = divmod(centavos, 100)
    milhares = f"{reais:,}".replace(",", ".")
    return f"R$ {milhares},{resto:02d}"


class Produto:

    def __init__(self, codigo, nome, preco_centavos):
        self.codigo = codigo
        self.nome = nome
        self.preco_centavos = preco_centavos


class Item:

    def __init__(self, produto, texto_quantidade):
        self.quantidade = quantidade(texto_quantidade)  
        self.produto = produto

    def subtotal(self):
        return self.quantidade * self.produto.preco_centavos


class Pedido:

    def __init__(self):
        self.itens = {}
        self.aberto = True

    def exigir_aberto(self):
        if not self.aberto:
            raise ValueError("Pedido fechado: inicie um novo pedido.")

    def adicionar(self, produto, texto_quantidade):
        self.exigir_aberto()
        if produto is None:
            raise ValueError("Selecione um produto antes de adicionar.")
        if produto.codigo in self.itens:
            existente = self.itens[produto.codigo]
            nova = quantidade(texto_quantidade)
            if existente.quantidade + nova > 999:
                raise ValueError("Quantidade acumulada: o máximo por produto é 999.")
            existente.quantidade += nova  
        else:
            self.itens[produto.codigo] = Item(produto, texto_quantidade)

    def total_centavos(self):
        return sum(item.subtotal() for item in self.itens.values())

    def linhas(self):
        return [
            (i.produto.codigo, i.produto.nome, i.quantidade, i.subtotal())
            for i in self.itens.values()
        ]