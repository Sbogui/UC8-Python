# Complete os casos do registro; não marque sucesso sem verificá-los.
# TODO: criar dados fictícios, executar e comparar com assert.
# TODO: testar erro após válido, limites e uma correção com nova execução.
from modelos import Pizza, Bebida, Pedido, formatar
from pagamento import calcular_pagamento


def verificar():
    mussarela_m = Pizza("PZ01", "Mussarela", "Média", 3500)
    mussarela_g = Pizza("PZ02", "Mussarela", "Grande", 4500)
    refri = Bebida("BB01", "Refrigerante", 600)

    # T01 - pizza + duas bebidas
    pedido = Pedido()
    pedido.adicionar(mussarela_m, "1")
    pedido.adicionar(refri, "2")
    assert pedido.total_centavos() == 4700
    assert formatar(4700) == "R$ 47,00"

    # T02 - tamanho desconhecido
    try:
        Pizza("PZ09", "Calabresa", "Gigante", 4000)
        recusou = False
    except ValueError:
        recusou = True
    assert recusou

    # T03 - pizza e bebida juntas, com códigos diferentes
    pedido.adicionar(mussarela_g, "1")
    assert len(pedido.linhas()) == 3
    assert pedido.total_centavos() == 9200

    # T04 - atualizar e remover pelo código
    pedido.atualizar("BB01", "5")
    assert pedido.itens["BB01"].quantidade == 5
    pedido.remover("PZ01")
    assert len(pedido.linhas()) == 2
    assert pedido.total_centavos() == 7500

    # T05 - quantidade inválida não muda o pedido
    total_antes = pedido.total_centavos()
    try:
        pedido.atualizar("BB01", "0")
    except ValueError:
        pass
    try:
        pedido.adicionar(refri, "abc")
    except ValueError:
        pass
    assert pedido.total_centavos() == total_antes

    # T06 - pagamento do pedido de R$ 47,00
    sub, desc, total = calcular_pagamento("47.00", "PIX")
    assert str(total) == "40.89"
    sub, desc, total = calcular_pagamento("47.00", "Crédito 1x")
    assert str(total) == "47.00"

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
