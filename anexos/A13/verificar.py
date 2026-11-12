# Complete os casos do registro; não marque sucesso sem verificá-los.

# TODO: criar dados fictícios, executar e comparar com assert.
# TODO: testar erro após válido, limites e uma correção com nova execução.

import csv
import os
import tempfile
from modelos import Pizza, Bebida, Pedido
from relatorios import exportar_csv, CABECALHO
from perfis import SessaoDemo


def ler_linhas(caminho):
    with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo, delimiter=";"))


def ler_bytes(caminho):
    with open(caminho, "rb") as arquivo:
        return arquivo.read()


def verificar():
    nome_dificil = 'Picolé; edição "verão"'
    picole = Bebida("BB09", nome_dificil, 500)
    pizza = Pizza("PZ01", "Mussarela Média", "Média", 3500)

    # Pedido fictício confirmado: 2 picolés (1000) + 1 pizza (3500) = 4500, PIX = 3915
    pedido = Pedido()
    pedido.adicionar(picole, "2")
    pedido.adicionar(pizza, "1")
    comprovante = pedido.finalizar("PIX", True, pedido.versao)

    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "vendas.csv")

        # T01 - sem comprovante não exporta
        try:
            exportar_csv(caminho, None)
            recusou = False
        except ValueError:
            recusou = True
        assert recusou
        assert not os.path.exists(caminho)

        # T02 - CSV conserva acento, ponto e vírgula e aspas
        exportar_csv(caminho, comprovante)
        assert ler_bytes(caminho).startswith(b"\xef\xbb\xbf")  # UTF-8 com BOM
        linhas = ler_linhas(caminho)
        assert len(linhas) == 2
        assert linhas[0]["nome"] == nome_dificil
        assert linhas[1]["nome"] == "Mussarela Média"

        # T03 - colunas, quantidade, centavos e total seguem o cabeçalho
        with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
            leitor = csv.reader(arquivo, delimiter=";")
            assert next(leitor) == CABECALHO
        assert linhas[0]["id"] == "BB09"
        assert linhas[0]["quantidade"] == "2"
        assert linhas[0]["preco_centavos"] == "500"
        assert linhas[0]["subtotal_centavos"] == "1000"
        assert linhas[1]["subtotal_centavos"] == "3500"
        assert linhas[0]["forma"] == "PIX"
        assert linhas[0]["total_pedido_reais"] == "39,15"
        assert linhas[1]["total_pedido_reais"] == "39,15"

        # T04 - o relatório vem do comprovante confirmado, não de outra montagem
        pedido.novo()
        pedido.adicionar(Bebida("BB02", "Suco", 700), "3")
        caminho2 = os.path.join(pasta, "vendas2.csv")
        exportar_csv(caminho2, comprovante)
        assert ler_linhas(caminho2) == linhas
        assert pedido.total_centavos() == 2100  # a nova montagem continua separada

        # T06 - falha não substitui o relatório anterior
        antes = ler_bytes(caminho)
        vazio = {"itens": [], "forma": "PIX", "total_centavos": 0}
        try:
            exportar_csv(caminho, vazio)
            recusou = False
        except ValueError:
            recusou = True
        assert recusou
        assert ler_bytes(caminho) == antes

        try:
            exportar_csv(os.path.join(pasta, "naoexiste", "x.csv"), comprovante)
            recusou = False
        except ValueError:
            recusou = True
        assert recusou  # pasta inexistente: erro avisado

        destino = os.path.join(pasta, "destino.csv")
        os.mkdir(destino)  # uma pasta com o nome do relatório faz a troca falhar
        try:
            exportar_csv(destino, comprovante)
            recusou = False
        except ValueError:
            recusou = True
        assert recusou
        assert os.path.isdir(destino)
        for nome in os.listdir(pasta):
            assert not nome.endswith(".tmp"), nome  # nenhum temporário sobrou
        assert ler_bytes(caminho) == antes

    # T07 - perfis: Caixa não configura, Administração configura
    sessao = SessaoDemo()
    assert sessao.pode_configurar() is False  # sem sessão
    sessao.entrar("Ana Fictícia", "Caixa")
    assert sessao.pode_configurar() is False
    sessao.entrar("Beto Fictício", "Administração")
    assert sessao.pode_configurar() is True
    try:
        sessao.entrar("", "Caixa")
        recusou = False
    except ValueError:
        recusou = True
    assert recusou
    try:
        sessao.entrar("Carla", "Gerente")
        recusou = False
    except ValueError:
        recusou = True
    assert recusou
    assert sessao.nome == "Beto Fictício"  # a recusa não trocou a sessão

    # T08 - sair limpa a sessão, mas não apaga vendas
    sessao.sair()
    assert sessao.nome is None and sessao.perfil is None
    assert sessao.pode_configurar() is False
    assert pedido.comprovante["total_centavos"] == 3915  # o comprovante continua guardado

    # T09 - núcleo da pizzaria preservado: código, totais e confirmação
    teste = Pedido()
    teste.adicionar(pizza, "1")
    teste.adicionar(Bebida("BB01", "Refrigerante", 600), "2")
    assert teste.total_centavos() == 4700
    recibo = teste.finalizar("PIX", True, teste.versao)
    assert recibo["total_centavos"] == 4089
    assert teste.estado == "finalizado"
    
    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
