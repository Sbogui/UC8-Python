# Complete os casos do registro; não marque sucesso sem verificá-los.

# TODO: criar dados fictícios, executar e comparar com assert.
# TODO: testar erro após válido, limites e uma correção com nova execução.
import os
import tempfile
from arquivos import ler_catalogo, salvar_catalogo, validar_catalogo
from modelos import Pizza, Bebida, Pedido
from pagamento import calcular_pagamento


def ler_bytes(caminho):
    with open(caminho, "rb") as arquivo:
        return arquivo.read()


def gravar_bytes(caminho, conteudo):
    with open(caminho, "wb") as arquivo:
        arquivo.write(conteudo)


def verificar():
    # Os arquivos de teste ficam numa pasta temporária que some no final.
    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "catalogo.json")
        bom = [{"id": 1, "nome": "Picolé de limão", "preco_centavos": 350},
            {"id": 2, "nome": "Sorvete", "preco_centavos": 1200}]

        # T01 - arquivo ausente: lista vazia e o arquivo não é criado
        assert ler_catalogo(caminho) == []
        assert not os.path.exists(caminho)

        # T02 - UTF-8 conserva Picolé e limão
        salvar_catalogo(caminho, bom)
        assert "Picolé de limão".encode("utf-8") in ler_bytes(caminho)
        assert ler_catalogo(caminho) == bom

        # T03 - JSON quebrado ou encoding inválido não são sobrescritos
        quebrado = b'[{"id": 3 "nome": "Sem virgula", "preco_centavos": 100}]'
        gravar_bytes(caminho, quebrado)
        try:
            ler_catalogo(caminho)
            recusou = False
        except ValueError:
            recusou = True
        assert recusou
        assert ler_bytes(caminho) == quebrado

        latin1 = "Picolé".encode("latin-1")
        gravar_bytes(caminho, latin1)
        try:
            ler_catalogo(caminho)
            recusou = False
        except ValueError:
            recusou = True
        assert recusou
        assert ler_bytes(caminho) == latin1

        # T04 - estrutura errada, id repetido e preço inválido são recusados
        ruins = [
            {"id": 1, "nome": "X", "preco_centavos": 100},
            ["texto"],
            [{"id": 1, "nome": "X"}],
            [{"id": 1, "nome": "A", "preco_centavos": 100},
            {"id": 1, "nome": "B", "preco_centavos": 200}],
            [{"id": 0, "nome": "X", "preco_centavos": 100}],
            [{"id": "1", "nome": "X", "preco_centavos": 100}],
            [{"id": 1, "nome": "  ", "preco_centavos": 100}],
            [{"id": 1, "nome": "X", "preco_centavos": "250"}],
            [{"id": 1, "nome": "X", "preco_centavos": 0}],
        ]
        for ruim in ruins:
            try:
                validar_catalogo(ruim)
                recusou = False
            except ValueError:
                recusou = True
            assert recusou, ruim

        # T05 - falha ao salvar mantém o arquivo anterior
        salvar_catalogo(caminho, bom)
        antes = ler_bytes(caminho)
        try:
            salvar_catalogo(caminho, [{"id": 1, "nome": "X", "preco_centavos": 0}])
            recusou = False
        except ValueError:
            recusou = True
        assert recusou
        assert ler_bytes(caminho) == antes

        # destino impossível: uma pasta com o nome do arquivo (com um arquivo dentro)
        destino = os.path.join(pasta, "catalogo2.json")
        os.mkdir(destino)
        gravar_bytes(os.path.join(destino, "dentro.txt"), b"nao mexer")
        try:
            salvar_catalogo(destino, [{"id": 9, "nome": "Novo", "preco_centavos": 500}])
            recusou = False
        except ValueError:
            recusou = True
        assert recusou
        assert ler_bytes(os.path.join(destino, "dentro.txt")) == b"nao mexer"
        for nome in os.listdir(pasta):
            assert not nome.endswith(".tmp"), nome 
        assert ler_bytes(caminho) == antes 

    # Caso anterior (A10/A11): pizza e duas bebidas
    pedido = Pedido()
    pedido.adicionar(Pizza("PZ01", "Mussarela Média", "Média", 3500), "1")
    pedido.adicionar(Bebida("BB01", "Refrigerante", 600), "2")
    assert pedido.total_centavos() == 4700
    sub, desc, total = calcular_pagamento("47.00", "PIX")
    assert str(total) == "40.89"

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
