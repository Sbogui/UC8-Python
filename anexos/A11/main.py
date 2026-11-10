# A11: integre sua versão anterior; preserve-a em outra pasta.
import tkinter as tk
from tkinter import ttk, messagebox
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
previa = {"janela": None, "versao": 0, "forma": ""}

janela = tk.Tk()
janela.title("Pizzaria fictícia — A11")

ttk.Label(janela, text="Produto:").pack(anchor="w", padx=10, pady=(10, 0))
nomes = [f"{p.codigo} — {p.nome} ({formatar(p.preco_centavos)})" for p in CATALOGO]
combo = ttk.Combobox(janela, values=nomes, state="readonly", width=40)
combo.pack(padx=10)

ttk.Label(janela, text="Quantidade (1 a 999):").pack(anchor="w", padx=10, pady=(10, 0))
entrada_qtd = ttk.Entry(janela)
entrada_qtd.pack(padx=10)

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

estado = ttk.Label(janela, text="Estado: montagem")
estado.pack(anchor="w", padx=10)
total = ttk.Label(janela, text="Subtotal do pedido: R$ 0,00")
total.pack(anchor="e", padx=10)

ttk.Label(janela, text="Forma de pagamento:").pack(anchor="w", padx=10, pady=(10, 0))
forma = ttk.Combobox(janela, values=list(FATORES), state="readonly")
forma.pack(padx=10)
resumo = ttk.Label(janela, text="Escolha a forma e clique em Finalizar pedido.")
resumo.pack(anchor="w", padx=10, pady=5)

aviso = ttk.Label(janela, text="Use dados fictícios.")
aviso.pack(anchor="w", padx=10, pady=5)


def mostrar_pedido():
    tabela.delete(*tabela.get_children())
    for cod, nome, qtd, sub in pedido.linhas():
        tabela.insert("", tk.END, values=(cod, nome, qtd, formatar(sub)))
    total.configure(text="Subtotal do pedido: " + formatar(pedido.total_centavos()))
    estado.configure(text="Estado: " + pedido.estado)


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


def fechar_previa():
    if previa["janela"] is not None:
        previa["janela"].destroy()
        previa["janela"] = None


def confirmar():
    try:
        comprovante = pedido.finalizar(previa["forma"], True, previa["versao"])
    except ValueError as erro:
        fechar_previa()
        aviso.configure(text=str(erro))
        return
    fechar_previa()
    mostrar_pedido()
    resumo.configure(text=(
        f"Comprovante — {comprovante['forma']} | "
        f"Subtotal: {formatar(comprovante['subtotal_centavos'])} | "
        f"Desconto: {formatar(comprovante['desconto_centavos'])} | "
        f"Total: {formatar(comprovante['total_centavos'])}"))
    aviso.configure(text="Pedido finalizado (fictício).")


def finalizar():
    if previa["janela"] is not None:
        previa["janela"].lift()
        return
    centavos = pedido.total_centavos()
    if pedido.estado != "montagem":
        aviso.configure(text="Pedido finalizado: inicie um novo pedido.")
        return
    if centavos == 0:
        aviso.configure(text="Adicione ao menos um item antes de finalizar.")
        return
    subtotal_texto = f"{centavos // 100}.{centavos % 100:02d}"
    try:
        sub, desc, tot = calcular_pagamento(subtotal_texto, forma.get())
    except ValueError as erro:
        aviso.configure(text=str(erro))
        return

    previa["versao"] = pedido.versao
    previa["forma"] = forma.get()

    nova = tk.Toplevel(janela)
    nova.title("Confirmar pedido")
    previa["janela"] = nova
    texto = (f"Forma: {forma.get()}\n"
             f"Subtotal: {formatar(int(sub * 100))}\n"
             f"Desconto: {formatar(int(desc * 100))}\n"
             f"Total: {formatar(int(tot * 100))}")
    ttk.Label(nova, text=texto).pack(padx=20, pady=15)
    botoes_previa = ttk.Frame(nova)
    botoes_previa.pack(pady=10)
    ttk.Button(botoes_previa, text="Confirmar", command=confirmar).pack(side="left", padx=5)
    botao_cancelar = ttk.Button(botoes_previa, text="Cancelar", command=fechar_previa)
    botao_cancelar.pack(side="left", padx=5)
    nova.protocol("WM_DELETE_WINDOW", fechar_previa)       
    nova.bind("<Escape>", lambda evento: fechar_previa())   
    botao_cancelar.focus_set()                              


def novo_pedido():
    if pedido.estado == "montagem" and len(pedido.itens) > 0:
        resposta = messagebox.askyesno("Novo pedido", "Descartar o pedido em montagem?")
        if not resposta:
            aviso.configure(text="Pedido em montagem preservado.")
            return
    fechar_previa()
    pedido.novo()
    mostrar_pedido()
    forma.set("")
    combo.set("")
    entrada_qtd.delete(0, tk.END)
    resumo.configure(text="Escolha a forma e clique em Finalizar pedido.")
    aviso.configure(text="Novo pedido iniciado.")


botoes = ttk.Frame(janela)
botoes.pack(pady=10)
ttk.Button(botoes, text="Adicionar", command=adicionar).pack(side="left", padx=4)
ttk.Button(botoes, text="Atualizar", command=atualizar).pack(side="left", padx=4)
ttk.Button(botoes, text="Remover", command=remover).pack(side="left", padx=4)
ttk.Button(botoes, text="Finalizar pedido", command=finalizar).pack(side="left", padx=4)
ttk.Button(botoes, text="Novo pedido", command=novo_pedido).pack(side="left", padx=4)

janela.mainloop()