# A18: assinaturas de apoio; traga sua implementação anterior.
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


class VendaController:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def confirmar(self, pedido, cliente_id, forma, versao_previa):
        if pedido.estado != "montagem":
            raise ValueError("Pedido finalizado: inicie um novo pedido.")
        if cliente_id is None:
            raise ValueError("Selecione um cliente antes de confirmar.")
        if len(pedido.itens) == 0:
            raise ValueError("Adicione ao menos um item antes de finalizar.")
        if versao_previa != pedido.versao:
            raise ValueError("A prévia ficou antiga: abra a confirmação de novo.")
        itens = []
        for codigo, item in pedido.itens.items():
            itens.append((int(codigo), item.produto.nome, item.produto.preco_centavos, item.quantidade))
        venda_id = self.repositorio.registrar_venda(cliente_id, itens, forma)
        comprovante = pedido.finalizar(forma, True, versao_previa)
        return venda_id, comprovante
