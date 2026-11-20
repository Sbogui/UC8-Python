from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

app = QApplication([])
janela = QWidget()
janela.setWindowTitle("Ensaio de sinais")
layout = QVBoxLayout(janela)
mensagem = QLabel("Aguardando o clique")
botao = QPushButton("Testar sinal")
layout.addWidget(mensagem)
layout.addWidget(botao)
# Passe a função ao connect para o Qt chamá-la no clique.
botao.clicked.connect(lambda: mensagem.setText("Clique recebido"))
janela.show()
app.exec()
