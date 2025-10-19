from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QHBoxLayout, QSizePolicy
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer

class VentanaUsuario(QMainWindow):
    
    # Constantes para el menú
    MENU_WIDTH_CLOSED = 70
    MENU_WIDTH_OPEN = 250
    COLOR_ABIERTO = "#2B2A2A"
    COLOR_CERRADO = "transparent"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("INPERIA - Usuario")
        self.setWindowIcon(QIcon("assets/icono_pest.ico"))
        self.setMinimumSize(1200,700)
        self.showMaximized()
        
        self.menu_abierto = False
        self.submenu_abierto = False # Estado del submenú de preguntas
        
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal (Menú Lateral + Contenido Principal)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- 1. Panel del Menú Lateral ---
        self.menu_frame = QWidget()
        self.menu_frame.setFixedWidth(self.MENU_WIDTH_CLOSED)
        self.menu_frame.setStyleSheet(f"background-color: {self.COLOR_CERRADO};") 
        
        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setContentsMargins(5, 5, 5, 5)
        menu_layout.setSpacing(10)
        
        # Contenedor para el botón hamburguesa
        self.header_menu_widget = QWidget()
        self.header_menu_layout = QHBoxLayout(self.header_menu_widget)
        self.header_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.header_menu_layout.setSpacing(0)
        
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
        
        self.header_menu_layout.addStretch() 
        self.header_menu_layout.addWidget(self.boton_hamburguesa)
        
        menu_layout.addWidget(self.header_menu_widget)
        menu_layout.addSpacing(10)

        # --- Estilos de Botones ---
        
        # Estilo base para botones del menú principal (similar a la imagen)
        self.button_style = """
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
        # Estilo para el botón de preguntas cuando está activo
        self.active_button_style = """
            QPushButton { 
                color: white; 
                border: 1px solid rgba(255, 255, 255, 0.4); 
                padding: 10px 15px; 
                text-align: left;
                background-color: rgba(85, 85, 85, 0.5); 
                border-radius: 15px;
            }
            QPushButton:hover { 
                background-color: rgba(85, 85, 85, 0.7); 
            }
        """

        # --- Botones del Menú Principal ---
        
        # Botón "Preguntas"
        self.btn_preguntas = QPushButton("Preguntas")
        self.btn_preguntas.setStyleSheet(self.button_style)
        self.btn_preguntas.setFont(QFont("Arial", 10))
        self.btn_preguntas.hide()
        self.btn_preguntas.clicked.connect(self.toggle_submenu_preguntas)


        # Contenedor para el submenú de preguntas
        self.submenu_preguntas_widget = QWidget()
        self.submenu_preguntas_layout = QVBoxLayout(self.submenu_preguntas_widget)
        self.submenu_preguntas_layout.setContentsMargins(10, 0, 0, 0) # Sangría
        self.submenu_preguntas_layout.setSpacing(5)

        # 5 Preguntas del submenú
        self.sub_buttons = []
        for i in range(1, 6): # De 1 a 5
            sub_btn = QPushButton(f"Pregunta {i}")
            sub_btn.setStyleSheet("""
                QPushButton { 
                    color: white; 
                    border: none; 
                    padding: 5px 10px; 
                    text-align: left;
                    background-color: rgba(0, 0, 0, 0.1); 
                    border-radius: 8px;
                }
                QPushButton:hover { background-color: rgba(85, 85, 85, 0.3); }
            """)
            sub_btn.setFont(QFont("Arial", 9))
            self.sub_buttons.append(sub_btn)
            self.submenu_preguntas_layout.addWidget(sub_btn)
            
        self.submenu_preguntas_widget.hide() # Ocultar el submenú contenedor

        # Otros botones del menú principal
        self.btn_perfil = QPushButton("Mi Perfil")
        self.btn_perfil.setStyleSheet(self.button_style)
        self.btn_perfil.setFont(QFont("Arial", 10))
        self.btn_perfil.hide()
        
        self.btn_cerrar = QPushButton("Cerrar Sesión")
        self.btn_cerrar.setStyleSheet(self.button_style)
        self.btn_cerrar.setFont(QFont("Arial", 10))
        self.btn_cerrar.hide()
        
        # Lista de todos los elementos del menú principal (para mostrar/ocultar)
        self.main_menu_widgets = [self.btn_preguntas, self.submenu_preguntas_widget, self.btn_perfil, self.btn_cerrar]
        
        menu_layout.addWidget(self.btn_preguntas)
        menu_layout.addWidget(self.submenu_preguntas_widget) 
        menu_layout.addWidget(self.btn_perfil)
        menu_layout.addWidget(self.btn_cerrar)
        
        # Separador para empujar los botones hacia arriba
        menu_layout.addStretch(1) 

        # --- Botón de Ajustes (Abajo a la derecha) ---
        
        self.footer_menu_widget = QWidget()
        self.footer_menu_layout = QHBoxLayout(self.footer_menu_widget)
        self.footer_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_menu_layout.setAlignment(Qt.AlignRight)
        self.footer_menu_widget.hide() 

        self.ajustes_button = QPushButton("⚙️") 
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


        # --- 2. Contenido Principal (Centrado Verticalmente) ---
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Centrado vertical
        content_layout.addStretch(1) 
        
        titulo = QLabel("Bienvenido al módulo usuario")
        titulo.setFont(QFont("Arial", 18))
        titulo.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(titulo)

        contenido = QLabel("Prepare aquí su contenido para el usuario.")
        contenido.setFont(QFont("Arial", 22))
        contenido.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(contenido)
        
        content_layout.addStretch(1)

        # Añadir widgets al layout principal
        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(content_widget)

    def movimiento_menu(self):   
        """Maneja la animación de apertura y cierre del menú principal."""
        
        if self.menu_abierto:
            # Estado A CERRAR (Actual: Abierto)
            end_width = self.MENU_WIDTH_CLOSED
            target_color = self.COLOR_CERRADO
            
            # Ocultar todos los botones de menú y el footer
            for widget in self.main_menu_widgets:
                widget.hide()
            self.footer_menu_widget.hide() 
            
            # Asegurarse de que el submenú esté cerrado y restablecer estilo del botón
            self.submenu_preguntas_widget.hide()
            self.submenu_abierto = False
            self.btn_preguntas.setStyleSheet(self.button_style) 

            # Ajuste de alineación del botón hamburguesa: Insertar stretch a la izquierda
            if self.header_menu_layout.itemAt(0) is None or self.header_menu_layout.itemAt(0).widget() is not None:
                self.header_menu_layout.insertStretch(0, 1)
            
        else:
            # Estado A ABRIR (Actual: Cerrado)
            end_width = self.MENU_WIDTH_OPEN
            target_color = self.COLOR_ABIERTO
            
            # Mostrar botones principales y el footer
            for widget in self.main_menu_widgets:
                # Ocultar el widget del submenú, solo se muestra al hacer clic en "Preguntas"
                if widget != self.submenu_preguntas_widget:
                    widget.show()
                else:
                    widget.hide()
                    
            self.footer_menu_widget.show()

            # Quitar el stretch para que el botón hamburguesa se quede a la derecha
            if self.header_menu_layout.itemAt(0) and self.header_menu_layout.itemAt(0).spacerItem():
                self.header_menu_layout.removeItem(self.header_menu_layout.itemAt(0))

        # Invertir el estado para el próximo clic
        self.menu_abierto = not self.menu_abierto
        
        # Aplicar el cambio de color (debe ser instantáneo)
        self.menu_frame.setStyleSheet(f"background-color: {target_color};")

        # Animación del ancho MÍNIMO y MÁXIMO
        self.animation_min = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        self.animation_min.setDuration(300)
        self.animation_min.setStartValue(self.menu_frame.width())
        self.animation_min.setEndValue(end_width)
        self.animation_min.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation_min.start()
        
        self.animation_max = QPropertyAnimation(self.menu_frame, b"maximumWidth")
        self.animation_max.setDuration(300)
        self.animation_max.setStartValue(self.menu_frame.width())
        self.animation_max.setEndValue(end_width)
        self.animation_max.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation_max.start()

    def toggle_submenu_preguntas(self):
        """Muestra u oculta el submenú de preguntas (Pregunta 1 a 5)."""

        if self.submenu_abierto:
            self.submenu_preguntas_widget.hide()
            self.submenu_abierto = False
            self.btn_preguntas.setStyleSheet(self.button_style) # Desactivar estilo
        else:
            self.submenu_preguntas_widget.show()
            self.submenu_abierto = True
            self.btn_preguntas.setStyleSheet(self.active_button_style) # Activar estilo