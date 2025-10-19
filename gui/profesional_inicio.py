from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QApplication, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont, QIcon

class VentanaProfesional(QMainWindow):
    
    # Ancho del menú cuando está cerrado y abierto
    MENU_WIDTH_CLOSED = 80
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
        self.menu_frame.setStyleSheet("background-color: transparent};")
        
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
        
        menu_layout.addWidget(self.boton_hamburguesa)
        menu_layout.addSpacing(20)
        
        # --- Elementos del Menú (Recreando la imagen) ---
        menu_options = [
            "Estadísticas de entrevistas",
            "Historial de entrevistas",
            "Datos de internos",
            "Modificar preguntas",
            "Ajustes del modelo",
            "Casos críticos"
        ]
        
        # Lista de botones que no son el de Ajustes/Configuración del fondo
        self.menu_buttons = []
        
        # Estilo base para los nuevos botones (simulando el efecto de la imagen)
        button_style = """
            QPushButton { 
                color: white; 
                border: 1px solid rgba(255, 255, 255, 0.4); 
                padding: 10px 15px; 
                text-align: left;
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 15px;
            }
            QPushButton:hover { 
                background-color: rgba(85, 85, 85, 0.5); 
            }
        """

        # Crear y añadir los 6 botones principales
        for text in menu_options:
            btn = QPushButton(text)
            btn.setStyleSheet(button_style)
            btn.setFont(QFont("Arial", 10))
            btn.hide() # Ocultar por defecto
            self.menu_buttons.append(btn)
            menu_layout.addWidget(btn)   
        
        menu_layout.addStretch(1) # Empuja los elementos a la parte superior

# --- Botón de Ajustes (Abajo a la derecha) ---
        
        # Contenedor para el botón de ajustes para control de alineación
        self.footer_menu_widget = QWidget()
        self.footer_menu_layout = QHBoxLayout(self.footer_menu_widget)
        self.footer_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_menu_layout.setAlignment(Qt.AlignRight) # Alineación a la derecha
        self.footer_menu_widget.hide() # Ocultar el widget contenedor por defecto

        self.ajustes_button = QPushButton()
        self.ajustes_button.setIcon(QIcon("assets/ajustes_icon.png"))
        #self.ajustes_button.setIconSize(QSize(20, 20))
        self.ajustes_button.setFixedSize(self.MENU_WIDTH_CLOSED - 10, self.MENU_WIDTH_CLOSED - 10) 
        self.ajustes_button.setFont(QFont("Arial", 20))
        self.ajustes_button.setStyleSheet("""
            QPushButton { 
                background-color: transparent; 
                color: white; 
                border: none;
            }
            QPushButton:hover { color: lightgray; }
        """)
        
        self.footer_menu_layout.addWidget(self.ajustes_button)
        menu_layout.addWidget(self.footer_menu_widget)        

        # --- 2. Contenido Principal ---
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F0F0F0;")
        content_layout = QVBoxLayout(content_widget)

        content_layout.addStretch(1)

        texto_bienvenida = QLabel("Bienvenido, Nom Ape")
        texto_bienvenida.setFont(QFont("Arial", 18))
        content_layout.addWidget(texto_bienvenida, alignment=Qt.AlignCenter)        
        
        texto_entrevistas = QLabel("Se han completado X entrevistas")
        texto_entrevistas.setFont(QFont("Arial", 22))
        content_layout.addWidget(texto_entrevistas, alignment=Qt.AlignCenter)

        content_layout.addStretch(1)


        # Añadir widgets al layout principal
        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(content_widget)

    def movimiento_menu(self):   

        # ancho de inicio y fin de la animación
        start_width = self.MENU_WIDTH_OPEN if self.menu_abierto else self.MENU_WIDTH_CLOSED
        end_width = self.MENU_WIDTH_CLOSED if self.menu_abierto else self.MENU_WIDTH_OPEN
       
        self.menu_abierto = not self.menu_abierto

        color_menu = self.COLOR_ABIERTO if self.menu_abierto else self.COLOR_CERRADO

        if self.menu_abierto:
            # Mostrar botones con retardo para efecto escalonado
            for i, btn in enumerate(self.menu_buttons):
                QTimer.singleShot(i * 100, btn.show)  # Muestra cada botón con un retardo
            self.footer_menu_widget.show()              
        else:
            # Ocultar botones inmediatamente
            for btn in self.menu_buttons:
                btn.hide()        

            self.footer_menu_widget.hide()


        self.menu_frame.setStyleSheet(f"background-color: {color_menu};")
        self.animation = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(start_width)
        self.animation.setEndValue(end_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad) # Suaviza la animación
        
        # Inicia la animación y actualiza el estado
        self.animation.start()        
        
        
    