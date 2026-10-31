"""A04 — complete as funções e teste as cinco notas no terminal."""
def calcular(campos, registro):
    # TODO: normalizar nome/turma e recusar texto vazio.
    nome = campos.get("nome", "").strip()
    turma = campos.get("turma", "").strip()
    if nome == "":
        return "Informe o nome."
    if turma == "":
        return "Informe a turma."
    
    # TODO: conferir a presença de exatamente cinco notas.
    textos = campos.get("notas", [])
    if len(textos) != 5:
        return "Informe exatamente cinco notas."
    
    # TODO: converter cada texto, validar de 0 a 10 e criar uma nova lista.
    notas = []
    for posicao, texto in enumerate(textos, start=1):
        try:
            nota = float(texto.strip().replace(",", "."))
        except ValueError:
            return f"Nota {posicao}: informe um número."
        if not (0 <= nota <= 10):
            return f"Nota {posicao}: use um valor de 0 a 10."
        notas.append(nota)
    
    # TODO: calcular a média com sum e len.
    media = sum(notas) / len(notas)
    
    # TODO: confirmar nome, turma, notas e média somente após validar tudo.
    registro.update({"nome": nome, "turma": turma, "notas": notas, "media": media})
    return "Registro confirmado."


def exibir(registro):
    # TODO: tratar ausência; consultar apenas o último registro confirmado.
    if not registro:
        return "Nenhum registro escolar confirmado nesta sessão."
    
    # TODO: mostrar identificação e cinco notas usadas, com média em uma casa.
    textos_notas = []
    for nota in registro["notas"]:
        textos_notas.append(str(nota))
    return (
        f"Aluno: {registro['nome']} > Turma: {registro['turma']} | "
        f"Notas: {', '.join(textos_notas)} > Média: {registro['media']:.1f}"
    )


def limpar(campos):
    # TODO: esvaziar nome, turma e os cinco textos de notas.
    # O registro confirmado não é recebido por esta função.
    campos["nome"] = ""
    campos["turma"] = ""
    campos["notas"] = ["", "", "", "", ""]


if __name__ == "__main__":
    campos = {"nome": "Lia", "turma": "T1", "notas": ["6", "7", "8", "9", "10"]}
    registro = {}
    # Acrescente as sequências da matriz, prevendo antes de executar.
    
    def tentar(nome, turma, notas):
        # Auxiliar dos cenários: digita nos campos e clica em Calcular média.
        campos["nome"] = nome
        campos["turma"] = turma
        campos["notas"] = list(notas)
        print("  ", calcular(campos, registro))
        print("  ", exibir(registro))

    # T01 e T02: abrir e Exibir; depois Lia / T1 / 6, 7, 8, 9, 10
    # Previsão: 1) "Nenhum registro escolar confirmado nesta sessão."
    #           2) "Registro confirmado."
    #           3) Lia | T1 | 6.0, 7.0, 8.0, 9.0, 10.0 | Média 8.0
    print("T01/T02")
    print(exibir(registro))
    print(calcular(campos, registro))
    print(exibir(registro))

    # T03: cinco notas zero (limite inferior inclusivo)
    # Previsão: aceito; notas 0.0 e média 0.0
    print("T03")
    tentar("Ana", "T1", ["0", "0", "0", "0", "0"])

    # T04: cinco notas 10 (limite superior inclusivo)
    # Previsão: aceito; notas 10.0 e média 10.0
    print("T04")
    tentar("Ana", "T1", ["10", "10", "10", "10", "10"])

    # T05: 7,5 / 8 / 6,5 / 9 / 7 e depois com ponto decimal
    # Previsão: os dois aceitos, soma 38, média 7.6
    print("T05")
    tentar("Bia", "T1", ["7,5", "8", "6,5", "9", "7"])
    tentar("Bia", "T1", ["7.5", "8", "6.5", "9", "7"])

    # Refazer o válido da Lia para as sequências T06 a T08
    print("Refazer Lia válido")
    tentar("Lia", "T1", ["6", "7", "8", "9", "10"])

    # T06: editar para Rui / T2 / cinco 5 e só Exibir
    # Previsão: continua Lia | T1 | 6.0 a 10.0 | Média 8.0
    print("T06")
    campos["nome"] = "Rui"
    campos["turma"] = "T2"
    campos["notas"] = ["5", "5", "5", "5", "5"]
    print("  ", exibir(registro))

    # T07: Rui / T2 / 5, 5, 5, 5, abc
    # Previsão: "Nota 5: informe um número." e o registro continua o da Lia inteiro
    print("T07")
    tentar("Rui", "T2", ["5", "5", "5", "5", "abc"])

    # T08: corrigir a quinta nota para 5
    # Previsão: confirmado; o conjunto inteiro troca: Rui | T2 | 5.0 x5 | Média 5.0
    print("T08")
    tentar("Rui", "T2", ["5", "5", "5", "5", "5"])

    # T09: nome vazio ou só espaços; turma vazia ou só espaços
    # Previsão: "Informe o nome." (2x) e "Informe a turma." (2x); registro do Rui intacto
    print("T09")
    tentar("", "T2", ["6", "6", "6", "6", "6"])
    tentar("   ", "T2", ["6", "6", "6", "6", "6"])
    tentar("Rui", "", ["6", "6", "6", "6", "6"])
    tentar("Rui", "   ", ["6", "6", "6", "6", "6"])

    # T10: cada nota vazia, só espaços ou letras, uma alteração por vez
    # Previsão: 15 recusas com "Nota N: informe um número." (N = posição alterada);
    #           registro do Rui intacto
    print("T10")
    for posicao in range(5):
        for valor in ["", "   ", "abc"]:
            notas = ["6", "6", "6", "6", "6"]
            notas[posicao] = valor
            campos["nome"] = "Rui"
            campos["turma"] = "T2"
            campos["notas"] = notas
            print("  ", repr(valor), "na nota", posicao + 1, "->", calcular(campos, registro))
    print("  ", exibir(registro))

    # T11: cada nota -0,1 ou 10,1, uma alteração por vez
    # Previsão: 10 recusas com "Nota N: use um valor de 0 a 10."; registro do Rui intacto
    print("T11")
    for posicao in range(5):
        for valor in ["-0,1", "10,1"]:
            notas = ["6", "6", "6", "6", "6"]
            notas[posicao] = valor
            campos["nome"] = "Rui"
            campos["turma"] = "T2"
            campos["notas"] = notas
            print("  ", repr(valor), "na nota", posicao + 1, "->", calcular(campos, registro))
    print("  ", exibir(registro))

    # T12: espaços nas pontas, nome composto e acentos
    # Previsão: aceito; strip só nas pontas: José da Silva | Turma 1A | 7.5, 8.0, 6.5, 9.0, 7.0 | Média 7.6
    print("T12")
    tentar("  José da Silva  ", "  Turma 1A  ", [" 7,5 ", "8 ", " 6,5", "9", "  7  "])

    # T13: depois de um válido, Limpar campos e Exibir
    # Previsão: campos vazios (nome "", turma "", cinco "") e o registro continua o do José
    print("T13")
    limpar(campos)
    print("  campos:", campos)
    print("  ", exibir(registro))

    # T14: 6 / 6 / 6 / 6 / 6,4
    # Previsão: média guardada perto de 6.08 e exibida 6.1
    print("T14")
    tentar("Ana", "T1", ["6", "6", "6", "6", "6,4"])
    print("   guardada:", registro["media"])

    # T15: lista com quatro notas e depois seis
    # Previsão: "Informe exatamente cinco notas." nas duas; registro da Ana intacto
    print("T15")
    tentar("Ana", "T1", ["6", "6", "6", "6"])
    tentar("Ana", "T1", ["6", "6", "6", "6", "6", "6"])

    # T16: fechar e reabrir (registro novo vazio) e Exibir
    # Previsão: "Nenhum registro escolar confirmado nesta sessão."
    print("T16")
    registro = {}
    print("  ", exibir(registro))
