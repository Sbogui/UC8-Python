# A10: assinaturas de apoio; traga sua implementação anterior.
from modelos import Pizza, Pedido, formatar


def demonstrar():
    try:
        import PySimpleGUI as sg
    except ImportError:
        print("PySimpleGUI não está instalado: comparação não executada.")
        return

    pizza = Pizza("PZ01", "Mussarela Média", "Média", 3500)
    pedido = Pedido()

    layout = [
        [sg.Text("Mussarela Média — quantidade:"), sg.Input(key="qtd")],
        [sg.Button("Adicionar"), sg.Button("Fechar")],
        [sg.Text("", key="aviso")],
    ]
    janela = sg.Window("A10 — comparação", layout)

    while True:
        evento, valores = janela.read()
        if evento == "Fechar" or evento == sg.WIN_CLOSED:
            break
        if evento == "Adicionar":
            try:
                pedido.adicionar(pizza, valores["qtd"])
                janela["aviso"].update("Total: " + formatar(pedido.total_centavos()))
            except ValueError as erro:
                janela["aviso"].update(str(erro))

    janela.close()


if __name__ == "__main__":
    demonstrar()