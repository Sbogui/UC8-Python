# Complete os casos do registro; não marque sucesso sem verificá-los.
from contextlib import closing
import os
import sqlite3
import tempfile
from modelos import Pedido, Pizza, Bebida
from repositorio import RepositorioSqlite
from backup_sqlite import criar_backup


def erro_de(funcao, *args):
    try:
        funcao(*args)
    except ValueError as erro:
        return str(erro)
    return None


def ler_bytes(caminho):
    with open(caminho, "rb") as arquivo:
        return arquivo.read()


def verificar():
    try:
        assert False
        raise RuntimeError("Execute sem -O: os assert estão desativados.")
    except AssertionError:
        pass

    pasta_do_projeto = os.path.dirname(os.path.abspath(__file__))
    banco_principal = os.path.join(pasta_do_projeto, "sorveteria_a18.db")
    existia = os.path.exists(banco_principal)
    antes_principal = None
    if existia:
        antes_principal = ler_bytes(banco_principal)

    with tempfile.TemporaryDirectory() as pasta:
        origem = os.path.join(pasta, "origem-ficticia.db")
        repo = RepositorioSqlite(origem)
        repo.iniciar_vendas()
        repo.adicionar_cliente("Maria D'Ávila")
        repo.adicionar_produto("Sorvete", 650)
        repo.adicionar_produto("Picolé d'água", 500)
        repo.registrar_venda(1, [(1, "Sorvete", 650, 2)], "PIX")
        bytes_da_origem = ler_bytes(origem)

        # ---------- T01 (fluxo válido): cria a cópia e consulta registros conhecidos ----------
        copia = os.path.join(pasta, "copia-nova.db")
        criar_backup(origem, copia)
        assert os.path.exists(copia)
        copia_repo = RepositorioSqlite(copia)    # outra conexão, outro caminho
        assert copia_repo.listar_produtos() == [(1, "Sorvete", 650), (2, "Picolé d'água", 500)]
        assert copia_repo.listar_clientes() == [(1, "Maria D'Ávila")]
        assert copia_repo.listar_vendas() == [(1, 1, "PIX", 1300, 169, 1131, [(1, "Sorvete", 650, 2, 1300)])]
        with closing(sqlite3.connect(copia)) as con:
            assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"

        # ---------- T02 (origem preservada) ----------
        assert ler_bytes(origem) == bytes_da_origem
        assert len(repo.listar_produtos()) == 2

        # ---------- T03 (erro): origem ausente não cria banco vazio ----------
        ausente = os.path.join(pasta, "nao-existe.db")
        mensagem = erro_de(criar_backup, ausente, os.path.join(pasta, "outra-copia.db"))
        assert mensagem is not None and "Origem não encontrada" in mensagem
        assert not os.path.exists(ausente)
        assert not os.path.exists(os.path.join(pasta, "outra-copia.db"))

        # ---------- T04 (limite): destino existente não é sobrescrito ----------
        existente = os.path.join(pasta, "ja-existe.db")
        with open(existente, "wb") as arquivo:
            arquivo.write(b"conteudo que nao pode ser perdido")
        mensagem = erro_de(criar_backup, origem, existente)
        assert mensagem is not None and "não será sobrescrito" in mensagem
        assert ler_bytes(existente) == b"conteudo que nao pode ser perdido"
        mensagem = erro_de(criar_backup, origem, copia)
        assert mensagem is not None

        assert erro_de(criar_backup, origem, os.path.join(pasta, "sem-pasta", "x.db")) is not None

        # ---------- T05 (falha depois do válido): origem que não é banco SQLite ----------
        falso = os.path.join(pasta, "texto.db")
        with open(falso, "wb") as arquivo:
            arquivo.write(b"isto nao e um banco de dados sqlite, e so texto")
        destino_falso = os.path.join(pasta, "copia-do-falso.db")
        assert erro_de(criar_backup, falso, destino_falso) is not None
        assert not os.path.exists(destino_falso)
        assert ler_bytes(falso) == b"isto nao e um banco de dados sqlite, e so texto"
        assert ler_bytes(origem) == bytes_da_origem

        # ---------- T06: a cópia é um retrato do momento do backup ----------
        repo.adicionar_produto("Casquinha", 300)
        assert len(repo.listar_produtos()) == 3
        assert len(copia_repo.listar_produtos()) == 2

        # ---------- T07: restaurar fora do banco principal (cópia da cópia, em outro caminho) ----------
        restaurada = os.path.join(pasta, "restaurada.db")
        criar_backup(copia, restaurada)
        assert RepositorioSqlite(restaurada).listar_produtos() == [(1, "Sorvete", 650), (2, "Picolé d'água", 500)]
        assert RepositorioSqlite(restaurada).listar_vendas() == copia_repo.listar_vendas()

        # ---------- T08: um teste propositalmente errado falha; a previsão correta passa ----------
        quantidade_copiada = len(copia_repo.listar_produtos())
        try:
            assert quantidade_copiada == 3
            detectou = False
        except AssertionError:
            detectou = True
        assert detectou
        assert quantidade_copiada == 2

    if existia:
        assert ler_bytes(banco_principal) == antes_principal
    else:
        assert not os.path.exists(banco_principal)

    # Caso anterior (A10/A18): o pedido continua calculando
    pedido = Pedido()
    pedido.adicionar(Pizza("PZ01", "Mussarela Média", "Média", 3500), "1")
    pedido.adicionar(Bebida("BB01", "Refrigerante", 600), "2")
    assert pedido.total_centavos() == 4700

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
