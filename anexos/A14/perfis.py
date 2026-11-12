# A14: assinaturas de apoio; traga sua implementação anterior.
PERFIS = ["Caixa", "Administração"]


class SessaoDemo:
    """Simulação local de identificação/perfil; não autentica usuários reais."""

    def __init__(self):
        self.nome = None
        self.perfil = None

    def entrar(self, nome, perfil):
        if nome.strip() == "":
            raise ValueError("Informe um nome fictício.")
        if perfil not in PERFIS:
            raise ValueError("Escolha o perfil Caixa ou Administração.")
        self.nome = nome.strip()
        self.perfil = perfil

    def pode_configurar(self):
        return self.perfil == "Administração"

    def sair(self):
        self.nome = None
        self.perfil = None