# Complete os casos do registro; não marque sucesso sem verificá-los.
import csv
import os
import tempfile
from contextlib import closing
from modelos import Produto, Pedido, Pizza, Bebida, quantidade, formatar
from pagamento import calcular_pagamento
from relatorios import exportar_csv
from repositorio import RepositorioSqlite
from memoria import RepositorioMemoria
from controller import VendaController


def erro_de(funcao, *args):
    try:
        funcao(*args)
    except ValueError as erro:
        return str(erro)
    return None


def ler_bytes(caminho):
    with open(caminho, "rb") as arquivo:
        return arquivo.read()


def contar(repo, tabela):
    with closing(repo.conectar()) as con:
        return con.execute("SELECT COUNT(*) FROM " + tabela).fetchone()[0]


def verificar():
    try:
        assert False
        raise RuntimeError("Execute sem -O: os assert estão desativados.")
    except AssertionError:
        pass

    # Banco principal do projeto: esta suíte nunca deve criá-lo nem mexer nele.
    pasta_do_projeto = os.path.dirname(os.path.abspath(__file__))
    banco_principal = os.path.join(pasta_do_projeto, "sorveteria_a18.db")
    existia = os.path.exists(banco_principal)
    antes_principal = None
    if existia:
        antes_principal = ler_bytes(banco_principal)

    # ---------- T01 (regra): valores conhecidos, erro após válido e cancelamento repetidos ----------
    pizza = Pizza("PZ01", "Mussarela Média", "Média", 3500)
    refri = Bebida("BB01", "Refrigerante", 600)
    pedido = Pedido()
    pedido.adicionar(pizza, "1")
    pedido.adicionar(refri, "2")
    assert pedido.total_centavos() == 4700     
    assert formatar(4700) == "R$ 47,00"
    antes = pedido.linhas()
    for repeticao in range(2):                   
        assert erro_de(pedido.adicionar, refri, "abc") is not None 
        assert erro_de(pedido.finalizar, "PIX", False) is not None 
        assert pedido.linhas() == antes
        assert pedido.estado == "montagem"
    assert str(calcular_pagamento("47.00", "PIX")[2]) == "40.89"
    assert str(calcular_pagamento("47.00", "Débito")[2]) == "43.24"
    assert quantidade("1") == 1 and quantidade(" 999 ") == 999
    assert erro_de(quantidade, "1000") is not None

    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "ensaio.db")
        repo = RepositorioSqlite(caminho)
        repo.iniciar()          # produtos e clientes
        repo.iniciar_vendas()   # vendas e itens
        repo.adicionar_cliente("Maria D'Ávila")
        repo.adicionar_produto("Sorvete", 650)
        repo.adicionar_produto("Picolé d'água", 500)
        repo.adicionar_produto("Casquinha", 300)

        # ---------- T02 (persistência): ID estável depois de reorganizar a lista ----------
        invertida = list(reversed(repo.listar_produtos()))
        assert invertida[0][0] == 3              
        repo.editar_produto(invertida[0][0], "Casquinha crocante", 350)
        esperado = [(1, "Sorvete", 650), (2, "Picolé d'água", 500), (3, "Casquinha crocante", 350)]
        assert repo.listar_produtos() == esperado
        repo.adicionar_produto("x'); DROP TABLE produtos;--", 100)
        assert len(repo.listar_produtos()) == 4
        assert erro_de(repo.excluir_produto, 4) is not None      
        assert len(repo.listar_produtos()) == 4
        repo.excluir_produto(4, True)
        assert erro_de(repo.excluir_produto, 99, True) is not None
        assert repo.listar_produtos() == esperado

        # ---------- T03 (persistência): reabrir o mesmo caminho ----------
        assert RepositorioSqlite(caminho).listar_produtos() == esperado
        assert RepositorioSqlite(caminho).listar_clientes() == [(1, "Maria D'Ávila")]
        memoria = RepositorioMemoria()
        memoria.adicionar_produto("Sorvete", 650)
        assert memoria.listar_produtos() == [(1, "Sorvete", 650)]
        assert RepositorioMemoria().listar_produtos() == []

        # ---------- T04 (persistência): falha transacional sem venda parcial ----------
        itens_ruins = [(1, "Sorvete", 650, 1), (1, "Sorvete", 650, 1)] 
        mensagem = erro_de(repo.registrar_venda, 1, itens_ruins, "PIX")
        assert mensagem is not None and "Nada foi salvo" in mensagem
        assert contar(repo, "vendas") == 0 and contar(repo, "itens_venda") == 0
        itens_certos = [(1, "Sorvete", 650, 2)]
        assert repo.registrar_venda(1, itens_certos, "PIX") == 1
        assert repo.listar_vendas() == [(1, 1, "PIX", 1300, 169, 1131, [(1, "Sorvete", 650, 2, 1300)])]
        repo.editar_produto(2, "Picolé d'água", 550)
        mensagem = erro_de(repo.registrar_venda, 1, [(2, "Picolé d'água", 500, 1)], "PIX")
        assert mensagem is not None and "mudou" in mensagem
        assert contar(repo, "vendas") == 1 and contar(repo, "itens_venda") == 1
        repo.editar_produto(2, "Picolé d'água", 500)
        mensagem = erro_de(repo.excluir_cliente, 1, True)
        assert mensagem is not None and "ligado a vendas" in mensagem
        assert repo.listar_clientes() == [(1, "Maria D'Ávila")]

        # ---------- T05 (CSV): exportação coerente com o comprovante ----------
        venda_pedido = Pedido()
        venda_pedido.adicionar(Produto("1", "Sorvete", 650), "2")
        venda_id, comprovante = VendaController(repo).confirmar(venda_pedido, 1, "PIX", venda_pedido.versao)
        assert venda_id == 2
        assert comprovante["total_centavos"] == 1131
        arquivo_csv = os.path.join(pasta, "venda.csv")
        exportar_csv(arquivo_csv, comprovante)
        with open(arquivo_csv, "r", encoding="utf-8-sig", newline="") as arquivo:
            linhas = list(csv.DictReader(arquivo, delimiter=";"))
        assert len(linhas) == 1
        assert linhas[0]["id"] == "1" and linhas[0]["quantidade"] == "2"
        assert linhas[0]["subtotal_centavos"] == "1300" and linhas[0]["total_pedido_reais"] == "11,31"
        venda_pedido.novo()
        venda_pedido.adicionar(Produto("3", "Casquinha crocante", 350), "9")
        exportar_csv(arquivo_csv, venda_pedido.ver_comprovante())
        with open(arquivo_csv, "r", encoding="utf-8-sig", newline="") as arquivo:
            assert list(csv.DictReader(arquivo, delimiter=";")) == linhas

        # ---------- T06: um teste propositalmente errado falha; a previsão restaurada passa ----------
        total = pedido.total_centavos()
        try:
            assert total == 4000                 
            detectou = False
        except AssertionError:
            detectou = True
        assert detectou
        assert total == 4700                     

    if existia:
        assert ler_bytes(banco_principal) == antes_principal
    else:
        assert not os.path.exists(banco_principal)

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
