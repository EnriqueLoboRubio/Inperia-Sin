from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

class VentanaUsuario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("INPERIA - Profesional")
        self.setWindowIcon(QIcon("assets/icono_pest.ico"))
        self.showMaximized()
        self.initUI()

    def initUI(self):
        central = QWidget() 
        self.setCentralWidget(central)        
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        # Título
        titulo = QLabel("Bienvenido al módulo usuario")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Contenido adicional
        contenido = QLabel("Prepare aquí su contenido para el usuario.")
        contenido.setAlignment(Qt.AlignCenter)
        layout.addWidget(contenido)       