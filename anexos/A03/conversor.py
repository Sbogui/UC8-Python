"""A03 — complete a lógica e os callbacks do conversor."""
import tkinter as tk
from tkinter import ttk


def calcular(campos, registro):
    # TODO: ler reais e as duas cotações; aceitar vírgula ou ponto decimal.
    texto_reais = campos.get("reais", "").strip().replace(",", ".")
    texto_dolar = campos.get("cotacao_dolar", "").strip().replace(",", ".")
    texto_euro = campos.get("cotacao_euro", "").strip().replace(",", ".")
    
    # TODO: tratar conversão inválida, reais negativos e cotações <= 0.
    try:
        reais = float(texto_reais)
        cotacao_dolar = float(texto_dolar)
        cotacao_euro = float(texto_euro)
    except ValueError:
        return "Informe números válidos para reais e para as duas cotações."
    
    if reais < 0:
        return "O valor em reais não pode ser negativo."
    if cotacao_dolar <= 0 or cotacao_euro <= 0:
        return "As cotações devem ser maiores que zero."
    
    # TODO: dividir reais por cada cotação.
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
        f"Última conversão confirmada: R$ {registro['reais']} com "
        f"R$ {registro['cotacao_dolar']} por USD e R$ {registro['cotacao_euro']} por EUR: "
        f"{registro['dolares']:.2f} USD e {registro['euros']:.2f} EUR."
    )



def limpar(campos):
    campos["reais"] = ""
    campos["cotacao_dolar"] = ""
    campos["cotacao_euro"] = ""



def criar_janela():
    janela = tk.Tk()
    janela.title("Conversor com cotações fictícias — A03")
    janela.columnconfigure(1, weight=1)
    campos = {"reais": "", "cotacao_dolar": "", "cotacao_euro": ""}
    registro = {}

    ttk.Label(janela, text="Cotações fictícias manuais; sem consulta à internet.", wraplength=420).grid(row=0, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    ttk.Label(janela, text="Valor em reais (R$):").grid(row=1, column=0, padx=12, pady=6, sticky="w")
    entrada_reais = ttk.Entry(janela)
    entrada_reais.grid(row=1, column=1, padx=12, pady=6, sticky="ew")
    ttk.Label(janela, text="R$ por 1 USD:").grid(row=2, column=0, padx=12, pady=6, sticky="w")
    entrada_dolar = ttk.Entry(janela)
    entrada_dolar.grid(row=2, column=1, padx=12, pady=6, sticky="ew")
    ttk.Label(janela, text="R$ por 1 EUR:").grid(row=3, column=0, padx=12, pady=6, sticky="w")
    entrada_euro = ttk.Entry(janela)
    entrada_euro.grid(row=3, column=1, padx=12, pady=6, sticky="ew")

    def ao_calcular():
        # TODO: ler os três Entry, calcular e atualizar aviso/último confirmado.
        campos["reais"] = entrada_reais.get()
        campos["cotacao_dolar"] = entrada_dolar.get()
        campos["cotacao_euro"] = entrada_euro.get()
        aviso.configure(text=calcular(campos, registro))
        
        resultado.configure(text=exibir(registro))

    def ao_exibir():
        resultado.configure(text=exibir(registro))
        aviso.configure(text="Consulta ao último conjunto confirmado.")

    def ao_limpar():
        limpar(campos)
        entrada_reais.delete(0, tk.END)
        entrada_dolar.delete(0, tk.END)
        entrada_euro.delete(0, tk.END)
        entrada_reais.focus_set()
        aviso.configure(text="Campos limpos. O último conjunto confirmado foi mantido.")

    ttk.Button(janela, text="Calcular", command=ao_calcular).grid(row=4, column=0, padx=12, pady=8)
    ttk.Button(janela, text="Exibir", command=ao_exibir).grid(row=4, column=1, padx=12, pady=8)
    ttk.Button(janela, text="Limpar campos", command=ao_limpar).grid(row=5, column=0, columnspan=2, pady=6)
    aviso = ttk.Label(janela, text="Use vírgula ou ponto decimal, sem milhares.", wraplength=420)
    aviso.grid(row=6, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    resultado = ttk.Label(janela, text="Nenhuma conversão confirmada nesta sessão.", wraplength=420)
    resultado.grid(row=7, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    entrada_reais.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
