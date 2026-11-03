# A08: integre sua versão anterior; preserve-a em outra pasta.
import tkinter as tk
from tkinter import ttk
from modelos import Produto, Pedido, formatar
from pagamento import FATORES, calcular_pagamento, preco_para_centavos

CATALOGO = [
    Produto("P01", "Fruta", preco_para_centavos("5,00")),
    Produto("P02", "Leite", preco_para_centavos("7,50")),
    Produto("P03", "Pão", preco_para_centavos("3,20")),
]


def centavos_do_decimal(valor):
    return int(valor * 100)


def criar_janela():
    janela = tk.Tk()
    janela.title("Sorveteria fictícia — A08")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    base.rowconfigure(2, weight=1)
    estado = {"pedido": Pedido()}  

    escolha = ttk.LabelFrame(base, text="Novo item", padding=8)

    escolha = ttk.LabelFrame(base, text="Novo item", padding=8)
    escolha.grid(row=0, column=0, pady=6, sticky="ew")
    escolha.columnconfigure(1, weight=1)
    ttk.Label(escolha, text="Produto:").grid(row=0, column=0, padx=6, pady=4, sticky="w")
    nomes = [f"{p.codigo} — {p.nome} ({formatar(p.preco_centavos)})" for p in CATALOGO]
    combo = ttk.Combobox(escolha, values=nomes, state="readonly")
    combo.grid(row=0, column=1, padx=6, pady=4, sticky="ew")
    ttk.Label(escolha, text="Quantidade (1 a 999):").grid(row=1, column=0, padx=6, pady=4, sticky="w")
    entrada_qtd = ttk.Entry(escolha)
    entrada_qtd.grid(row=1, column=1, padx=6, pady=4, sticky="ew")

    ttk.Label(base, text="Itens do pedido").grid(row=1, column=0, sticky="w")
    tabela = ttk.Treeview(base, columns=("cod", "nome", "qtd", "sub"), show="headings", height=5)
    for coluna, titulo, largura in [("cod", "Código", 70), ("nome", "Produto", 140), ("qtd", "Qtd", 60), ("sub", "Subtotal", 100)]:
        tabela.heading(coluna, text=titulo)
        tabela.column(coluna, width=largura, anchor="w")
    tabela.grid(row=2, column=0, pady=6, sticky="nsew")
    total_pedido = ttk.Label(base, text="Subtotal do pedido: R$ 0,00")
    total_pedido.grid(row=3, column=0, pady=2, sticky="e")

    pagamento = ttk.LabelFrame(base, text="Pagamento (regras fictícias)", padding=8)
    pagamento.grid(row=4, column=0, pady=6, sticky="ew")
    pagamento.columnconfigure(1, weight=1)
    ttk.Label(pagamento, text="Forma:").grid(row=0, column=0, padx=6, pady=4, sticky="w")
    forma = ttk.Combobox(pagamento, values=list(FATORES), state="readonly")
    forma.grid(row=0, column=1, padx=6, pady=4, sticky="ew")
    previa = ttk.Label(pagamento, text="Escolha a forma e confira o pagamento.", wraplength=400)
    previa.grid(row=2, column=0, columnspan=2, padx=6, pady=4, sticky="w")
    aviso = ttk.Label(base, text="Use dados fictícios.", wraplength=430)
    aviso.grid(row=6, column=0, pady=4, sticky="w")

    def atualizar_tela():
        tabela.delete(*tabela.get_children())
        for cod, nome, qtd, sub in estado["pedido"].linhas():
            tabela.insert("", tk.END, values=(cod, nome, qtd, formatar(sub)))
        total_pedido.configure(text=f"Subtotal do pedido: {formatar(estado['pedido'].total_centavos())}")
        previa.configure(text="Itens mudaram: confira o pagamento de novo.")

    def ao_adicionar():
        indice = combo.current()
        produto = CATALOGO[indice] if indice >= 0 else None
        try:
            estado["pedido"].adicionar(produto, entrada_qtd.get())
        except ValueError as erro:
            aviso.configure(text=str(erro))  
            return
        atualizar_tela()
        aviso.configure(text="Item adicionado.")
        entrada_qtd.delete(0, tk.END)
        entrada_qtd.focus_set()

    def ao_conferir():
        centavos = estado["pedido"].total_centavos()
        if centavos == 0:
            aviso.configure(text="Adicione ao menos um item antes de conferir o pagamento.")
            return
        subtotal_texto = f"{centavos // 100}.{centavos % 100:02d}"
        try:
            sub, desc, tot = calcular_pagamento(subtotal_texto, forma.get())
        except ValueError as erro:
            aviso.configure(text=str(erro)) 
            forma.focus_set()
            return
        previa.configure(text=(
            f"{forma.get()} — Subtotal: {formatar(centavos_do_decimal(sub))} | "
            f"Desconto: {formatar(centavos_do_decimal(desc))} | "
            f"Total: {formatar(centavos_do_decimal(tot))}"))
        aviso.configure(text="Pagamento conferido a partir do subtotal original.")

    def ao_novo_pedido():
        estado["pedido"] = Pedido()
        atualizar_tela()
        combo.set("")
        forma.set("")
        entrada_qtd.delete(0, tk.END)
        previa.configure(text="Escolha a forma e confira o pagamento.")
        aviso.configure(text="Novo pedido iniciado.")

    acoes = ttk.Frame(base)
    acoes.grid(row=5, column=0, pady=6, sticky="ew")
    for coluna in range(3):
        acoes.columnconfigure(coluna, weight=1)
    ttk.Button(acoes, text="Adicionar", command=ao_adicionar).grid(row=0, column=0, padx=4)
    ttk.Button(acoes, text="Conferir pagamento", command=ao_conferir).grid(row=0, column=1, padx=4)
    ttk.Button(acoes, text="Novo pedido", command=ao_novo_pedido).grid(row=0, column=2, padx=4)
    entrada_qtd.bind("<Return>", lambda evento: ao_adicionar())
    combo.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
