# A18: assinaturas de apoio; traga sua implementação anterior.
from contextlib import closing
from pathlib import Path
import sqlite3
from pagamento import calcular_pagamento

LIMITE_CENTAVOS = 10000000

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
            con = sqlite3.connect(self.caminho)
            con.execute("PRAGMA foreign_keys = ON")
            return con
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
        except sqlite3.IntegrityError:
            raise ValueError("Não é possível excluir: o produto já está ligado a vendas.")
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
        except sqlite3.IntegrityError:
            raise ValueError("Não é possível excluir: o cliente já está ligado a vendas.")
        except sqlite3.Error:
            raise ValueError("Não foi possível excluir o cliente. Nada foi apagado.")
        if linhas_afetadas == 0:
            raise ValueError("Cliente não encontrado: o ID " + str(codigo) + " não existe.")

    def iniciar_vendas(self):
        try:
            with closing(self.conectar()) as con:
                with con:
                    con.execute("CREATE TABLE IF NOT EXISTS vendas ("
                                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                "cliente_id INTEGER NOT NULL REFERENCES clientes(id), "
                                "forma TEXT NOT NULL, "
                                "subtotal_centavos INTEGER NOT NULL, "
                                "desconto_centavos INTEGER NOT NULL, "
                                "total_centavos INTEGER NOT NULL)")
                    con.execute("CREATE TABLE IF NOT EXISTS itens_venda ("
                                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                "venda_id INTEGER NOT NULL REFERENCES vendas(id), "
                                "produto_id INTEGER NOT NULL REFERENCES produtos(id), "
                                "nome TEXT NOT NULL, "
                                "preco_centavos INTEGER NOT NULL, "
                                "quantidade INTEGER NOT NULL, "
                                "subtotal_centavos INTEGER NOT NULL, "
                                "UNIQUE (venda_id, produto_id))")
        except sqlite3.Error:
            raise ValueError("Não foi possível preparar as tabelas de vendas.")

    def registrar_venda(self, cliente_id, itens, forma):
        cliente_id = validar_id(cliente_id)
        if type(itens) != list or len(itens) == 0:
            raise ValueError("Adicione ao menos um item antes de gravar a venda.")
        subtotal = 0
        for produto_id, nome, preco, quantidade in itens:
            validar_id(produto_id)
            validar_nome(nome)
            validar_preco(preco)
            if type(quantidade) != int or quantidade < 1 or quantidade > 999:
                raise ValueError("Quantidade: use um número inteiro de 1 a 999.")
            subtotal += preco * quantidade
        subtotal_texto = f"{subtotal // 100}.{subtotal % 100:02d}"
        sub, desc, total = calcular_pagamento(subtotal_texto, forma)

        try:
            with closing(self.conectar()) as con:
                with con:
                    cliente = con.execute("SELECT id FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
                    if cliente is None:
                        raise ValueError("Cliente ID " + str(cliente_id) + " não foi encontrado.")
                    for produto_id, nome, preco, quantidade in itens:
                        atual = con.execute("SELECT nome, preco_centavos FROM produtos WHERE id = ?",
                                            (produto_id,)).fetchone()
                        if atual is None:
                            raise ValueError("O produto ID " + str(produto_id) + " não existe mais. "
                                            "Revise o item antes de confirmar.")
                        if atual[0] != nome or atual[1] != preco:
                            raise ValueError("O produto ID " + str(produto_id) + " mudou (nome ou preço). "
                                            "Atualize o catálogo e monte o item de novo.")
                    cursor = con.execute(
                        "INSERT INTO vendas (cliente_id, forma, subtotal_centavos, desconto_centavos, total_centavos) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (cliente_id, forma, int(sub * 100), int(desc * 100), int(total * 100)))
                    venda_id = cursor.lastrowid
                    for produto_id, nome, preco, quantidade in itens:
                        con.execute(
                            "INSERT INTO itens_venda (venda_id, produto_id, nome, preco_centavos, quantidade, subtotal_centavos) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            (venda_id, produto_id, nome, preco, quantidade, preco * quantidade))
        except sqlite3.Error:
            raise ValueError("Não foi possível gravar a venda. Nada foi salvo.")
        return validar_id(venda_id)

    def listar_vendas(self):
        try:
            with closing(self.conectar()) as con:
                vendas = con.execute(
                    "SELECT id, cliente_id, forma, subtotal_centavos, desconto_centavos, total_centavos "
                    "FROM vendas ORDER BY id").fetchall()
                resultado = []
                for venda in vendas:
                    itens = con.execute(
                        "SELECT produto_id, nome, preco_centavos, quantidade, subtotal_centavos "
                        "FROM itens_venda WHERE venda_id = ? ORDER BY id", (venda[0],)).fetchall()
                    resultado.append(venda + (itens,))
                return resultado
        except sqlite3.Error:
            raise ValueError("Não foi possível consultar as vendas.")