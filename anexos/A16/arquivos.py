# A15: assinaturas de apoio; traga sua implementação anterior.
from pathlib import Path
import json
import os
import tempfile

def validar_catalogo(dados):
    if type(dados) != list:
        raise ValueError("O JSON deve ser uma lista de produtos.")
    ids = []
    for produto in dados:
        if type(produto) != dict:
            raise ValueError("Cada produto deve ser um objeto com id, nome e preco_centavos.")
        for chave in ["id", "nome", "preco_centavos"]:
            if chave not in produto:
                raise ValueError("Falta o campo " + chave + ".")
        if type(produto["id"]) != int or produto["id"] <= 0:
            raise ValueError("O id deve ser um número inteiro positivo.")
        if produto["id"] in ids:
            raise ValueError("O id " + str(produto["id"]) + " está repetido.")
        ids.append(produto["id"])
        if type(produto["nome"]) != str or produto["nome"].strip() == "":
            raise ValueError("O nome deve ser um texto não vazio.")
        if type(produto["preco_centavos"]) != int or produto["preco_centavos"] <= 0:
            raise ValueError("O preço deve ser um número inteiro positivo, em centavos.")
    return dados


def ler_catalogo(caminho):
    caminho = Path(caminho)
    if not caminho.exists():
        return []  
    try:
        conteudo = caminho.read_bytes()
    except OSError:
        raise ValueError("Não foi possível abrir o arquivo.")
    try:
        texto = conteudo.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("O arquivo não está em UTF-8. Ele foi mantido sem alteração.")
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError:
        raise ValueError("O arquivo tem erro de JSON (confira vírgulas e aspas). Ele foi mantido sem alteração.")
    return validar_catalogo(dados)


def salvar_catalogo(caminho, dados):
    validar_catalogo(dados)
    caminho = Path(caminho)
    texto = json.dumps(dados, ensure_ascii=False, indent=2)
    temporario = None
    try:
        identificador, temporario = tempfile.mkstemp(dir=caminho.parent, suffix=".tmp")
        with os.fdopen(identificador, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)
        os.replace(temporario, caminho)
    except OSError:
        if temporario is not None and os.path.exists(temporario):
            os.remove(temporario)
        raise ValueError("Não foi possível salvar. O arquivo anterior foi mantido.")