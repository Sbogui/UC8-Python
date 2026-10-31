from modelos import Produto, Item, Pedido, quantidade, formatar


def tentar_adicionar(pedido, produto, texto):
    try:
        pedido.adicionar(produto, texto)
    except ValueError as erro:
        return str(erro)
    return None


def verificar():
    fruta = Produto("P01", "Fruta", 500)
    leite = Produto("P02", "Leite", 750)
    outra_fruta = Produto("P03", "Fruta", 600)  

    pedido = Pedido()
    pedido.adicionar(fruta, "2")
    pedido.adicionar(leite, "3")
    assert [linha[3] for linha in pedido.linhas()] == [1000, 2250]
    assert pedido.total_centavos() == 3250
    assert formatar(pedido.total_centavos()) == "R$ 32,50"

    outro = Pedido()
    assert outro.linhas() == [] and outro.total_centavos() == 0
    assert outro.itens is not pedido.itens

    pedido.adicionar(fruta, "3")
    assert len(pedido.linhas()) == 2 and pedido.linhas()[0][2] == 5
    pedido.adicionar(outra_fruta, "1")
    assert len(pedido.linhas()) == 3
    assert pedido.total_centavos() == 5 * 500 + 3 * 750 + 600

    antes = (pedido.linhas(), pedido.total_centavos())
    assert tentar_adicionar(pedido, None, "1") == "Selecione um produto antes de adicionar."
    assert antes == (pedido.linhas(), pedido.total_centavos())

    for ruim in ["", "   ", "abc", "0", "-1", "1,5", "1.5", "1000", "+2", "2 3"]:
        assert tentar_adicionar(pedido, fruta, ruim) is not None, ruim
        assert antes == (pedido.linhas(), pedido.total_centavos()), ruim
    # Limites 1 e 999 são válidos.
    assert quantidade("1") == 1 and quantidade(" 999 ") == 999

    grande = Pedido()
    grande.adicionar(leite, "999")
    assert tentar_adicionar(grande, leite, "1") is not None
    assert grande.linhas() == [("P02", "Leite", 999, 999 * 750)]

    novo = Pedido()
    esperados = []
    for produto, texto, parcial in [(fruta, "1", 500), (leite, "2", 2000), (fruta, "2", 3000)]:
        novo.adicionar(produto, texto)
        esperados.append(parcial)
        assert novo.total_centavos() == parcial
    assert esperados == [500, 2000, 3000]

    item = Item(leite, "4")
    assert item.produto is leite and item.quantidade == 4 and item.subtotal() == 3000
    try:
        Item(leite, "0")
        criou = True
    except ValueError:
        criou = False
    assert criou is False

    try:
        assert pedido.total_centavos() == 1
        falhou = False
    except AssertionError:
        falhou = True
    assert falhou

    assert formatar(5) == "R$ 0,05" and formatar(123456) == "R$ 1.234,56"
    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
