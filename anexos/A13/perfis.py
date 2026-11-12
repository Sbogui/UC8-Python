# A13: assinaturas de apoio; traga sua implementação anterior.

"""Simulação local de identificação/perfil; não autentica usuários reais."""
"""TODO A13: implemente __init__ conforme o contrato e reutilize seu código anterior."""
"""TODO A13: implemente entrar conforme o contrato e reutilize seu código anterior."""
"""TODO A13: implemente pode_configurar conforme o contrato e reutilize seu código anterior."""
"""TODO A13: implemente sair conforme o contrato e reutilize seu código anterior."""
PERFIS = ["Caixa", "Administração"]

class SessaoDemo:
    

    def __init__(self):
        self.nome = None
        self.perfil = None        

    def entrar(self, nome, perfil):
        if nome.strip() = "":
            raise ValueError("Informe um nome fictício.")
        if perfil not in PERFIS:
            raise ValueError("Escolha o pergil Caixa ou Administração.")
        self.nome = nome.strip()
        self.perfil = perfil

    def pode_configurar(self):
        return self.perfil == "Administração"


    def sair(self):
        self.nome = None
        self.perfil = None
