"""A03 — complete as funções antes de conectá-las à janela."""

    # TODO: ler reais e as duas cotações; aceitar vírgula ou ponto decimal.
def calcular(campos, registro):
    valores_reais = campos.get("reais", "").strip().replace(",", ".")
    valores_dolar = campos.get("cotacao_dolar", "").strip().replace(",",".")
    valores_euro = campos.get("cotacao_euro", "").strip().replace(",",".")
    
    # TODO: tratar conversão inválida, reais negativos e cotações <= 0.
    try:
        reais = float(valores_reais)
        cotacao_dolar = float(valores_dolar)
        cotacao_euro = float(valores_euro)
    except ValueError:
        return "Informe números válidos para reais e para as duas cotações."
    
    # TODO: dividir reais por cada cotação.
    if reais < 0:
        return "O valor em reais não pode ser negativo."
    if cotacao_dolar <= 0 or cotacao_euro <= 0:
        return "As cotações devem ser maiores que zero."
    
    dolares = reais / cotacao_dolar
    euros = reais / cotacao_euro
    
    # TODO: confirmar entradas e os dois resultados somente após validar tudo.
    registro.update({
        "reais": reais,
        "cotacao_dolar": cotacao_dolar,
        "cotacao_euro": cotacao_euro,
        "dolares": dolares,
        "euros": euros,
    })
    return "Conversão confirmada."


def exibir(registro):
    # TODO: tratar ausência de conversão; consultar somente registro.
    if not registro:
        return "Nenhuma conversão confirmada nesta sessão."
    # TODO: mostrar entradas usadas e resultados, estes com duas casas.
    return (
        f"R$ {registro['reais']} com R$ {registro['cotacao_dolar']} por USD "
        f"e R$ {registro['cotacao_euro']} por EUR: "
        f"{registro['dolares']:.2f} USD e {registro['euros']:.2f} EUR."
    )


def limpar(campos):
    # TODO: esvaziar os três campos; preservar registro e resultados.
    campos["reais"] = ""
    campos["cotacao_dolar"] = ""
    campos["cotacao_euro"] = ""
    pass


if __name__ == "__main__":
    campos = {"reais": "100", "cotacao_dolar": "5", "cotacao_euro": "4"}
    registro = {}
    print(exibir(registro))
    print(calcular(campos, registro))
    print(exibir(registro))
    # Acrescente as outras sequências da matriz, prevendo antes de executar.
    
    # Sequência 1: editar 200 / 10 / 8 sem calcular e só Exibir
    campos.update({"reais": "200", "cotacao_dolar": "10", "cotacao_euro": "8"})
    print(exibir(registro))

    # Sequência 2: Limpar campos e Exibir
    limpar(campos)
    print("Campos após limpar:", campos)
    print(exibir(registro))

    # Sequência 3: tentativa inválida (euro "abc") depois de um válido
    campos.update({"reais": "200", "cotacao_dolar": "10", "cotacao_euro": "abc"})
    print(calcular(campos, registro))
    print(exibir(registro))

    # Sequência 4: correção válida 200 / 10 / 8
    campos.update({"reais": "200", "cotacao_dolar": "10", "cotacao_euro": "8"})
    print(calcular(campos, registro))
    print(exibir(registro))

    # Sequência 5: reais zero (0 / 5 / 4)
    campos.update({"reais": "0", "cotacao_dolar": "5", "cotacao_euro": "4"})
    print(calcular(campos, registro))
    print(exibir(registro))

    # Sequência 6: reais negativo (-10 / 5 / 4)
    campos.update({"reais": "-10", "cotacao_dolar": "5", "cotacao_euro": "4"})
    print(calcular(campos, registro))
    print(exibir(registro))

    # Sequência 7: dólar zero (100 / 0 / 4)
    campos.update({"reais": "100", "cotacao_dolar": "0", "cotacao_euro": "4"})
    print(calcular(campos, registro))
    print(exibir(registro))

    # Sequência 8: dólar negativo (100 / -5 / 4)
    campos.update({"reais": "100", "cotacao_dolar": "-5", "cotacao_euro": "4"})
    print(calcular(campos, registro))
    print(exibir(registro))

    # Sequência 9: euro zero (100 / 5 / 0)
    campos.update({"reais": "100", "cotacao_dolar": "5", "cotacao_euro": "0"})
    print(calcular(campos, registro))
    print(exibir(registro))

    # Sequência 10: euro negativo (100 / 5 / -4)
    campos.update({"reais": "100", "cotacao_dolar": "5", "cotacao_euro": "-4"})
    print(calcular(campos, registro))
    print(exibir(registro))
