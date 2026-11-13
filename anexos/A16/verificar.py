# Complete os casos do registro; não marque sucesso sem verificá-los.
import os
import sys
import tempfile
from modelos import Pizza, Bebida, Pedido
from repositorio import RepositorioSqlite
from memoria import RepositorioMemoria
from controller import CadastroController


class RepositorioQueFalha:

    def adicionar_produto(self, nome, preco):
        raise ValueError("Falha simulada no armazenamento.")

    def editar_produto(self, codigo, nome, preco):
        raise ValueError("Falha simulada no armazenamento.")

    def adicionar_cliente(self, nome):
        raise ValueError("Falha simulada no armazenamento.")

    def editar_cliente(self, codigo, nome):
        raise ValueError("Falha simulada no armazenamento.")

    def listar_produtos(self):
        return []


def rodar_cenario(repositorio):
    controle = CadastroController(repositorio)
    resultado = []
    resultado.append(controle.salvar("produto", "Sorvete", "12,00"))
    resultado.append(controle.salvar("produto", "Picolé", "5,00"))
    resultado.append(controle.salvar("produto", "Sorvete de creme", "15,00", 1))
    resultado.append(controle.listar("produto"))
    resultado.append(controle.salvar("cliente", "Maria D'Ávila"))
    resultado.append(controle.salvar("cliente", "João"))
    resultado.append(controle.salvar("cliente", "João Pedro", "", 2))
    try:
        controle.excluir("cliente", 1, False)
        resultado.append("excluiu sem confirmar")
    except ValueError as erro:
        resultado.append(str(erro))
    resultado.append(controle.listar("cliente"))
    resultado.append(controle.excluir("cliente", 1, True))
    resultado.append(controle.listar("cliente"))
    controle.excluir("produto", 1, True)
    controle.excluir("produto", 2, True)
    resultado.append(controle.listar("produto"))
    resultado.append(controle.salvar("produto", "Novo", "1,00"))
    return resultado


def verificar():
    # T01 - o controller roda sem Tkinter
    assert "tkinter" not in sys.modules

    esperado = [
        1, 2, 1,
        [(1, "Sorvete de creme", 1500), (2, "Picolé", 500)],
        1, 2, 2,
        "Confirme a exclusão para apagar o cliente.",
        [(1, "Maria D'Ávila"), (2, "João Pedro")],
        1,
        [(2, "João Pedro")],
        [],
        3,
    ]

    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "teste.db")
        sqlite = RepositorioSqlite(caminho)
        sqlite.iniciar()
        memoria = RepositorioMemoria()

        # T02 e T04 e T05 - o mesmo cenário (incluir, listar, editar por ID, excluir cliente,
        # cancelar exclusão) dá o mesmo resultado nas duas implementações
        resultado_memoria = rodar_cenario(memoria)
        resultado_sqlite = rodar_cenario(sqlite)
        assert resultado_memoria == esperado
        assert resultado_sqlite == esperado
        assert resultado_memoria == resultado_sqlite

        # T03 - memória começa vazia numa instância nova; SQLite reabre com os dados
        assert RepositorioMemoria().listar_produtos() == []
        assert RepositorioMemoria().listar_clientes() == []
        novo_sqlite = RepositorioSqlite(caminho)
        assert novo_sqlite.listar_produtos() == [(3, "Novo", 100)]
        assert novo_sqlite.listar_clientes() == [(2, "João Pedro")]

        # T06 - tipo de cadastro desconhecido é rejeitado
        controle = CadastroController(memoria)
        for tipo in ["fornecedor", "", "produto; DROP TABLE produtos", None]:
            try:
                controle.listar(tipo)
                recusou = False
            except ValueError:
                recusou = True
            assert recusou, tipo
            try:
                controle.salvar(tipo, "X", "1,00")
                recusou = False
            except ValueError:
                recusou = True
            assert recusou, tipo
            try:
                controle.excluir(tipo, 1, True)
                recusou = False
            except ValueError:
                recusou = True
            assert recusou, tipo

        # T07 - a falha do repositório chega ao chamador (não vira lista vazia nem sucesso)
        falho = CadastroController(RepositorioQueFalha())
        try:
            falho.salvar("produto", "Teste", "7,50")
            comunicou = False
        except ValueError as erro:
            comunicou = "Falha simulada" in str(erro)
        assert comunicou
        try:
            falho.salvar("cliente", "Teste", "", 5)
            comunicou = False
        except ValueError as erro:
            comunicou = "Falha simulada" in str(erro)
        assert comunicou
        sem_tabelas = CadastroController(RepositorioSqlite(os.path.join(pasta, "vazio.db")))
        try:
            sem_tabelas.salvar("produto", "Teste", "7,50")
            comunicou = False
        except ValueError:
            comunicou = True
        assert comunicou
        for preco_ruim in ["", "abc", "0", "-1"]:
            try:
                controle.salvar("produto", "Teste", preco_ruim)
                recusou = False
            except ValueError:
                recusou = True
            assert recusou, preco_ruim

        # T08 - a cópia devolvida pela memória não altera o armazenamento por fora
        repo = RepositorioMemoria()
        repo.adicionar_produto("Sorvete", 1200)
        copia = repo.listar_produtos()
        copia.append((99, "Intruso", 1))
        copia.clear()
        assert repo.listar_produtos() == [(1, "Sorvete", 1200)]
        repo.adicionar_cliente("Maria")
        copia_clientes = repo.listar_clientes()
        copia_clientes.append((99, "Intruso"))
        assert repo.listar_clientes() == [(1, "Maria")]

    # T09 (componentes independentes) é da janela: não dá para verificar aqui.

    # Caso anterior (A10/A15): pedido em memória continua funcionando
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
