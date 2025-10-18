from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QApplication, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont, QIcon

class VentanaProfesional(QMainWindow):
    
    # Ancho del menú cuando está cerrado y abierto
    MENU_WIDTH_CLOSED = 70
    MENU_WIDTH_OPEN = 450
    COLOR_ABIERTO = "#2B2A2A"
    COLOR_CERRADO = "transparent"

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setWindowTitle("Profesional INPERIA")           
        self.init_ui()
        self.menu_abierto = False

    def setup_window(self):      
        self.setWindowIcon(QIcon("assets/icono_pest.ico"))
        self.setMinimumSize(1200,700)
        self.showMaximized()        

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal (Menú Lateral + Contenido Principal)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0) # Quitar márgenes

        # --- 1. Panel del Menú Lateral (Menú Hamburguesa) ---
        self.menu_frame = QWidget()
        self.menu_frame.setFixedWidth(self.MENU_WIDTH_CLOSED)
        self.menu_frame.setStyleSheet("background-color: {color_menu}};")
        
        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setAlignment(Qt.AlignTop)
        menu_layout.setSpacing(10)
        
        # Botón Hamburguesa
        self.boton_hamburguesa = QPushButton("☰")
        self.boton_hamburguesa.setFixedSize(self.MENU_WIDTH_CLOSED - 10, self.MENU_WIDTH_CLOSED - 10)
        self.boton_hamburguesa.setFont(QFont("Arial", 20, QFont.Bold))
        self.boton_hamburguesa.setStyleSheet("""
            QPushButton { 
                background-color: #444444; 
                color: white; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #555555; }
        """)
        self.boton_hamburguesa.clicked.connect(self.movimiento_menu)
        
        menu_layout.addWidget(self.boton_hamburguesa, alignment=Qt.AlignCenter)
        menu_layout.addSpacing(20)
        
        # Elementos del Menú
        for text in ["Inicio", "Perfil", "Configuración", "Salir"]:
            btn = QPushButton(text)
            btn.setStyleSheet("color: white; border: none; padding: 10px; text-align: left;")
            btn.setFont(QFont("Arial", 12))
            menu_layout.addWidget(btn)
        
        menu_layout.addStretch() # Empuja los elementos a la parte superior

        # --- 2. Contenido Principal ---
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F0F0F0;")
        content_layout = QVBoxLayout(content_widget)

        texto_bienvenida = QLabel("Bienbenido, Nom Ape")
        texto_bienvenida.setFont(QFont("Arial", 18))
        content_layout.addWidget(texto_bienvenida, alignment=Qt.AlignCenter)        
        
        texto_entrevistas = QLabel("Se han completado X entrevistas")
        texto_entrevistas.setFont(QFont("Arial", 22))
        content_layout.addWidget(texto_entrevistas, alignment=Qt.AlignCenter)

        content_layout.addStretch()


        # Añadir widgets al layout principal
        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(content_widget)

    def movimiento_menu(self):   

        # ancho de inicio y fin de la animación
        start_width = self.MENU_WIDTH_OPEN if self.menu_abierto else self.MENU_WIDTH_CLOSED
        end_width = self.MENU_WIDTH_CLOSED if self.menu_abierto else self.MENU_WIDTH_OPEN
       
        start_width = self.MENU_WIDTH_OPEN if self.menu_abierto else self.MENU_WIDTH_CLOSED

        
        self.animation = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(start_width)
        self.animation.setEndValue(end_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad) # Suaviza la animación
        
        # Inicia la animación y actualiza el estado
        self.animation.start()
        self.menu_abierto = not self.menu_abierto
        
        
    