import tkinter as tk
from tkinter import ttk
from pathlib import Path
from aluno import Aluno


def inserir_marca(container, caminho=None):
    if caminho is None:
        caminho = Path(__file__).resolve().parent / "marca-a06.png"
    rotulo = ttk.Label(container, text="Sistema escolar fictício — A06")
    try:
        caminho = Path(caminho)
        if caminho.is_file():
            imagem = tk.PhotoImage(master=container, file=str(caminho))
            rotulo.configure(image=imagem, compound="top")
            rotulo.image = imagem 
    except (OSError, tk.TclError):
        pass  
    return rotulo


def abrir_consulta(principal, aluno):
    if aluno.calcular_media() is None:
        return None

    texto = aluno.resumo()

    consulta = tk.Toplevel(principal)
    consulta.title("Consulta")
    consulta.columnconfigure(0, weight=1)
    quadro = ttk.LabelFrame(consulta, text="Registro confirmado na abertura", padding=8)
    quadro.grid(row=0, column=0, padx=12, pady=8, sticky="ew")
    quadro.columnconfigure(0, weight=1)
    ttk.Label(quadro, text=texto, wraplength=340).grid(row=0, column=0, padx=6, pady=4, sticky="w")
    ttk.Label(
        consulta,
        text="Esta consulta é um retrato: não muda se a principal for editada ou confirmar outro registro.",
        wraplength=360,
    ).grid(row=1, column=0, padx=12, pady=4, sticky="w")

    def fechar(event=None):
        consulta.destroy()
        principal.focus_set()

    ttk.Button(consulta, text="Fechar consulta", command=fechar).grid(row=2, column=0, pady=8)
    consulta.protocol("WM_DELETE_WINDOW", fechar)
    consulta.bind("<Escape>", fechar)
    consulta.focus_set()
    return consulta


def criar_janela():
    janela = tk.Tk()
    janela.title("Escolar com consulta — A06")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    aluno = Aluno()  
    consultas = {"abertas": 0}  
    inserir_marca(base).grid(row=0, column=0, pady=6, sticky="w")
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

    ttk.Label(identificacao, text="Nome fictício:").grid(row=0, column=0, padx=6, pady=4, sticky="w")
    entrada_nome = ttk.Entry(identificacao)
    entrada_nome.grid(row=0, column=1, padx=6, pady=4, sticky="ew")
    ttk.Label(identificacao, text="Turma fictícia:").grid(row=1, column=0, padx=6, pady=4, sticky="w")
    entrada_turma = ttk.Entry(identificacao)
    entrada_turma.grid(row=1, column=1, padx=6, pady=4, sticky="ew")
    entradas_notas = []
    for numero in range(1, 6):
        ttk.Label(grupo_notas, text=f"Nota {numero} (0 a 10):").grid(row=numero-1, column=0, padx=6, pady=4, sticky="w")
        entrada = ttk.Entry(grupo_notas)
        entrada.grid(row=numero-1, column=1, padx=6, pady=4, sticky="ew")
        entradas_notas.append(entrada)

    def ao_calcular():
        textos = []
        for entrada in entradas_notas:
            textos.append(entrada.get())
        aviso.configure(text=aluno.atualizar(entrada_nome.get(), entrada_turma.get(), textos))
        resultado.configure(text=aluno.resumo())

    def ao_exibir():
        consulta = abrir_consulta(janela, aluno)
        if consulta is None:
            aviso.configure(text="Calcule uma média válida antes de consultar.")
            return
        consultas["abertas"] = consultas["abertas"] + 1
        consulta.title(f"Consulta C{consultas['abertas']}")
        aviso.configure(text=f"Consulta C{consultas['abertas']} aberta com o último registro confirmado.")

    def ao_limpar():
        entrada_nome.delete(0, tk.END)
        entrada_turma.delete(0, tk.END)
        for entrada in entradas_notas:
            entrada.delete(0, tk.END)
        entrada_nome.focus_set()
        aviso.configure(text="Campos limpos. O último registro confirmado foi mantido.")

    ttk.Button(acoes, text="Calcular média", command=ao_calcular).grid(row=0, column=0, padx=4, pady=6)
    ttk.Button(acoes, text="Consultar", command=ao_exibir).grid(row=0, column=1, padx=4, pady=6)
    ttk.Button(acoes, text="Limpar campos", command=ao_limpar).grid(row=1, column=0, columnspan=2, padx=4, pady=6)
    aviso = ttk.Label(base, text="Use dados fictícios e confira as cinco notas.", wraplength=430)
    aviso.grid(row=4, column=0, pady=6, sticky="w")
    resultado = ttk.Label(base, text="Nenhum registro escolar confirmado nesta sessão.", wraplength=430)
    resultado.grid(row=5, column=0, pady=6, sticky="w")
    entrada_nome.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
