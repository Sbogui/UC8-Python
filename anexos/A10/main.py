# A10: integre sua versão anterior; preserve-a em outra pasta.
import tkinter as tk
from tkinter import ttk
from modelos import Pizza, Bebida, Pedido, formatar
from pagamento import FATORES, calcular_pagamento

CATALOGO = [
    Pizza("PZ01", "Mussarela Média", "Média", 3500),
    Pizza("PZ02", "Mussarela Grande", "Grande", 4500),
    Pizza("PZ03", "Calabresa Média", "Média", 3800),
    Pizza("PZ04", "Calabresa Grande", "Grande", 4800),
    Bebida("BB01", "Refrigerante", 600),
    Bebida("BB02", "Suco", 700),
]

pedido = Pedido()

janela = tk.Tk()
janela.title("Pizzaria fictícia — A10")

# Escolha do produto e quantidade
ttk.Label(janela, text="Produto:").pack(anchor="w", padx=10, pady=(10, 0))
nomes = [f"{p.codigo} — {p.nome} ({formatar(p.preco_centavos)})" for p in CATALOGO]
combo = ttk.Combobox(janela, values=nomes, state="readonly", width=40)
combo.pack(padx=10)

ttk.Label(janela, text="Quantidade (1 a 999):").pack(anchor="w", padx=10, pady=(10, 0))
entrada_qtd = ttk.Entry(janela)
entrada_qtd.pack(padx=10)

# Tabela do pedido
tabela = ttk.Treeview(janela, columns=("cod", "nome", "qtd", "sub"), show="headings", height=6)
tabela.heading("cod", text="Código")
tabela.heading("nome", text="Produto")
tabela.heading("qtd", text="Qtd")
tabela.heading("sub", text="Subtotal")
tabela.column("cod", width=70)
tabela.column("nome", width=160)
tabela.column("qtd", width=50)
tabela.column("sub", width=100)
tabela.pack(padx=10, pady=10, fill="both", expand=True)

total = ttk.Label(janela, text="Subtotal do pedido: R$ 0,00")
total.pack(anchor="e", padx=10)

# Pagamento
ttk.Label(janela, text="Forma de pagamento:").pack(anchor="w", padx=10, pady=(10, 0))
forma = ttk.Combobox(janela, values=list(FATORES), state="readonly")
forma.pack(padx=10)
previa = ttk.Label(janela, text="Escolha a forma e confira o pagamento.")
previa.pack(anchor="w", padx=10, pady=5)

aviso = ttk.Label(janela, text="Use dados fictícios.")
aviso.pack(anchor="w", padx=10, pady=5)


def mostrar_pedido():
    tabela.delete(*tabela.get_children())
    for cod, nome, qtd, sub in pedido.linhas():
        tabela.insert("", tk.END, values=(cod, nome, qtd, formatar(sub)))
    total.configure(text="Subtotal do pedido: " + formatar(pedido.total_centavos()))
    previa.configure(text="Itens mudaram: confira o pagamento de novo.")


def adicionar():
    indice = combo.current()
    produto = None
    if indice >= 0:
        produto = CATALOGO[indice]
    try:
        pedido.adicionar(produto, entrada_qtd.get())
    except ValueError as erro:
        aviso.configure(text=str(erro))
        return
    mostrar_pedido()
    aviso.configure(text="Item adicionado.")
    entrada_qtd.delete(0, tk.END)


def codigo_da_linha():
    selecionada = tabela.selection()
    if not selecionada:
        return None
    return tabela.item(selecionada[0])["values"][0]


def atualizar():
    codigo = codigo_da_linha()
    if codigo is None:
        aviso.configure(text="Selecione uma linha da tabela.")
        return
    try:
        pedido.atualizar(codigo, entrada_qtd.get())
    except ValueError as erro:
        aviso.configure(text=str(erro))
        return
    mostrar_pedido()
    aviso.configure(text="Quantidade atualizada.")
    entrada_qtd.delete(0, tk.END)


def remover():
    codigo = codigo_da_linha()
    if codigo is None:
        aviso.configure(text="Selecione uma linha da tabela.")
        return
    try:
        pedido.remover(codigo)
    except ValueError as erro:
        aviso.configure(text=str(erro))
        return
    mostrar_pedido()
    aviso.configure(text="Item removido.")


def conferir_pagamento():
    centavos = pedido.total_centavos()
    if centavos == 0:
        aviso.configure(text="Adicione ao menos um item antes de conferir o pagamento.")
        return
    subtotal_texto = f"{centavos // 100}.{centavos % 100:02d}"
    try:
        sub, desc, tot = calcular_pagamento(subtotal_texto, forma.get())
    except ValueError as erro:
        aviso.configure(text=str(erro))
        return
    previa.configure(text=(
        f"{forma.get()} — Subtotal: {formatar(int(sub * 100))} | "
        f"Desconto: {formatar(int(desc * 100))} | "
        f"Total: {formatar(int(tot * 100))}"))
    aviso.configure(text="Pagamento conferido a partir do subtotal original.")


botoes = ttk.Frame(janela)
botoes.pack(pady=10)
ttk.Button(botoes, text="Adicionar", command=adicionar).pack(side="left", padx=4)
ttk.Button(botoes, text="Atualizar", command=atualizar).pack(side="left", padx=4)
ttk.Button(botoes, text="Remover", command=remover).pack(side="left", padx=4)
ttk.Button(botoes, text="Conferir pagamento", command=conferir_pagamento).pack(side="left", padx=4)

janela.mainloop()