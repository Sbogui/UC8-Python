# Complete os casos do registro; não marque sucesso sem verificá-los.
from contextlib import closing
import os
import sqlite3
import tempfile
from modelos import Produto, Pedido, Pizza, Bebida
from pagamento import preco_para_centavos
from relatorios import exportar_csv
from repositorio import RepositorioSqlite
from controller import CadastroController, VendaController
import csv


def contar(repo, tabela):
    # conta as linhas de uma tabela (nomes fixos, escritos aqui no teste)
    with closing(repo.conectar()) as con:
        return con.execute("SELECT COUNT(*) FROM " + tabela).fetchone()[0]


def montar_pedido(repo):
    # monta um pedido a partir do que está no banco agora (como o "Atualizar catálogo")
    pedido = Pedido()
    for codigo, nome, preco in repo.listar_produtos():
        if codigo == 1:
            pedido.adicionar(Produto(str(codigo), nome, preco), "2")
    return pedido


def verificar():
    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "teste.db")
        repo = RepositorioSqlite(caminho)
        repo.iniciar_vendas()
        cadastros = CadastroController(repo)
        vendas = VendaController(repo)

        cliente = cadastros.salvar("cliente", "Maria D'Ávila")
        produto_1 = cadastros.salvar("produto", "Sorvete", "6,50")
        produto_2 = cadastros.salvar("produto", "Picolé", "5,00")
        assert (cliente, produto_1, produto_2) == (1, 1, 2)

        # T01 - catálogo e clientes vêm do banco por ID, também depois de reabrir
        novo_repo = RepositorioSqlite(caminho)
        assert novo_repo.listar_produtos() == [(1, "Sorvete", 650), (2, "Picolé", 500)]
        assert novo_repo.listar_clientes() == [(1, "Maria D'Ávila")]

        # T02 - cadastro novo só aparece depois de consultar de novo
        catalogo_na_tela = repo.listar_produtos()
        cadastros.salvar("produto", "Novo", "1,00")  # cadastrado depois da consulta
        assert len(catalogo_na_tela) == 2            # a lista da tela não mudou sozinha
        assert len(repo.listar_produtos()) == 3      # ao atualizar (consultar), ele aparece
        cadastros.excluir("produto", 3, True)        # volta ao catálogo anterior (ainda sem vendas)

        # T04 - cliente não selecionado ou inexistente: orienta e não grava
        pedido = montar_pedido(repo)
        versao = pedido.versao
        try:
            vendas.confirmar(pedido, None, "PIX", versao)
            recusou = False
        except ValueError as erro:
            recusou = "Selecione um cliente" in str(erro)
        assert recusou
        try:
            vendas.confirmar(pedido, 99, "PIX", versao)
            recusou = False
        except ValueError as erro:
            recusou = "Cliente ID 99" in str(erro)
        assert recusou
        assert contar(repo, "vendas") == 0
        assert pedido.estado == "montagem" and len(pedido.itens) == 1

        # T03 - preço mudou ou produto sumiu: recusa sem venda parcial, montagem preservada
        antes = pedido.linhas()
        repo.editar_produto(1, "Sorvete", 700)  
        try:
            vendas.confirmar(pedido, cliente, "PIX", versao)
            recusou = False
        except ValueError as erro:
            recusou = "mudou" in str(erro)
        assert recusou
        assert contar(repo, "vendas") == 0 and contar(repo, "itens_venda") == 0
        assert pedido.estado == "montagem" and pedido.linhas() == antes
        repo.editar_produto(1, "Sorvete", 650)  
        repo.editar_produto(1, "Sorvete artesanal", 650)  
        try:
            vendas.confirmar(pedido, cliente, "PIX", versao)
            recusou = False
        except ValueError as erro:
            recusou = "mudou" in str(erro)
        assert recusou
        repo.editar_produto(1, "Sorvete", 650)
        outro = Pedido()  
        outro.adicionar(Produto("2", "Picolé", 500), "1")
        repo.excluir_produto(2, True)
        try:
            vendas.confirmar(outro, cliente, "PIX", outro.versao)
            recusou = False
        except ValueError as erro:
            recusou = "não existe mais" in str(erro)
        assert recusou
        assert contar(repo, "vendas") == 0

        # T06 - falha na segunda inserção desfaz venda e itens (o mesmo produto duas vezes)
        itens_ruins = [(1, "Sorvete", 650, 1), (1, "Sorvete", 650, 1)]
        try:
            repo.registrar_venda(cliente, itens_ruins, "PIX")
            recusou = False
        except ValueError as erro:
            recusou = "Nada foi salvo" in str(erro)
        assert recusou
        assert contar(repo, "vendas") == 0   
        assert contar(repo, "itens_venda") == 0

        # vínculos conferidos pelo próprio banco (foreign_keys ligado em cada conexão)
        with closing(repo.conectar()) as con:
            try:
                with con:
                    con.execute("INSERT INTO vendas (cliente_id, forma, subtotal_centavos, "
                                "desconto_centavos, total_centavos) VALUES (999, 'PIX', 1, 0, 1)")
                aceitou = True
            except sqlite3.IntegrityError:
                aceitou = False
        assert not aceitou

        # T05 e T07 - venda de 2 unidades a 6,50 no PIX: 13,00 -> 11,31. Sucesso grava uma venda
        assert preco_para_centavos("6,50") == 650
        venda_id, comprovante = vendas.confirmar(pedido, cliente, "PIX", versao)
        assert venda_id == 1
        assert comprovante["subtotal_centavos"] == 1300
        assert comprovante["desconto_centavos"] == 169
        assert comprovante["total_centavos"] == 1131
        assert pedido.estado == "finalizado"
        assert repo.listar_vendas() == [(1, 1, "PIX", 1300, 169, 1131, [(1, "Sorvete", 650, 2, 1300)])]
        try:
            vendas.confirmar(pedido, cliente, "PIX", versao)  
            recusou = False
        except ValueError:
            recusou = True
        assert recusou
        assert contar(repo, "vendas") == 1 and contar(repo, "itens_venda") == 1

        # T08 - excluir cadastro vinculado é bloqueado, e as vendas continuam
        for chamada in range(2):
            try:
                if chamada == 0:
                    repo.excluir_cliente(1, True)
                else:
                    repo.excluir_produto(1, True)
                recusou = False
            except ValueError as erro:
                recusou = "ligado a vendas" in str(erro)
            assert recusou
        assert repo.listar_clientes() == [(1, "Maria D'Ávila")]
        assert len(repo.listar_vendas()) == 1

        # T09 - o CSV usa o comprovante confirmado e mantém os totais
        pedido.novo()
        pedido.adicionar(Produto("1", "Sorvete", 650), "5") 
        arquivo_csv = os.path.join(pasta, "venda.csv")
        exportar_csv(arquivo_csv, pedido.ver_comprovante())
        with open(arquivo_csv, "r", encoding="utf-8-sig", newline="") as arquivo:
            linhas = list(csv.DictReader(arquivo, delimiter=";"))
        assert len(linhas) == 1
        assert linhas[0]["id"] == "1" and linhas[0]["quantidade"] == "2"
        assert linhas[0]["subtotal_centavos"] == "1300"
        assert linhas[0]["total_pedido_reais"] == "11,31"
        assert linhas[0]["total_pedido_reais"] == f"{1131 // 100},{1131 % 100:02d}"  

        # reabrir o banco conserva a venda
        assert RepositorioSqlite(caminho).listar_vendas() == repo.listar_vendas()

    # T10 (comparação ttk/CTk) é da janela e opcional: não dá para verificar aqui.

    # Caso anterior (A10/A16): pedido em memória e total
    teste = Pedido()
    teste.adicionar(Pizza("PZ01", "Mussarela Média", "Média", 3500), "1")
    teste.adicionar(Bebida("BB01", "Refrigerante", 600), "2")
    assert teste.total_centavos() == 4700

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
