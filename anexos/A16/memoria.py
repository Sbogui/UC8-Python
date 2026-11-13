# A16: assinaturas de apoio; traga sua implementação anterior.
from copy import deepcopy
from repositorio import validar_nome, validar_preco, validar_id

class RepositorioMemoria:

    def __init__(self):
        self.produtos = []        
        self.clientes = []        
        self.proximo_produto = 1  
        self.proximo_cliente = 1

    def adicionar_produto(self, nome, preco):
        nome = validar_nome(nome)
        preco = validar_preco(preco)
        codigo = self.proximo_produto
        self.produtos.append((codigo, nome, preco))
        self.proximo_produto += 1
        return validar_id(codigo)

    def listar_produtos(self):
        return deepcopy(self.produtos)  

    def editar_produto(self, codigo, nome, preco):
        codigo = validar_id(codigo)
        nome = validar_nome(nome)
        preco = validar_preco(preco)
        for posicao in range(len(self.produtos)):
            if self.produtos[posicao][0] == codigo:
                self.produtos[posicao] = (codigo, nome, preco)
                return
        raise ValueError("Produto não encontrado: o ID " + str(codigo) + " não existe.")

    def excluir_produto(self, codigo, confirmado=False):
        codigo = validar_id(codigo)
        if not confirmado:
            raise ValueError("Confirme a exclusão para apagar o produto.")
        for posicao in range(len(self.produtos)):
            if self.produtos[posicao][0] == codigo:
                del self.produtos[posicao]
                return
        raise ValueError("Produto não encontrado: o ID " + str(codigo) + " não existe.")

    def adicionar_cliente(self, nome):
        nome = validar_nome(nome)
        codigo = self.proximo_cliente
        self.clientes.append((codigo, nome))
        self.proximo_cliente += 1
        return validar_id(codigo)

    def listar_clientes(self):
        return deepcopy(self.clientes)

    def editar_cliente(self, codigo, nome):
        codigo = validar_id(codigo)
        nome = validar_nome(nome)
        for posicao in range(len(self.clientes)):
            if self.clientes[posicao][0] == codigo:
                self.clientes[posicao] = (codigo, nome)
                return
        raise ValueError("Cliente não encontrado: o ID " + str(codigo) + " não existe.")

    def excluir_cliente(self, codigo, confirmado=False):
        codigo = validar_id(codigo)
        if not confirmado:
            raise ValueError("Confirme a exclusão para apagar o cliente.")
        for posicao in range(len(self.clientes)):
            if self.clientes[posicao][0] == codigo:
                del self.clientes[posicao]
                return
        raise ValueError("Cliente não encontrado: o ID " + str(codigo) + " não existe.")