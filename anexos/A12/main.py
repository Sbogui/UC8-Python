# A12: integre sua versão anterior; preserve-a em outra pasta.
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from modelos import Pizza, Bebida, Pedido, formatar
from pagamento import FATORES, calcular_pagamento
from arquivos import validar_catalogo, ler_catalogo, salvar_catalogo

CATALOGO = [
    Pizza("PZ01", "Mussarela Média", "Média", 3500),
    Pizza("PZ02", "Mussarela Grande", "Grande", 4500),
    Pizza("PZ03", "Calabresa Média", "Média", 3800),
    Pizza("PZ04", "Calabresa Grande", "Grande", 4800),
    Bebida("BB01", "Refrigerante", 600),
    Bebida("BB02", "Suco", 700),
]

def criar_janela():
    pedido = Pedido()
    previa = {"janela": None, "versao": 0, "forma": ""}

    janela = tk.Tk()
    janela.title("Pizzaria fictícia — A12")

    abas = ttk.Notebook(janela)
    abas.pack(fill="both", expand=True)
    aba_pedido = ttk.Frame(abas)
    aba_json = ttk.Frame(abas)
    abas.add(aba_pedido, text="Pedido")
    abas.add(aba_json, text="Exercício JSON")

    # Aba Pedido (igual à A11)
    ttk.Label(aba_pedido, text="Produto:").pack(anchor="w", padx=10, pady=(10, 0))
    nomes = [f"{p.codigo} — {p.nome} ({formatar(p.preco_centavos)})" for p in CATALOGO]
    combo = ttk.Combobox(aba_pedido, values=nomes, state="readonly", width=40)
    combo.pack(padx=10)

    ttk.Label(aba_pedido, text="Quantidade (1 a 999):").pack(anchor="w", padx=10, pady=(10, 0))
    entrada_qtd = ttk.Entry(aba_pedido)
    entrada_qtd.pack(padx=10)

    tabela = ttk.Treeview(aba_pedido, columns=("cod", "nome", "qtd", "sub"), show="headings", height=6)
    tabela.heading("cod", text="Código")
    tabela.heading("nome", text="Produto")
    tabela.heading("qtd", text="Qtd")
    tabela.heading("sub", text="Subtotal")
    tabela.column("cod", width=70)
    tabela.column("nome", width=160)
    tabela.column("qtd", width=50)
    tabela.column("sub", width=100)
    tabela.pack(padx=10, pady=10, fill="both", expand=True)

    estado = ttk.Label(aba_pedido, text="Estado: montagem")
    estado.pack(anchor="w", padx=10)
    total = ttk.Label(aba_pedido, text="Subtotal do pedido: R$ 0,00")
    total.pack(anchor="e", padx=10)

    ttk.Label(aba_pedido, text="Forma de pagamento:").pack(anchor="w", padx=10, pady=(10, 0))
    forma = ttk.Combobox(aba_pedido, values=list(FATORES), state="readonly")
    forma.pack(padx=10)
    resumo = ttk.Label(aba_pedido, text="Escolha a forma e clique em Finalizar pedido.")
    resumo.pack(anchor="w", padx=10, pady=5)

    aviso = ttk.Label(aba_pedido, text="Use dados fictícios.")
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


    botoes = ttk.Frame(aba_pedido)
    botoes.pack(pady=10)
    ttk.Button(botoes, text="Adicionar", command=adicionar).pack(side="left", padx=4)
    ttk.Button(botoes, text="Atualizar", command=atualizar).pack(side="left", padx=4)
    ttk.Button(botoes, text="Remover", command=remover).pack(side="left", padx=4)
    ttk.Button(botoes, text="Finalizar pedido", command=finalizar).pack(side="left", padx=4)
    ttk.Button(botoes, text="Novo pedido", command=novo_pedido).pack(side="left", padx=4)

    # Aba Exercício JSON 
    # Esta aba é separada do pedido: carregar um JSON aqui não muda o pedido nem o CATALOGO.
    ttk.Label(aba_json, text="Catálogo em JSON (dados fictícios):").pack(anchor="w", padx=10, pady=(10, 0))
    editor = tk.Text(aba_json, width=60, height=15)
    editor.pack(padx=10, pady=5, fill="both", expand=True)
    editor.insert("1.0", '[\n  {"id": 1, "nome": "Picolé de limão", "preco_centavos": 350},\n'
                        '  {"id": 2, "nome": "Sorvete", "preco_centavos": 1200}\n]')
    aviso_json = ttk.Label(aba_json, text="Carregue um arquivo ou edite o texto.")
    aviso_json.pack(anchor="w", padx=10, pady=5)

    def carregar_json():
        caminho = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not caminho:
            return 
        try:
            dados = ler_catalogo(caminho)
        except ValueError as erro:
            aviso_json.configure(text=str(erro)) 
            return
        editor.delete("1.0", tk.END)
        editor.insert("1.0", json.dumps(dados, ensure_ascii=False, indent=2))
        aviso_json.configure(text="Arquivo carregado.")

    def salvar_json():
        texto = editor.get("1.0", tk.END)
        try:
            dados = json.loads(texto)
            validar_catalogo(dados)
        except ValueError as erro:
            aviso_json.configure(text="Não salvou: " + str(erro))
            return
        caminho = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not caminho:
            return 
        try:
            salvar_catalogo(caminho, dados)
        except ValueError as erro:
            aviso_json.configure(text=str(erro))
            return
        aviso_json.configure(text="Arquivo salvo.")

    botoes_json = ttk.Frame(aba_json)
    botoes_json.pack(pady=10)
    ttk.Button(botoes_json, text="Carregar JSON", command=carregar_json).pack(side="left", padx=4)
    ttk.Button(botoes_json, text="Salvar JSON", command=salvar_json).pack(side="left", padx=4)

    #Menu
    menu = tk.Menu(janela)
    menu_ir = tk.Menu(menu, tearoff=0)
    menu_ir.add_command(label="Pedido", command=lambda: abas.select(aba_pedido))
    menu_ir.add_command(label="Exercício JSON", command=lambda: abas.select(aba_json))
    menu.add_cascade(label="Ir para", menu=menu_ir)
    janela.config(menu=menu)
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
