
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QApplication, QHeaderView, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from modelos import Pedido, Produto, formatar


def moeda(centavos):
    return f"R$ {formatar(centavos)}"


def pedido_de_ensaio():
    pedido = Pedido()
    pedido.adicionar(Produto("1", "Picolé de fruta", 500), "2")
    pedido.adicionar(Produto("2", "Picolé de leite", 750), "3")
    return pedido


class JanelaCarrinho(QWidget):
    def __init__(self, pedido):
        super().__init__()
        self.pedido = pedido
        self.setObjectName("carrinho")
        self.setWindowTitle("Carrinho de vendas")
        self.resize(740, 480)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        titulo = QLabel("Carrinho de vendas")
        titulo.setObjectName("titulo")
        apoio = QLabel("Selecione um produto para editar sua quantidade.")
        apoio.setObjectName("apoio")
        layout.addWidget(titulo)
        layout.addWidget(apoio)

        self.tabela = QTableWidget(0, 4)
        self.tabela.setAccessibleName("Itens do carrinho")
        self.tabela.setHorizontalHeaderLabels(
            ["Produto", "Qtd.", "Preço unitário", "Subtotal"]
        )
        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tabela.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tabela.verticalHeader().hide()

        cabecalho = self.tabela.horizontalHeader()
        cabecalho.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        cabecalho.setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.tabela, 1)

        painel = QWidget()
        painel.setObjectName("edicao")
        edicao = QVBoxLayout(painel)
        edicao.setContentsMargins(14, 12, 14, 12)

        linha = QHBoxLayout()
        rotulo = QLabel("&Nova quantidade")
        self.campo = QLineEdit()
        self.campo.setAccessibleName("Nova quantidade")
        self.campo.setMaxLength(12)
        rotulo.setBuddy(self.campo)

        self.botao = QPushButton("&Atualizar quantidade")

        linha.addWidget(rotulo)
        linha.addWidget(self.campo, 1)
        linha.addWidget(self.botao)

        edicao.addLayout(linha)

        self.retorno = QLabel("Selecione uma linha para começar.")
        self.retorno.setObjectName("retorno")
        self.retorno.setWordWrap(True)
        edicao.addWidget(self.retorno)

        layout.addWidget(painel)

        self.total = QLabel()
        self.total.setObjectName("total")
        self.total.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.total)

        self.setTabOrder(self.tabela, self.campo)
        self.setTabOrder(self.campo, self.botao)

        self.botao.clicked.connect(self.atualizar_quantidade)
        self.campo.returnPressed.connect(self.atualizar_quantidade)

        self.renderizar()

    def renderizar(self):
        linhas = self.pedido.linhas()

        self.tabela.setRowCount(len(linhas))

        for indice, linha in enumerate(linhas):
            codigo = linha[0]
            nome = linha[1]
            quantidade = linha[2]
            subtotal = linha[3]

            preco_unitario = subtotal // quantidade

            valores = (
                nome,
                str(quantidade),
                moeda(preco_unitario),
                moeda(subtotal),
            )

            for coluna, valor in enumerate(valores):
                celula = QTableWidgetItem(valor)

                if coluna == 0:
                    celula.setData(
                        Qt.ItemDataRole.UserRole, codigo
                    )
                else:
                    celula.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight
                        | Qt.AlignmentFlag.AlignVCenter
                    )

                self.tabela.setItem(indice, coluna, celula)

        self.total.setText(
            f"Total do carrinho · {moeda(self.pedido.total_centavos())}"
        )

    def mostrar_retorno(self, mensagem, erro=False):
        self.retorno.setProperty("erro", erro)
        self.retorno.setText(mensagem)

        estilo = self.retorno.style()
        estilo.unpolish(self.retorno)
        estilo.polish(self.retorno)

    def atualizar_quantidade(self):
        # Leia a seleção atual e recupere o ID guardado em UserRole.
        # Envie o texto do campo para a regra de edição em Pedido.
        # Mostre o retorno, atualize a tela se aceita e trate o foco.
        self.mostrar_retorno(
            "Evento recebido. Implemente a edição neste método."
        )


if __name__ == "__main__":
    app = QApplication([])

    tema = Path(__file__).with_name("carrinho.qss")
    app.setStyleSheet(tema.read_text(encoding="utf-8"))

    janela = JanelaCarrinho(pedido_de_ensaio())
    janela.show()

    app.exec()
