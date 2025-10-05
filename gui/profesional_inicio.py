from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

class VentanaProfesional(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("INPERIA - Profesional")
        self.showMaximized()
        self.setWindowIcon(QIcon("assets/icono_pest.ico"))
        self.initUI()

    def initUI(self):
        central = QWidget() 
        self.setCentralWidget(central)        
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        # Título
        titulo = QLabel("Bienvenido al Módulo Profesional")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Contenido adicional para el profesional
        contenido = QLabel("Aquí puedes gestionar tus pacientes y consultas.")
        contenido.setAlignment(Qt.AlignCenter)
        layout.addWidget(contenido)
    