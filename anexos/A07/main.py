# A07: integre sua versão anterior; preserve-a em outra pasta.
import tkinter as tk
from tkinter import ttk
from modelos import Produto, Pedido, formatar

CATALOGO = [
    Produto("P01", "Fruta", 500),
    Produto("P02", "Leite", 750),
    Produto("P03", "Pão", 320),
]


def criar_janela():
    janela = tk.Tk()
    janela.title("Pedido fictício — A07")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    base.rowconfigure(2, weight=1)
    estado = {"pedido": Pedido()} 

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
    tabela = ttk.Treeview(base, columns=("cod", "nome", "qtd", "sub"), show="headings", height=6)
    for coluna, titulo, largura in [("cod", "Código", 70), ("nome", "Produto", 140), ("qtd", "Qtd", 60), ("sub", "Subtotal", 100)]:
        tabela.heading(coluna, text=titulo)
        tabela.column(coluna, width=largura, anchor="w")
    tabela.grid(row=2, column=0, pady=6, sticky="nsew")

    aviso = ttk.Label(base, text="Use dados fictícios.", wraplength=430)
    aviso.grid(row=4, column=0, pady=4, sticky="w")
    total = ttk.Label(base, text="Total: R$ 0,00")
    total.grid(row=3, column=0, pady=4, sticky="e")

    def atualizar_tela():
        tabela.delete(*tabela.get_children())
        for cod, nome, qtd, sub in estado["pedido"].linhas():
            tabela.insert("", tk.END, values=(cod, nome, qtd, formatar(sub)))
        total.configure(text=f"Total: {formatar(estado['pedido'].total_centavos())}")

    def ao_adicionar():
        indice = combo.current()
        produto = CATALOGO[indice] if indice >= 0 else None
        try:
            estado["pedido"].adicionar(produto, entrada_qtd.get())
        except ValueError as erro:
            aviso.configure(text=str(erro))  # pedido preservado
            return
        atualizar_tela()
        aviso.configure(text="Item adicionado.")
        entrada_qtd.delete(0, tk.END)
        entrada_qtd.focus_set()

    def ao_novo_pedido():
        estado["pedido"] = Pedido()
        atualizar_tela()
        combo.set("")
        entrada_qtd.delete(0, tk.END)
        aviso.configure(text="Novo pedido iniciado.")

    acoes = ttk.Frame(base)
    acoes.grid(row=5, column=0, pady=6, sticky="ew")
    acoes.columnconfigure(0, weight=1)
    acoes.columnconfigure(1, weight=1)
    ttk.Button(acoes, text="Adicionar", command=ao_adicionar).grid(row=0, column=0, padx=4)
    ttk.Button(acoes, text="Novo pedido", command=ao_novo_pedido).grid(row=0, column=1, padx=4)
    entrada_qtd.bind("<Return>", lambda evento: ao_adicionar())
    combo.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
