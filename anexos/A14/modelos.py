# A14: assinaturas de apoio; traga sua implementação anterior.
from pagamento import calcular_pagamento

TAMANHOS = ("Média", "Grande")


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
        if not codigo.strip():
            raise ValueError("Produto: informe o código.")
        if not nome.strip():
            raise ValueError("Produto: informe o nome.")
        if preco_centavos <= 0:
            raise ValueError("Produto: o preço deve ser maior que zero.")
        self.codigo = codigo
        self.nome = nome
        self.preco_centavos = preco_centavos


class Pizza:

    def __init__(self, codigo, nome, tamanho, preco_centavos):
        if tamanho not in TAMANHOS:
            raise ValueError("Pizza: o tamanho deve ser Média ou Grande.")
        self.produto = Produto(codigo, nome, preco_centavos)
        self.tamanho = tamanho
        self.codigo = self.produto.codigo
        self.nome = self.produto.nome
        self.preco_centavos = self.produto.preco_centavos


class Bebida:

    def __init__(self, codigo, nome, preco_centavos):
        self.produto = Produto(codigo, nome, preco_centavos)
        self.codigo = self.produto.codigo
        self.nome = self.produto.nome
        self.preco_centavos = self.produto.preco_centavos


class Item:

    def __init__(self, produto, texto_quantidade):
        self.quantidade = quantidade(texto_quantidade)
        self.produto = produto

    def subtotal(self):
        return self.quantidade * self.produto.preco_centavos


class Pedido:

    def __init__(self):
        self.itens = {}
        self.estado = "montagem"   
        self.versao = 1            
        self.comprovante = None    

    def exigir_aberto(self):
        if self.estado != "montagem":
            raise ValueError("Pedido finalizado: inicie um novo pedido.")

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
        self.versao += 1

    def total_centavos(self):
        return sum(item.subtotal() for item in self.itens.values())

    def linhas(self):
        return [
            (i.produto.codigo, i.produto.nome, i.quantidade, i.subtotal())
            for i in self.itens.values()
        ]

    def atualizar(self, codigo, texto_quantidade):
        self.exigir_aberto()
        if codigo not in self.itens:
            raise ValueError("Item não encontrado no pedido.")
        self.itens[codigo].quantidade = quantidade(texto_quantidade)
        self.versao += 1

    def remover(self, codigo):
        self.exigir_aberto()
        if codigo not in self.itens:
            raise ValueError("Item não encontrado no pedido.")
        del self.itens[codigo]
        self.versao += 1

    def finalizar(self, forma, confirmado, versao_previa=None):
        self.exigir_aberto()
        if len(self.itens) == 0:
            raise ValueError("Adicione ao menos um item antes de finalizar.")
        if versao_previa is not None and versao_previa != self.versao:
            raise ValueError("A prévia ficou antiga: abra a confirmação de novo.")
        if not confirmado:
            raise ValueError("Confirme o pedido para finalizar.")
        centavos = self.total_centavos()
        subtotal_texto = f"{centavos // 100}.{centavos % 100:02d}"
        sub, desc, total = calcular_pagamento(subtotal_texto, forma)  
        self.comprovante = {
            "itens": self.linhas(),  
            "forma": forma,
            "subtotal_centavos": int(sub * 100),
            "desconto_centavos": int(desc * 100),
            "total_centavos": int(total * 100),
        }
        self.estado = "finalizado"
        return self.ver_comprovante()

    def ver_comprovante(self):
        c = self.comprovante
        return {
            "itens": list(c["itens"]),
            "forma": c["forma"],
            "subtotal_centavos": c["subtotal_centavos"],
            "desconto_centavos": c["desconto_centavos"],
            "total_centavos": c["total_centavos"],
        }

    def novo(self):
        self.itens = {}
        self.estado = "montagem"
        self.versao += 1