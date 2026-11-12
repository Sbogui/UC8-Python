# A14: integre sua versão anterior; preserve-a em outra pasta.

import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from modelos import Pizza, Bebida, Pedido, formatar
from pagamento import FATORES, calcular_pagamento, preco_para_centavos
from arquivos import validar_catalogo, ler_catalogo, salvar_catalogo
from relatorios import exportar_csv
from perfis import SessaoDemo, PERFIS
from repositorio import RepositorioSqlite

CAMINHO_BANCO = Path(__file__).with_name("pizzaria_a14.db")

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
    sessao = SessaoDemo()
    repositorio = RepositorioSqlite(CAMINHO_BANCO)
    previa = {"janela": None, "versao": 0, "forma": ""}

    janela = tk.Tk()
    janela.title("Pizzaria fictícia — A14")

    abas = ttk.Notebook(janela)
    abas.pack(fill="both", expand=True)
    aba_pedido = ttk.Frame(abas)
    aba_json = ttk.Frame(abas)
    aba_produtos = ttk.Frame(abas)
    aba_perfil = ttk.Frame(abas)
    abas.add(aba_pedido, text="Pedido")
    abas.add(aba_produtos, text="Produtos")
    abas.add(aba_perfil, text="Perfil (simulação)")
    abas.add(aba_json, text="Exercício JSON", state="disabled")

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


    def exportar():
        comprovante = None
        if pedido.comprovante is not None:
            comprovante = pedido.ver_comprovante()
        if comprovante is None:
            aviso.configure(text="Finalize o pedido antes de exportar o relatório.")
            return
        caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not caminho:
            return  
        try:
            exportar_csv(caminho, comprovante)
        except ValueError as erro:
            aviso.configure(text=str(erro))  
            return
        aviso.configure(text="Relatório exportado (comprovante didático, sem valor fiscal).")


    botoes = ttk.Frame(aba_pedido)
    botoes.pack(pady=10)
    ttk.Button(botoes, text="Adicionar", command=adicionar).pack(side="left", padx=4)
    ttk.Button(botoes, text="Atualizar", command=atualizar).pack(side="left", padx=4)
    ttk.Button(botoes, text="Remover", command=remover).pack(side="left", padx=4)
    ttk.Button(botoes, text="Finalizar pedido", command=finalizar).pack(side="left", padx=4)
    ttk.Button(botoes, text="Novo pedido", command=novo_pedido).pack(side="left", padx=4)
    ttk.Button(botoes, text="Exportar CSV", command=exportar).pack(side="left", padx=4)

    ttk.Label(aba_json, text="Catálogo em JSON (dados fictícios):").pack(anchor="w", padx=10, pady=(10, 0))
    editor = tk.Text(aba_json, width=60, height=15)
    editor.pack(padx=10, pady=5, fill="both", expand=True)
    editor.insert("1.0", '[\n  {"id": 1, "nome": "Picolé de limão", "preco_centavos": 350},\n' '  {"id": 2, "nome": "Sorvete", "preco_centavos": 1200}\n]')
    aviso_json = ttk.Label(aba_json, text="Carregue um arquivo ou edite o texto.")
    aviso_json.pack(anchor="w", padx=10, pady=5)


    def carregar_json():
        if not sessao.pode_configurar():
            aviso_json.configure(text="Sem permissão: entre como Administração.")
            return
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
        if not sessao.pode_configurar():
            aviso_json.configure(text="Sem permissão: entre como Administração.")
            return
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

    ttk.Label(aba_produtos, text="Banco de dados: " + str(CAMINHO_BANCO), wraplength=420).pack(anchor="w", padx=10, pady=(10, 0))
    ttk.Label(aba_produtos, text="Nome do produto:").pack(anchor="w", padx=10, pady=(10, 0))
    entrada_produto = ttk.Entry(aba_produtos, width=40)
    entrada_produto.pack(padx=10)
    ttk.Label(aba_produtos, text="Preço (ex.: 7,50):").pack(anchor="w", padx=10, pady=(10, 0))
    entrada_preco = ttk.Entry(aba_produtos, width=20)
    entrada_preco.pack(padx=10)

    tabela_produtos = ttk.Treeview(aba_produtos, columns=("id", "nome", "preco"), show="headings", height=8)
    tabela_produtos.heading("id", text="ID")
    tabela_produtos.heading("nome", text="Produto")
    tabela_produtos.heading("preco", text="Preço")
    tabela_produtos.column("id", width=50)
    tabela_produtos.column("nome", width=220)
    tabela_produtos.column("preco", width=100)
    tabela_produtos.pack(padx=10, pady=10, fill="both", expand=True)

    aviso_produtos = ttk.Label(aba_produtos, text="Use dados fictícios.", wraplength=420)
    aviso_produtos.pack(anchor="w", padx=10, pady=5)


    def mostrar_produtos():
        tabela_produtos.delete(*tabela_produtos.get_children())
        for codigo, nome, preco in repositorio.listar_produtos():
            tabela_produtos.insert("", tk.END, iid=str(codigo), values=(codigo, nome, formatar(preco)))


    def salvar_produto():
        try:
            preco = preco_para_centavos(entrada_preco.get())
            novo_id = repositorio.adicionar_produto(entrada_produto.get(), preco)
        except ValueError as erro:
            aviso_produtos.configure(text=str(erro))  
            return
        try:
            mostrar_produtos()
        except ValueError as erro:
            aviso_produtos.configure(text="Produto salvo (ID " + str(novo_id) + "), mas a lista não atualizou: " + str(erro))
            return
        aviso_produtos.configure(text="Produto salvo com ID " + str(novo_id) + ".")
        entrada_produto.delete(0, tk.END)
        entrada_preco.delete(0, tk.END)
        entrada_produto.focus_set()


    ttk.Button(aba_produtos, text="Salvar produto", command=salvar_produto).pack(pady=10)

    try:
        repositorio.iniciar()
        mostrar_produtos()
    except ValueError as erro:
        aviso_produtos.configure(text=str(erro))

    ttk.Label(aba_perfil, text="Simulação de perfil: não autentica usuários reais.").pack(anchor="w", padx=10, pady=(10, 0))
    ttk.Label(aba_perfil, text="Nome fictício:").pack(anchor="w", padx=10, pady=(10, 0))
    entrada_nome = ttk.Entry(aba_perfil)
    entrada_nome.pack(padx=10)
    ttk.Label(aba_perfil, text="Perfil:").pack(anchor="w", padx=10, pady=(10, 0))
    combo_perfil = ttk.Combobox(aba_perfil, values=PERFIS, state="readonly")
    combo_perfil.pack(padx=10)
    situacao = ttk.Label(aba_perfil, text="Sessão: ninguém identificado.")
    situacao.pack(anchor="w", padx=10, pady=10)
    aviso_perfil = ttk.Label(aba_perfil, text="Use só nomes fictícios, sem senhas.")
    aviso_perfil.pack(anchor="w", padx=10)


    def mostrar_sessao():
        if sessao.nome is None:
            situacao.configure(text="Sessão: ninguém identificado.")
        else:
            situacao.configure(text="Sessão: " + sessao.nome + " (" + sessao.perfil + ")")
        if sessao.pode_configurar():
            abas.tab(aba_json, state="normal")
        else:
            abas.tab(aba_json, state="disabled")


    def entrar():
        try:
            sessao.entrar(entrada_nome.get(), combo_perfil.get())
        except ValueError as erro:
            aviso_perfil.configure(text=str(erro))
            return
        mostrar_sessao()
        aviso_perfil.configure(text="Perfil escolhido na simulação.")


    def sair():
        sessao.sair()  
        entrada_nome.delete(0, tk.END)
        combo_perfil.set("")
        mostrar_sessao()
        abas.select(aba_perfil)
        aviso_perfil.configure(text="Sessão encerrada. Vendas e relatórios não foram apagados.")


    botoes_perfil = ttk.Frame(aba_perfil)
    botoes_perfil.pack(pady=10)
    ttk.Button(botoes_perfil, text="Entrar", command=entrar).pack(side="left", padx=4)
    ttk.Button(botoes_perfil, text="Sair", command=sair).pack(side="left", padx=4)

    def ir_para_json():
        if sessao.pode_configurar():
            abas.select(aba_json)
        else:
            abas.select(aba_perfil)
            aviso_perfil.configure(text="Entre como Administração para abrir o Exercício JSON.")


    menu = tk.Menu(janela)
    menu_ir = tk.Menu(menu, tearoff=0)
    menu_ir.add_command(label="Pedido", command=lambda: abas.select(aba_pedido))
    menu_ir.add_command(label="Produtos", command=lambda: abas.select(aba_produtos))
    menu_ir.add_command(label="Perfil (simulação)", command=lambda: abas.select(aba_perfil))
    menu_ir.add_command(label="Exercício JSON", command=ir_para_json)
    menu.add_cascade(label="Ir para", menu=menu_ir)
    janela.config(menu=menu)
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
