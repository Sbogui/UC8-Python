"""A01 — prática 2. Esqueleto funcional de janela, sem validação pronta."""
import tkinter as tk
from tkinter import ttk


def conferir_cadastro():
    nome = entrada_nome.get()
    idade_texto = entrada_idade.get()

    nome_limpo = nome.strip()
    if not nome_limpo:
        resultado.configure(text="O nome não pode ficar vazio!")
        return

    try:
        idade_numero = int(idade_texto)
    except ValueError:
        resultado.configure(text="Coloque a idade como número inteiro!")
        return

    if idade_numero <= 0:
        resultado.configure(text="A idade tem que ser maior que 0!")
        return

    resultado.configure(
        text=f"Conferencia do cadastro.\nNome: {nome_limpo}\nIdade: {idade_numero} anos"
    )


janela = tk.Tk()
janela.title("Conferir cadastro fictício")
janela.columnconfigure(1, weight=1)
ttk.Label(janela, text="Nome fictício:").grid(row=0, column=0, padx=12, pady=8, sticky="w")
entrada_nome = ttk.Entry(janela)
entrada_nome.grid(row=0, column=1, padx=12, pady=8, sticky="ew")
ttk.Label(janela, text="Idade fictícia:").grid(row=1, column=0, padx=12, pady=8, sticky="w")
entrada_idade = ttk.Entry(janela)
entrada_idade.grid(row=1, column=1, padx=12, pady=8, sticky="ew")
ttk.Button(janela, text="Conferir cadastro", command=conferir_cadastro).grid(row=2, column=0, columnspan=2, pady=8)
resultado = ttk.Label(janela, text="Nenhum cadastro conferido nesta sessão.", wraplength=360)
resultado.grid(row=3, column=0, columnspan=2, padx=12, pady=8, sticky="w")
entrada_nome.focus_set()
janela.mainloop()
