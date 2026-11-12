# Complete os casos do registro; não marque sucesso sem verificá-los.
def verificar():
# TODO: criar dados fictícios, executar e comparar com assert.
# TODO: testar erro após válido, limites e uma correção com nova execução.
import os
import tempfile
from modelos import Pizza, Bebida, Pedido
from pagamento import preco_para_centavos
from repositorio import RepositorioSqlite, validar_id


def verificar():
    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "teste.db")
        repo = RepositorioSqlite(caminho)

        # T08 (parte 1) - criar o objeto não cria o arquivo do banco
        assert not os.path.exists(caminho)

        # T01 - a tabela é criada sem apagar linhas existentes
        repo.iniciar()
        assert os.path.exists(caminho)
        assert repo.listar_produtos() == []
        repo.adicionar_produto("Sorvete", 1200)
        repo.iniciar()  # roda de novo
        assert len(repo.listar_produtos()) == 1

        # T02 - preço 7,50 vira 750, número inteiro
        assert preco_para_centavos("7,50") == 750
        repo.adicionar_produto("Picolé", preco_para_centavos("7,50"))
        linhas = repo.listar_produtos()
        assert linhas[1][2] == 750
        assert type(linhas[1][2]) == int

        # T03 - nome com apóstrofo e texto de SQL são só texto
        repo.adicionar_produto("Picolé d'água", 500)
        repo.adicionar_produto("x'); DROP TABLE produtos;--", 100)
        linhas = repo.listar_produtos()
        assert linhas[2][1] == "Picolé d'água"
        assert linhas[3][1] == "x'); DROP TABLE produtos;--"
        assert len(linhas) == 4  

        # T04 - nome vazio ou preço inválido não inserem registro
        antes = repo.listar_produtos()
        ruins = [("", 500), ("   ", 500), ("Teste", 0), ("Teste", -1), ("Teste", "750"), ("Teste", 10000001), ("Teste", True)]
        for nome, preco in ruins:
            try:
                repo.adicionar_produto(nome, preco)
                recusou = False
            except ValueError:
                recusou = True
            assert recusou, (nome, preco)
        assert repo.listar_produtos() == antes

        # T05 - IDs positivos e únicos, vindos do banco (não da posição)
        ids = [linha[0] for linha in repo.listar_produtos()]
        assert ids == [1, 2, 3, 4]
        assert len(set(ids)) == len(ids)
        for ruim in [0, -1, "1", 1.5]:
            try:
                validar_id(ruim)
                recusou = False
            except ValueError:
                recusou = True
            assert recusou, ruim
        assert [linha[0] for linha in reversed(repo.listar_produtos())] == [4, 3, 2, 1]

        repo.adicionar_cliente("Maria D'Ávila")
        assert repo.listar_clientes() == [(1, "Maria D'Ávila")]
        try:
            repo.adicionar_cliente("")
            recusou = False
        except ValueError:
            recusou = True
        assert recusou
        assert len(repo.listar_clientes()) == 1

        # T06 - reabrir o MESMO arquivo conserva os produtos
        novo_repo = RepositorioSqlite(caminho)
        assert novo_repo.listar_produtos() == antes
        assert novo_repo.listar_clientes() == [(1, "Maria D'Ávila")]

        # T07 - falha de conexão ou de gravação não aparece como sucesso
        sem_pasta = RepositorioSqlite(os.path.join(pasta, "naoexiste", "x.db"))
        try:
            sem_pasta.iniciar()
            recusou = False
        except ValueError:
            recusou = True
        assert recusou
        try:
            sem_pasta.adicionar_produto("Teste", 500)
            recusou = False
        except ValueError:
            recusou = True
        assert recusou
        vazio = RepositorioSqlite(os.path.join(pasta, "semtabela.db"))  
        try:
            vazio.adicionar_produto("Teste", 500)
            recusou = False
        except ValueError:
            recusou = True
        assert recusou

        # T08 (parte 2) - conexões fechadas: o arquivo pode ser removido
        os.remove(caminho)
        assert not os.path.exists(caminho)

    # T09 - pedido em memória separado dos produtos do banco
    pedido = Pedido()
    pedido.adicionar(Pizza("PZ01", "Mussarela Média", "Média", 3500), "1")
    pedido.adicionar(Bebida("BB01", "Refrigerante", 600), "2")
    assert pedido.total_centavos() == 4700
    assert Pedido().linhas() == []  

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
