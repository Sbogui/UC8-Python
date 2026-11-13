# A16: assinaturas de apoio; traga sua implementação anterior.
from pagamento import preco_para_centavos

TIPOS = ["produto", "cliente"]


class CadastroController:

    def __init__(self, repositorio):
        self.repositorio = repositorio

    def conferir_tipo(self, tipo):
        if tipo not in TIPOS:
            raise ValueError("Tipo de cadastro desconhecido: " + str(tipo))

    def listar(self, tipo):
        self.conferir_tipo(tipo)
        if tipo == "produto":
            return self.repositorio.listar_produtos()
        return self.repositorio.listar_clientes()

    def salvar(self, tipo, nome, preco_texto="", codigo=None):
        self.conferir_tipo(tipo)
        if tipo == "produto":
            preco = preco_para_centavos(preco_texto)
            if codigo is None:
                return self.repositorio.adicionar_produto(nome, preco)
            self.repositorio.editar_produto(codigo, nome, preco)
            return codigo
        if codigo is None:
            return self.repositorio.adicionar_cliente(nome)
        self.repositorio.editar_cliente(codigo, nome)
        return codigo

    def excluir(self, tipo, codigo, confirmado):
        self.conferir_tipo(tipo)
        if tipo == "produto":
            self.repositorio.excluir_produto(codigo, confirmado)
        else:
            self.repositorio.excluir_cliente(codigo, confirmado)
        return codigo
