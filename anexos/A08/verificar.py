# Complete os casos do registro; não marque sucesso sem verificá-los.
from decimal import Decimal
from modelos import Produto, Pedido, formatar
from pagamento import valor_monetario, calcular_pagamento, preco_para_centavos


def erro_de(funcao, *args):
    try:
        funcao(*args)
    except ValueError as erro:
        return str(erro)
    return None


def verificar():
    D = Decimal
    for forma, total in [("Dinheiro", "87.00"), ("PIX", "87.00"), ("Débito", "92.00"), ("Crédito 1x", "100.00")]:
        sub, desc, tot = calcular_pagamento("100,00", forma)
        assert sub == D("100.00") and tot == D(total), forma
        assert desc == D("100.00") - D(total), forma

    assert calcular_pagamento("0,50", "PIX") == (D("0.50"), D("0.06"), D("0.44"))

    pedido = Pedido()
    pedido.adicionar(Produto("P01", "Fruta", 500), "2")
    pedido.adicionar(Produto("P02", "Leite", 750), "3")
    antes = (pedido.linhas(), pedido.total_centavos())
    texto = f"{pedido.total_centavos() // 100}.{pedido.total_centavos() % 100:02d}"
    assert texto == "32.50"
    primeira = calcular_pagamento(texto, "PIX")
    segunda = calcular_pagamento(texto, "PIX")
    assert primeira == segunda == (D("32.50"), D("4.22"), D("28.28")) 
    assert antes == (pedido.linhas(), pedido.total_centavos())

    totais = [calcular_pagamento(texto, f)[2] for f in ("PIX", "Crédito 1x", "PIX")]
    assert totais == [D("28.28"), D("32.50"), D("28.28")]

    assert erro_de(calcular_pagamento, "10,00", "") == "Escolha a forma de pagamento."
    assert erro_de(calcular_pagamento, "10,00", "   ") == "Escolha a forma de pagamento."
    assert erro_de(calcular_pagamento, "10,00", "Cheque") == "Forma de pagamento desconhecida."

    for ruim in ["abc", "nan", "inf", "-1", "+1", "1.000,00", "1,000", "1.234", "10,555", "", "  ", "1e3", "1 0", "٣"]:
        assert erro_de(valor_monetario, ruim) is not None, ruim
    assert erro_de(valor_monetario, "1000000,01") is not None
    assert valor_monetario("1000000,00") == D("1000000.00") and valor_monetario("0") == D("0.00")
    assert valor_monetario("7,5") == valor_monetario("7.50") == D("7.50")
    assert erro_de(valor_monetario, "0", False) == "Valor: informe um valor maior que zero."

    for sub_texto in ["0,01", "0,50", "1,15", "2,35", "99,99", "12345,67"]:
        for forma in ("Dinheiro", "PIX", "Débito", "Crédito 1x"):
            sub, desc, tot = calcular_pagamento(sub_texto, forma)
            assert sub == desc + tot, (sub_texto, forma)
            assert tot.as_tuple().exponent == -2 and desc >= 0

    fruta = Produto("P01", "Fruta", 500)
    novo = Pedido()
    novo.adicionar(fruta, "999")
    assert erro_de(novo.adicionar, fruta, "1") is not None
    assert erro_de(novo.adicionar, None, "1") == "Selecione um produto antes de adicionar."
    assert erro_de(novo.adicionar, fruta, "1,5") is not None
    assert novo.linhas() == [("P01", "Fruta", 999, 999 * 500)]
    assert formatar(3250) == "R$ 32,50" and preco_para_centavos("7,50") == 750
    assert erro_de(preco_para_centavos, "0") is not None

    try:
        assert calcular_pagamento("100,00", "PIX")[2] == D("88.00")
        falhou = False
    except AssertionError:
        falhou = True
    assert falhou
    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
