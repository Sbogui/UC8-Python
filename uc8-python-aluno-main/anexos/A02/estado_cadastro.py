
"""A02 — prática 1: campos em edição e registro confirmado."""


def registrar(campos, registro):
    nome = campos["nome"].strip()
    sobrenome = campos["sobrenome"].strip()
    idade_texto = campos["idade"].strip()

    if not nome:
        return "Preencha o nome."

    if not sobrenome:
        return "Preencha o sobrenome."

    try:
        idade = int(idade_texto)
    except ValueError:
        return "Coloque a idade como número inteiro!"

    if idade <= 0:
        return "A idade tem que ser maior que 0!"

    registro["nome"] = nome
    registro["sobrenome"] = sobrenome
    registro["idade"] = idade

    return (
        f"Cadastro registrado. Nome: {nome} {sobrenome} "
        f"| Idade: {idade} anos"
    )


def exibir(registro):
    if not registro:
        return "Nenhum registro confirmado."

    return (
        f"Nome: {registro['nome']} {registro['sobrenome']} "
        f"| Idade: {registro['idade']} anos"
    )


def limpar(campos):
    campos["nome"] = ""
    campos["sobrenome"] = ""
    campos["idade"] = ""


if __name__ == "__main__":
    campos = {"nome": "Lia", "sobrenome": "Costa", "idade": "18"}
    registro = {}

    # Cenário 1:  uma pessoa válida
    print(registrar(campos, registro))
    print(exibir(registro))

    # Cenário 2: limpar sem apagar o registro
    limpar(campos)
    print("Campos após limpar:", campos)
    print(exibir(registro))

    # Cenário 3: tentativa inválida preserva o registro anterior
    campos = {"nome": "Lia", "sobrenome": "Costa", "idade": "abc"}
    print(registrar(campos, registro))
    print("Após tentativa inválida:", exibir(registro))

    # Cenário 4: idade zero
    campos = {"nome": "Lia", "sobrenome": "Costa", "idade": "0"}
    print(registrar(campos, registro))
    print("Após idade zero:", exibir(registro))

    # Cenário 5: nome vazio
    campos = {"nome": "   ", "sobrenome": "Costa", "idade": "18"}
    print(registrar(campos, registro))
    print("Após nome vazio:", exibir(registro))

    # Cenário 6: novo cadastro válido substitui o anterior
    campos = {"nome": "Ana", "sobrenome": "Maria", "idade": "21"}
    print(registrar(campos, registro))
    print("Registro atualizado:", exibir(registro))
