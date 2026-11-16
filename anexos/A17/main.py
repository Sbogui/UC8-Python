# A17: integre sua versão anterior; preserve-a em outra pasta.
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from modelos import Produto, Pedido, formatar
from pagamento import FATORES, calcular_pagamento
from arquivos import validar_catalogo, ler_catalogo, salvar_catalogo
from relatorios import exportar_csv
from perfis import SessaoDemo, PERFIS
from repositorio import RepositorioSqlite
from controller import CadastroController, VendaController

CAMINHO_BANCO = Path(__file__).with_name("sorveteria_a17.db")


def criar_cadastro(pai, tipo, controller, descricao):
    com_preco = (tipo == "produto")
    rotulo = tipo.capitalize()
    na_tela = {}             
    editando = {"id": None}   

    ttk.Label(pai, text=descricao, wraplength=420).pack(anchor="w", padx=10, pady=(10, 0))
    modo = ttk.Label(pai, text="Modo: novo " + tipo)
    modo.pack(anchor="w", padx=10, pady=(5, 0))
    ttk.Label(pai, text="Nome do " + tipo + ":").pack(anchor="w", padx=10, pady=(10, 0))
    entrada_nome = ttk.Entry(pai, width=40)
    entrada_nome.pack(padx=10)
    entrada_preco = None
    if com_preco:
        ttk.Label(pai, text="Preço (ex.: 7,50):").pack(anchor="w", padx=10, pady=(10, 0))
        entrada_preco = ttk.Entry(pai, width=20)
        entrada_preco.pack(padx=10)

    if com_preco:
        tabela = ttk.Treeview(pai, columns=("id", "nome", "preco"), show="headings", height=8)
        tabela.heading("preco", text="Preço")
        tabela.column("preco", width=100)
    else:
        tabela = ttk.Treeview(pai, columns=("id", "nome"), show="headings", height=8)
    tabela.heading("id", text="ID")
    tabela.heading("nome", text=rotulo)
    tabela.column("id", width=50)
    tabela.column("nome", width=220)
    tabela.pack(padx=10, pady=10, fill="both", expand=True)

    aviso = ttk.Label(pai, text="Use dados fictícios.", wraplength=420)
    aviso.pack(anchor="w", padx=10, pady=5)

    def limpar_campos():
        entrada_nome.delete(0, tk.END)
        if com_preco:
            entrada_preco.delete(0, tk.END)

    def iniciar_novo():
        editando["id"] = None
        tabela.selection_remove(*tabela.selection())
        limpar_campos()
        modo.configure(text="Modo: novo " + tipo)
        entrada_nome.focus_set()

    def mostrar():
        linhas = controller.listar(tipo)
        na_tela.clear()
        tabela.delete(*tabela.get_children())
        for linha in linhas:
            if com_preco:
                codigo, nome, preco = linha
                na_tela[codigo] = (nome, preco)
                tabela.insert("", tk.END, iid=str(codigo), values=(codigo, nome, formatar(preco)))
            else:
                codigo, nome = linha
                na_tela[codigo] = (nome, None)
                tabela.insert("", tk.END, iid=str(codigo), values=(codigo, nome))
        if editando["id"] is not None:
            if editando["id"] in na_tela:
                tabela.selection_set(str(editando["id"]))
            else:
                iniciar_novo() 

    def ao_selecionar(evento):
        selecionada = tabela.selection()
        if not selecionada:
            return
        codigo = int(selecionada[0])
        if codigo not in na_tela:
            return
        nome, preco = na_tela[codigo]
        editando["id"] = codigo
        limpar_campos()
        entrada_nome.insert(0, nome)
        if com_preco:
            entrada_preco.insert(0, f"{preco // 100},{preco % 100:02d}")
        modo.configure(text="Modo: editando o " + tipo + " ID " + str(codigo))

    def salvar():
        preco_texto = ""
        if com_preco:
            preco_texto = entrada_preco.get()
        try:
            codigo = controller.salvar(tipo, entrada_nome.get(), preco_texto, editando["id"])
        except ValueError as erro:
            aviso.configure(text=str(erro)) 
            return
        if editando["id"] is None:
            mensagem = rotulo + " salvo com ID " + str(codigo) + "."
        else:
            mensagem = rotulo + " ID " + str(codigo) + " atualizado."
        try:
            mostrar()
        except ValueError as erro:
            aviso.configure(text="Salvo (ID " + str(codigo) + "), mas a lista não atualizou: " + str(erro))
            return
        aviso.configure(text=mensagem)
        if editando["id"] is None:
            limpar_campos()
            entrada_nome.focus_set()

    def excluir():
        codigo = editando["id"]
        if codigo is None:
            aviso.configure(text="Selecione uma linha da tabela para excluir.")
            return  
        nome = na_tela[codigo][0]
        resposta = messagebox.askyesno("Excluir " + tipo, "Excluir o " + tipo + " ID " + str(codigo) + " (" + nome + ")?")
        if not resposta:
            aviso.configure(text="Exclusão cancelada. Nada foi apagado.")
            return
        try:
            controller.excluir(tipo, codigo, True)
        except ValueError as erro:
            aviso.configure(text=str(erro))
            return
        editando["id"] = None
        try:
            mostrar()
        except ValueError as erro:
            aviso.configure(text="Excluído, mas a lista não atualizou: " + str(erro))
            return
        iniciar_novo()
        aviso.configure(text=rotulo + " ID " + str(codigo) + " excluído.")

    tabela.bind("<<TreeviewSelect>>", ao_selecionar)
    botoes_cadastro = ttk.Frame(pai)
    botoes_cadastro.pack(pady=10)
    ttk.Button(botoes_cadastro, text="Salvar", command=salvar).pack(side="left", padx=4)
    ttk.Button(botoes_cadastro, text="Novo", command=iniciar_novo).pack(side="left", padx=4)
    ttk.Button(botoes_cadastro, text="Excluir", command=excluir).pack(side="left", padx=4)

    try:
        mostrar()
    except ValueError as erro:
        aviso.configure(text=str(erro))


def criar_janela():
    pedido = Pedido()
    sessao = SessaoDemo()
    repositorio = RepositorioSqlite(CAMINHO_BANCO)
    descricao_armazenamento = "Banco SQLite: " + str(CAMINHO_BANCO)
    controller = CadastroController(repositorio)
    venda_controller = VendaController(repositorio)
    previa = {"janela": None, "versao": 0, "forma": "", "cliente": None}

    janela = tk.Tk()
    janela.title("Sorveteria fictícia — A17")

    abas = ttk.Notebook(janela)
    abas.pack(fill="both", expand=True)
    aba_pedido = ttk.Frame(abas)
    aba_json = ttk.Frame(abas)
    aba_produtos = ttk.Frame(abas)
    aba_clientes = ttk.Frame(abas)
    aba_perfil = ttk.Frame(abas)
    abas.add(aba_pedido, text="Pedido")
    abas.add(aba_produtos, text="Produtos")
    abas.add(aba_clientes, text="Clientes")
    abas.add(aba_perfil, text="Perfil (simulação)")
    abas.add(aba_json, text="Exercício JSON", state="disabled")

    catalogo = []          
    clientes_na_tela = []   

    ttk.Label(aba_pedido, text="Cliente:").pack(anchor="w", padx=10, pady=(10, 0))
    combo_cliente = ttk.Combobox(aba_pedido, values=[], state="readonly", width=40)
    combo_cliente.pack(padx=10)
    ttk.Label(aba_pedido, text="Produto:").pack(anchor="w", padx=10, pady=(10, 0))
    combo = ttk.Combobox(aba_pedido, values=[], state="readonly", width=40)
    combo.pack(padx=10)
    ttk.Button(aba_pedido, text="Atualizar catálogo e clientes", command=lambda: atualizar_catalogo()).pack(pady=(5, 0))

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


    def atualizar_catalogo():
        try:
            produtos = repositorio.listar_produtos()
            clientes = repositorio.listar_clientes()
        except ValueError as erro:
            aviso.configure(text=str(erro))
            return
        anterior = None
        if combo_cliente.current() >= 0:
            anterior = clientes_na_tela[combo_cliente.current()][0]
        catalogo.clear()
        for codigo, nome, preco in produtos:
            catalogo.append(Produto(str(codigo), nome, preco)) 
        clientes_na_tela.clear()
        for codigo, nome in clientes:
            clientes_na_tela.append((codigo, nome))
        combo.configure(values=[f"{p.codigo} — {p.nome} ({formatar(p.preco_centavos)})" for p in catalogo])
        combo.set("")
        combo_cliente.configure(values=[f"{codigo} — {nome}" for codigo, nome in clientes_na_tela])
        combo_cliente.set("")
        for posicao in range(len(clientes_na_tela)):
            if clientes_na_tela[posicao][0] == anterior:
                combo_cliente.current(posicao) 
        aviso.configure(text="Catálogo e clientes atualizados.")


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
            produto = catalogo[indice]
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
            venda_id, comprovante = venda_controller.confirmar(
                pedido, previa["cliente"], previa["forma"], previa["versao"])
        except ValueError as erro:
            fechar_previa()
            aviso.configure(text=str(erro))  
            return
        fechar_previa()
        mostrar_pedido()
        resumo.configure(text=(
            f"Venda ID {venda_id} — Comprovante — {comprovante['forma']} | "
            f"Subtotal: {formatar(comprovante['subtotal_centavos'])} | "
            f"Desconto: {formatar(comprovante['desconto_centavos'])} | "
            f"Total: {formatar(comprovante['total_centavos'])}"))
        aviso.configure(text="Venda gravada no banco. Pedido finalizado (fictício).")


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

        indice_cliente = combo_cliente.current()
        if indice_cliente < 0:
            aviso.configure(text="Selecione um cliente antes de finalizar.")
            return

        previa["versao"] = pedido.versao
        previa["forma"] = forma.get()
        previa["cliente"] = clientes_na_tela[indice_cliente][0]

        nova = tk.Toplevel(janela)
        nova.title("Confirmar pedido")
        previa["janela"] = nova
        texto = (f"Cliente: {clientes_na_tela[indice_cliente][1]}\n"
                f"Forma: {forma.get()}\n"
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
        combo_cliente.set("")
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

    try:
        repositorio.iniciar_vendas()  
    except ValueError as erro:
        aviso.configure(text=str(erro))
    criar_cadastro(aba_produtos, "produto", controller, descricao_armazenamento)
    criar_cadastro(aba_clientes, "cliente", controller, descricao_armazenamento)
    atualizar_catalogo()

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
    menu_ir.add_command(label="Clientes", command=lambda: abas.select(aba_clientes))
    menu_ir.add_command(label="Perfil (simulação)", command=lambda: abas.select(aba_perfil))
    menu_ir.add_command(label="Exercício JSON", command=ir_para_json)
    menu.add_cascade(label="Ir para", menu=menu_ir)
    janela.config(menu=menu)
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
