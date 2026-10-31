"""A05 — complete: Escolar em grupos — A05."""
import tkinter as tk
from tkinter import ttk
from math import isfinite


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
    textos_notas = []
    for nota in registro["notas"]:
        textos_notas.append(str(nota))
    return (
        f"Aluno: {registro['nome']} | Turma: {registro['turma']} | "
        f"Notas: {', '.join(textos_notas)} | Média: {registro['media']:.1f}"
    )

    # TODO: mostrar identificação e cinco notas usadas, com média em uma casa.
    return (
        f"Aluno: {registro['nome']} | Turma: {registro['turma']} | "
        f"Notas: {', '.join(textos_notas)} | Média: {registro['media']:.1f}"
    )

def limpar(campos):
    # TODO: esvaziar nome, turma e os cinco textos de notas.
    # O registro confirmado não é recebido por esta função.
    campos["nome"] = ""
    campos["turma"] = ""
    campos["notas"] = ["", "", "", "", ""]


def criar_janela():
    janela = tk.Tk()
    janela.title("Escolar em grupos — A05")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    campos = {"nome": "", "turma": "", "notas": ["", "", "", "", ""]}
    registro = {}
    ttk.Label(base, text="Sistema escolar fictício — organize os campos").grid(row=0, column=0, columnspan=2, pady=6, sticky="w")
    # TODO: criar LabelFrame para identificação e notas e Frame para ações.
    # TODO: posicionar os grupos na base e configurar expansão das colunas.
    # A disposição inicial é plana; substitua os pais e ajuste as linhas internas.
    identificacao = ttk.LabelFrame(base, text="Identificação", padding=8)
    identificacao.grid(row=1, column=0, pady=6, sticky="ew")
    identificacao.columnconfigure(1, weight=1)
    grupo_notas = ttk.LabelFrame(base, text="Notas (0 a 10)", padding=8)
    grupo_notas.grid(row=2, column=0, pady=6, sticky="ew")
    grupo_notas.columnconfigure(1, weight=1)
    acoes = ttk.Frame(base)
    acoes.grid(row=3, column=0, pady=6, sticky="ew")
    acoes.columnconfigure(0, weight=1)
    acoes.columnconfigure(1, weight=1)
    
    identificacao = base
    grupo_notas = base
    acoes = base
    base.columnconfigure(1, weight=1)

    ttk.Label(identificacao, text="Nome fictício:").grid(row=1, column=0, padx=6, pady=4, sticky="w")
    entrada_nome = ttk.Entry(identificacao)
    entrada_nome.grid(row=1, column=1, padx=6, pady=4, sticky="ew")
    ttk.Label(identificacao, text="Turma fictícia:").grid(row=2, column=0, padx=6, pady=4, sticky="w")
    entrada_turma = ttk.Entry(identificacao)
    entrada_turma.grid(row=2, column=1, padx=6, pady=4, sticky="ew")
    entradas_notas = []
    for numero in range(1, 6):
        ttk.Label(grupo_notas, text=f"Nota {numero} (0 a 10):").grid(row=numero+2, column=0, padx=6, pady=4, sticky="w")
        entrada = ttk.Entry(grupo_notas)
        entrada.grid(row=numero+2, column=1, padx=6, pady=4, sticky="ew")
        entradas_notas.append(entrada)

    def ao_calcular():
        # TODO: reutilizar a leitura, validação e confirmação da sua A04.
        campos["nome"] = entrada_nome.get()
        campos["turma"] = entrada_turma.get()
        textos = []
        for entrada in entradas_notas:
            textos.append(entrada.get())
        campos["notas"] = textos
        aviso.configure(text=calcular(campos, registro))
        resultado.configure(text=exibir(registro))

    def ao_exibir():
        # TODO: consultar o último confirmado; na prática 2, abrir a Toplevel.
        resultado.configure(text=exibir(registro))
        aviso.configure(text="Consulta ao último registro confirmado.")

    def ao_limpar():
        # TODO: limpar as sete entradas sem apagar o último confirmado.
        limpar(campos)
        entrada_nome.delete(0, tk.END)
        entrada_turma.delete(0, tk.END)
        for entrada in entradas_notas:
            entrada.delete(0, tk.END)
        entrada_nome.focus_set()
        aviso.configure(text="Campos limpos. O último registro confirmado foi mantido.")

    ttk.Button(acoes, text="Calcular média", command=ao_calcular).grid(row=8, column=0, padx=4, pady=6)
    ttk.Button(acoes, text="Exibir", command=ao_exibir).grid(row=8, column=1, padx=4, pady=6)
    ttk.Button(acoes, text="Limpar campos", command=ao_limpar).grid(row=9, column=0, columnspan=2, padx=4, pady=6)
    aviso = ttk.Label(base, text="Use dados fictícios e confira as cinco notas.", wraplength=430)
    aviso.grid(row=10, column=0, columnspan=2, pady=6, sticky="w")
    resultado = ttk.Label(base, text="Nenhum registro escolar confirmado nesta sessão.", wraplength=430)
    resultado.grid(row=11, column=0, columnspan=2, pady=6, sticky="w")
    entrada_nome.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
