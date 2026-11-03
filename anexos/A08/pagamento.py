# A08: assinaturas de apoio; traga sua implementação anterior.
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re
FATORES = {'Dinheiro': '0.87', 'PIX': '0.87', 'Débito': '0.92', 'Crédito 1x': '1.00'}
LIMITE = Decimal("1000000.00")
CENTAVO = Decimal("0.01")
PADRAO = re.compile(r"[0-9]+(?:[.,][0-9]{1,2})?")

def valor_monetario(texto, permitir_zero=True):
    limpo = texto.strip()
    if PADRAO.fullmatch(limpo) is None:
        raise ValueError("Valor: use números com até duas casas, sem milhares nem sinais (ex.: 12,50).")
    try:
        valor = Decimal(limpo.replace(",", "."))  
    except InvalidOperation:
        raise ValueError("Valor: informe um número válido.")
    if valor > LIMITE:
        raise ValueError("Valor: use um valor de 0,00 a 1.000.000,00.")
    if valor == 0 and not permitir_zero:
        raise ValueError("Valor: informe um valor maior que zero.")
    return valor.quantize(CENTAVO, rounding=ROUND_HALF_UP)


def calcular_pagamento(subtotal_texto, forma):
    forma = forma.strip()
    if forma == "":
        raise ValueError("Escolha a forma de pagamento.")
    if forma not in FATORES:
        raise ValueError("Forma de pagamento desconhecida.")
    subtotal = valor_monetario(subtotal_texto)  # base original, sempre
    total = (subtotal * Decimal(FATORES[forma])).quantize(CENTAVO, rounding=ROUND_HALF_UP)
    desconto = subtotal - total  
    return subtotal, desconto, total


def preco_para_centavos(texto):
    return int(valor_monetario(texto, permitir_zero=False) * 100)