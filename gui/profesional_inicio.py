from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QApplication, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont, QIcon

class VentanaProfesional(QMainWindow):
    
    # Ancho del menú cuando está cerrado y abierto
    MENU_ANCHURA_CERRADO = 80
    MENU_ANCHURA_ABIERTO = 450
    COLOR_ABIERTO = "#2B2A2A"
    COLOR_CERRADO = "transparent"

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setWindowTitle("INPERIA - Profesional")           
        
        self.menu_abierto = False

        self.init_ui()

    def setup_window(self):      
        self.setWindowIcon(QIcon("assets/icono_pest.ico"))
        self.setMinimumSize(1200,700)
        self.showMaximized()        

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout principal horizontal (Menú Lateral + Contenido Principal)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0) # Quitar márgenes

        # --- 1. Panel del Menú Lateral---
        self.menu_frame = QWidget()
        self.menu_frame.setFixedWidth(self.MENU_ANCHURA_CERRADO)
        self.menu_frame.setStyleSheet(f"background-color: {self.COLOR_CERRADO};") 
        
        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setAlignment(Qt.AlignTop)
        menu_layout.setSpacing(10)

        # Contenedor para el botón hamburguesa
        self.cabecera_menu_widget = QWidget()
        self.cabecera_menu_layout = QHBoxLayout(self.cabecera_menu_widget)
        self.cabecera_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.cabecera_menu_layout.setSpacing(0)
        
        # Botón Hamburguesa
        self.boton_hamburguesa = QPushButton("☰")
        self.boton_hamburguesa.setFixedSize(self.MENU_ANCHURA_CERRADO - 10, self.MENU_ANCHURA_CERRADO - 10)
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

        self.cabecera_menu_layout.addWidget(self.boton_hamburguesa)
        self.cabecera_menu_layout.addSpacing(20)
        
        menu_layout.addWidget(self.boton_hamburguesa)
        menu_layout.addSpacing(20)

        # --- Estilos de Botones ---
        
        # Estilo base para botones del menú principal
        self.boton_estilo = """
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
        # --- Botones del Menú Principal ---

        # Botón Estadísticas
        self.boton_estadisticas = QPushButton("Estadísticas de entrevistas")
        self.boton_estadisticas.setStyleSheet(self.boton_estilo)
        self.boton_estadisticas.setFont(QFont("Arial", 10))
        self.boton_estadisticas.hide() # Ocultar por defecto

        # Botón Historial
        self.boton_historial = QPushButton("Historial de entrevistas")
        self.boton_historial.setStyleSheet(self.boton_estilo)
        self.boton_historial.setFont(QFont("Arial", 10))
        self.boton_historial.hide()

        # Botón Datos
        self.boton_datos = QPushButton("Datos de internos")
        self.boton_datos.setStyleSheet(self.boton_estilo)
        self.boton_datos.setFont(QFont("Arial", 10))
        self.boton_datos.hide()

        # Botón Modificar Preguntas
        self.boton_modificar = QPushButton("Modificar preguntas")
        self.boton_modificar.setStyleSheet(self.boton_estilo)
        self.boton_modificar.setFont(QFont("Arial", 10))
        self.boton_modificar.hide()

        # Botón Ajustes del Modelo
        self.boton_ajustes_modelo = QPushButton("Ajustes del modelo")
        self.boton_ajustes_modelo.setStyleSheet(self.boton_estilo)
        self.boton_ajustes_modelo.setFont(QFont("Arial", 10))
        self.boton_ajustes_modelo.hide()

        # Botón Casos Críticos
        self.boton_casos_criticos = QPushButton("Casos críticos")
        self.boton_casos_criticos.setStyleSheet(self.boton_estilo)
        self.boton_casos_criticos.setFont(QFont("Arial", 10))
        self.boton_casos_criticos.hide()   

       
        # Lista de todos los elementos del menú principal (para mostrar/ocultar)
        self.main_menu_widgets = [
            self.boton_estadisticas,
            self.boton_historial,
            self.boton_datos,
            self.boton_modificar,
            self.boton_ajustes_modelo,
            self.boton_casos_criticos
        ]

        # Añadir botones al layout del menú
        for boton in self.main_menu_widgets:
            menu_layout.addWidget(boton)           
        
        # Separador para empujar los botones hacia arriba
        menu_layout.addStretch(1)

        # --- Botón de Ajustes (Abajo a la derecha) ---
        
        self.pie_menu_widget = QWidget()
        self.pie_menu_layout = QHBoxLayout(self.pie_menu_widget)
        self.pie_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.pie_menu_layout.setAlignment(Qt.AlignRight)
        self.pie_menu_widget.hide() 

        self.boton_ajustes = QPushButton() 
        self.boton_ajustes.setFixedSize(self.MENU_ANCHURA_CERRADO - 10, self.MENU_ANCHURA_CERRADO - 10) 
        self.boton_ajustes.setIcon(QIcon("assets/ajustes.png")) 
        self.boton_ajustes.setIconSize(QSize(self.MENU_ANCHURA_CERRADO - 20, self.MENU_ANCHURA_CERRADO - 20))  # Ajusta el tamaño del icono
        self.boton_ajustes.setStyleSheet("""
            QPushButton { 
                background-color: transparent; 
                color: white; 
                border: none;
            }
            QPushButton:hover { background-color: rgba(85, 85, 85, 0.3); }
        """)
        
        self.pie_menu_layout.addWidget(self.boton_ajustes)
        menu_layout.addWidget(self.pie_menu_widget) 

        # --- 2. Contenido Principal ---
        principal_widget = QWidget()
        principal_widget.setStyleSheet("background-color: #F0F0F0;")
        principal_layout = QVBoxLayout(principal_widget)

        principal_layout.addStretch(1)

        titulo = QLabel("Bienvenido, Nom Ape")
        titulo.setFont(QFont("Arial", 18))
        titulo.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(titulo)   

        principal_layout.addSpacing(50)     
        
        texto_entrevistas = QLabel("Se han completado _ entrevistas")
        texto_entrevistas.setFont(QFont("Arial", 22))
        texto_entrevistas.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(texto_entrevistas)

        principal_layout.addStretch(1)

        # Añadir widgets al layout principal
        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(principal_widget)

        # --- 3. Parte de usuario ---

        usuario_widget = QWidget()
        usuario_layout = QHBoxLayout(usuario_widget)
        usuario_layout.setContentsMargins(0, 0, 0, 0)
        usuario_layout.setAlignment(Qt.AlignRight)

        boton_usuario = QPushButton()
        boton_usuario.setIcon(QIcon("assets/profesional.png"))
        boton_usuario.setIconSize(QSize(40, 40))        

        usuario_layout.addStretch(1)
        usuario_layout.addWidget(boton_usuario)

        principal_layout.addWidget(usuario_widget)

        # --- 4. Conexiones de botones ---

    def movimiento_menu(self):   
        
        if self.menu_abierto:
            # Estado A CERRAR (Actual: Abierto)
            anchura_final = self.MENU_ANCHURA_CERRADO
            color_menu = self.COLOR_CERRADO
            
            # Ocultar todos los botones de menú
            for widget in self.main_menu_widgets:
                widget.hide()
            self.pie_menu_widget.hide()             

            # Ajuste de alineación del botón hamburguesa: Insertar stretch a la izquierda
            if self.cabecera_menu_layout.itemAt(0) is None or self.cabecera_menu_layout.itemAt(0).widget() is not None:
                self.cabecera_menu_layout.insertStretch(0, 1)
            
        else:
            # Estado A ABRIR (Actual: Cerrado)
            anchura_final = self.MENU_ANCHURA_ABIERTO
            color_menu = self.COLOR_ABIERTO   
          
            # Mostrar botones con retardo para efecto escalonado
            for i, boton in enumerate(self.main_menu_widgets):
                QTimer.singleShot(i * 100, boton.show)  # Muestra cada botón con un retardo
            self.pie_menu_widget.show()  
            
        # Invertir el estado para el próximo clic
        self.menu_abierto = not self.menu_abierto
        
        # Aplicar el cambio de color
        self.menu_frame.setStyleSheet(f"background-color: {color_menu};")

        # Animación del ancho MÍNIMO y MÁXIMO
        self.animacion_min = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        self.animacion_min.setDuration(300)
        self.animacion_min.setStartValue(self.menu_frame.width())
        self.animacion_min.setEndValue(anchura_final)
        self.animacion_min.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacion_min.start()
        
        self.animacion_max = QPropertyAnimation(self.menu_frame, b"maximumWidth")
        self.animacion_max.setDuration(300)
        self.animacion_max.setStartValue(self.menu_frame.width())
        self.animacion_max.setEndValue(anchura_final)
        self.animacion_max.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacion_max.start()        
        
        
    