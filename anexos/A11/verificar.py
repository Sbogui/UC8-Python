# Complete os casos do registro; não marque sucesso sem verificá-los.
# TODO: criar dados fictícios, executar e comparar com assert.
# TODO: testar erro após válido, limites e uma correção com nova execução.

from modelos import Pizza, Bebida, Pedido


def verificar():
    pizza = Pizza("PZ01", "Mussarela Média", "Média", 3500)
    refri = Bebida("BB01", "Refrigerante", 600)
    suco = Bebida("BB02", "Suco", 700)

    # T01 - pedido vazio não finaliza
    pedido = Pedido()
    try:
        pedido.finalizar("PIX", True)
        recusou = False
    except ValueError:
        recusou = True
    assert recusou
    assert pedido.estado == "montagem"

    # T02 - sem forma de pagamento não finaliza
    pedido.adicionar(pizza, "1")
    pedido.adicionar(refri, "2")
    try:
        pedido.finalizar("", True)
        recusou = False
    except ValueError:
        recusou = True
    assert recusou
    assert pedido.estado == "montagem"
    assert pedido.total_centavos() == 4700

    # T03 - cancelar não chama finalizar: confirmado=False também não finaliza
    try:
        pedido.finalizar("PIX", False)
        recusou = False
    except ValueError:
        recusou = True
    assert recusou
    assert pedido.estado == "montagem"
    assert len(pedido.linhas()) == 2

    # T04 - prévia antiga é rejeitada
    versao_previa = pedido.versao
    pedido.adicionar(suco, "1")
    try:
        pedido.finalizar("PIX", True, versao_previa)
        recusou = False
    except ValueError:
        recusou = True
    assert recusou
    assert pedido.estado == "montagem"
    pedido.remover("BB02")

    # T05 - confirmar gera o comprovante
    comprovante = pedido.finalizar("PIX", True, pedido.versao)
    assert pedido.estado == "finalizado"
    assert comprovante["subtotal_centavos"] == 4700
    assert comprovante["desconto_centavos"] == 611
    assert comprovante["total_centavos"] == 4089
    assert comprovante["subtotal_centavos"] == comprovante["desconto_centavos"] + comprovante["total_centavos"]

    # T06 - finalizado bloqueia mudanças e segunda finalização
    for numero in range(4):
        try:
            if numero == 0:
                pedido.adicionar(suco, "1")
            elif numero == 1:
                pedido.atualizar("PZ01", "2")
            elif numero == 2:
                pedido.remover("PZ01")
            else:
                pedido.finalizar("PIX", True)
            bloqueou = False
        except ValueError:
            bloqueou = True
        assert bloqueou, numero
    assert pedido.total_centavos() == 4700

    # T07 - mexer no recibo devolvido não muda o comprovante guardado
    comprovante["itens"].append("lixo")
    comprovante["total_centavos"] = 0
    assert len(pedido.comprovante["itens"]) == 2
    assert pedido.comprovante["total_centavos"] == 4089

    # T08 - novo pedido começa vazio e o comprovante antigo continua guardado
    pedido.novo()
    assert pedido.estado == "montagem"
    assert pedido.linhas() == []
    assert pedido.comprovante["total_centavos"] == 4089

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
