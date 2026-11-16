# A17: assinaturas de apoio; traga sua implementação anterior.

def criar_comparacao():
    try:
        import customtkinter as ctk
    except ImportError:
        print("CustomTkinter não está instalado: comparação não executada.")
        return None

    janela = ctk.CTk()
    janela.title("A17 — comparação (opcional)")
    ctk.CTkLabel(janela, text="Nome do cliente (fictício):").pack(padx=10, pady=(10, 0))
    entrada = ctk.CTkEntry(janela)
    entrada.pack(padx=10)
    aviso = ctk.CTkLabel(janela, text="Observe o foco, o Tab e as mensagens.")
    aviso.pack(padx=10, pady=10)

    def salvar():
        if entrada.get().strip() == "":
            aviso.configure(text="Informe um nome.")
        else:
            aviso.configure(text="Nome recebido: " + entrada.get().strip())

    ctk.CTkButton(janela, text="Salvar", command=salvar).pack(pady=10)
    return janela


if __name__ == "__main__":
    janela = criar_comparacao()
    if janela is not None:
        janela.mainloop()