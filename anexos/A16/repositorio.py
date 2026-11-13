# A15: assinaturas de apoio; traga sua implementação anterior.
from contextlib import closing
from pathlib import Path
import sqlite3

LIMITE_CENTAVOS = 10000000  # R$ 100.000,00

def validar_nome(nome):
    if type(nome) != str or nome.strip() == "":
        raise ValueError("Nome: informe um nome.")
    return nome.strip()

def validar_id(codigo):
    if type(codigo) != int or codigo <= 0:
        raise ValueError("ID: deve ser um número inteiro positivo.")
    return codigo

def validar_preco(preco):
    if type(preco) != int or preco <= 0:
        raise ValueError("Preço: informe um valor maior que zero, em centavos inteiros.")
    if preco > LIMITE_CENTAVOS:
        raise ValueError("Preço: o máximo é R$ 100.000,00.")
    return preco

class RepositorioSqlite:

    def __init__(self, caminho):
        self.caminho = Path(caminho)

    def conectar(self):
        try:
            return sqlite3.connect(self.caminho)
        except sqlite3.Error:
            raise ValueError("Não foi possível abrir o banco de dados.")

    def iniciar(self):
        try:
            with closing(self.conectar()) as con:
                with con:
                    con.execute("CREATE TABLE IF NOT EXISTS produtos ("
                                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                "nome TEXT NOT NULL, "
                                "preco_centavos INTEGER NOT NULL)")
                    con.execute("CREATE TABLE IF NOT EXISTS clientes ("
                                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                "nome TEXT NOT NULL)")
        except sqlite3.Error:
            raise ValueError("Não foi possível preparar o banco de dados.")

    def adicionar_produto(self, nome, preco):
        nome = validar_nome(nome)
        preco = validar_preco(preco)
        try:
            with closing(self.conectar()) as con:
                with con: 
                    cursor = con.execute(
                        "INSERT INTO produtos (nome, preco_centavos) VALUES (?, ?)",
                        (nome, preco))
                    novo_id = cursor.lastrowid
        except sqlite3.Error:
            raise ValueError("Não foi possível gravar o produto. Nada foi salvo.")
        return validar_id(novo_id)

    def listar_produtos(self):
        try:
            with closing(self.conectar()) as con:
                return con.execute(
                    "SELECT id, nome, preco_centavos FROM produtos ORDER BY id").fetchall()
        except sqlite3.Error:
            raise ValueError("Não foi possível consultar os produtos.")

    def adicionar_cliente(self, nome):
        nome = validar_nome(nome)
        try:
            with closing(self.conectar()) as con:
                with con:
                    cursor = con.execute("INSERT INTO clientes (nome) VALUES (?)", (nome,))
                    novo_id = cursor.lastrowid
        except sqlite3.Error:
            raise ValueError("Não foi possível gravar o cliente. Nada foi salvo.")
        return validar_id(novo_id)

    def listar_clientes(self):
        try:
            with closing(self.conectar()) as con:
                return con.execute("SELECT id, nome FROM clientes ORDER BY id").fetchall()
        except sqlite3.Error:
            raise ValueError("Não foi possível consultar os clientes.")

    def editar_produto(self, codigo, nome, preco):
        codigo = validar_id(codigo)
        nome = validar_nome(nome)
        preco = validar_preco(preco)
        try:
            with closing(self.conectar()) as con:
                with con:
                    cursor = con.execute(
                        "UPDATE produtos SET nome = ?, preco_centavos = ? WHERE id = ?",
                        (nome, preco, codigo))
                    linhas_afetadas = cursor.rowcount
        except sqlite3.Error:
            raise ValueError("Não foi possível editar o produto. Nada foi alterado.")
        if linhas_afetadas == 0:
            raise ValueError("Produto não encontrado: o ID " + str(codigo) + " não existe.")

    def excluir_produto(self, codigo, confirmado=False):
        codigo = validar_id(codigo)
        if not confirmado:
            raise ValueError("Confirme a exclusão para apagar o produto.")
        try:
            with closing(self.conectar()) as con:
                with con:
                    cursor = con.execute("DELETE FROM produtos WHERE id = ?", (codigo,))
                    linhas_afetadas = cursor.rowcount
        except sqlite3.Error:
            raise ValueError("Não foi possível excluir o produto. Nada foi apagado.")
        if linhas_afetadas == 0:
            raise ValueError("Produto não encontrado: o ID " + str(codigo) + " não existe.")

    def editar_cliente(self, codigo, nome):
        codigo = validar_id(codigo)
        nome = validar_nome(nome)
        try:
            with closing(self.conectar()) as con:
                with con:
                    cursor = con.execute(
                        "UPDATE clientes SET nome = ? WHERE id = ?", (nome, codigo))
                    linhas_afetadas = cursor.rowcount
        except sqlite3.Error:
            raise ValueError("Não foi possível editar o cliente. Nada foi alterado.")
        if linhas_afetadas == 0:
            raise ValueError("Cliente não encontrado: o ID " + str(codigo) + " não existe.")

    def excluir_cliente(self, codigo, confirmado=False):
        codigo = validar_id(codigo)
        if not confirmado:
            raise ValueError("Confirme a exclusão para apagar o cliente.")
        try:
            with closing(self.conectar()) as con:
                with con:
                    cursor = con.execute("DELETE FROM clientes WHERE id = ?", (codigo,))
                    linhas_afetadas = cursor.rowcount
        except sqlite3.Error:
            raise ValueError("Não foi possível excluir o cliente. Nada foi apagado.")
        if linhas_afetadas == 0:
            raise ValueError("Cliente não encontrado: o ID " + str(codigo) + " não existe.")