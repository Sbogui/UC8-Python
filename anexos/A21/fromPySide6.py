from PySide6.QtWidgets import QApplication, QLabel

app = QApplication([])

label = QLabel("Hello, World!")
label.setWindowTitle("My First PySide6 App")
label.resize(400, 200)
label.show()

app.exec()