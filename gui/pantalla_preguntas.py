from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

class PantallaPreguntas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
            
        principal_layout = QVBoxLayout(self)                     
        
        # ------------------- 1. Título pregunta con botón de información -------------------
        self.pregunta_widget = QWidget()
        self.pregunta_layout = QHBoxLayout(self.pregunta_widget)
        self.pregunta_layout.setAlignment(Qt.AlignCenter)

        # Botón de información
        self.boton_info = QPushButton()
        self.boton_info.setToolTip("Información sobre la pregunta")
        self.boton_info.setFixedSize(40, 40)
        self.boton_info.setIcon(QIcon("assets/info.png"))
        self.boton_info.setIconSize(QSize(30, 30))
        self.boton_info.setStyleSheet("""
            QPushButton { background: rgba(200, 200, 200, 0.6); border-radius: 15px;; padding: 10px; }
            QPushButton:hover { background-color: rgba(128, 128, 128, 0.6); border-radius: 15px; }
        """)

        # Variable para el número de pregunta
        numero_pregunta = 1
        
        # Título de la pregunta
        self.titulo_pregunta = QLabel("Pregunta "+ str(numero_pregunta) + " :")
        self.titulo_pregunta.setFont(QFont("Arial", 18, QFont.Bold))
        self.titulo_pregunta.setAlignment(Qt.AlignLeft)
        self.pregunta_layout.addWidget(self.titulo_pregunta)

        # Añadir el botón de información y el título al layout de la pregunta
        self.pregunta_layout.addWidget(self.boton_info)
        self.pregunta_layout.setSpacing(10)
        self.pregunta_layout.addWidget(self.titulo_pregunta)

        # ------------------- 2. Texto con la pregunta ------------------- 
        self.texto_pregunta = QLabel("""¿Usted reside en España? ¿Es usted tiene residencia legal o no?\n¿Tiene determinada la expulsión judicial de España?\n¿Tiene usted algún vínculo personal, familiar o profesional con personas españolas o residentes en España?\n¿Puede detallarlo?""")
        self.texto_pregunta.setFont(QFont("Arial", 14))
        self.texto_pregunta.setAlignment(Qt.AlignCenter)

        # ------------------- 3. Entrada de la pregunta -------------------  
        self.respuesta_widget = QTextEdit()
        self.respuesta_widget.setFont(QFont("Arial", 12))
        self.respuesta_widget.setPlaceholderText("Escriba su respuesta aquí...")
        self.respuesta_widget.setFixedHeight(350)
        self.respuesta_widget.setFixedWidth(1600)
        #self.respuesta_widget.setStyleSheet("padding-left: 10px; border-radius: 15px;")
        self.respuesta_widget.setStyleSheet("""
            QTextEdit {
                border-radius: 10px;
                border: 1px solid #ccc;
                padding: 5px;
                background-color: #f7f7f7;
            }
            QTextEdit:hover {
                border: 1px solid #999;
            }
            QTextEdit:focus {
                border: 1px solid #0078d7;
            }
        """)
        
        # ------------------- 4. Botón para entrada por voz -------------------
        self.boton_voz = QPushButton()
        self.boton_voz.setToolTip("Responder por voz")
        self.boton_voz.setFixedSize(50, 50)
        self.boton_voz.setIcon(QIcon("assets/micro.png"))
        self.boton_voz.setIconSize(QSize(40, 40))
        self.boton_voz.setProperty("estado_grabando", False) # Estado inicial: no grabando
        self.boton_voz.setStyleSheet("""
            /* Estilo Base */
            QPushButton { 
                background: rgba(200, 200, 200, 0.6); 
                border-radius: 15px;
                padding: 10px; 
            }
            
            /* Estilo al pasar el ratón */
            QPushButton:hover { 
                background-color: rgba(128, 128, 128, 0.6); 
            }
            
            /* Estilo cuando el estado es activo */
            QPushButton[estado_grabando="true"] { 
                background-color: #FF0000;
            }

            /* Estilo hover cuando ya está GRABANDO */
            QPushButton[estado_grabando="true"]:hover { 
                background-color: #CC0000;
            }
        """)

        # ------------------- 5. Botones atrás/siguiente/finalizar -------------------
        self.botones_widget = QWidget()
        self.botones_layout = QHBoxLayout(self.botones_widget)
        
        self.botones_layout.addStretch(1)

        #estilo boton
        estilo_boton = """                                   
            QPushButton { 
                color: white; 
                border: 1px solid rgba(255, 255, 255, 0.4); 
                padding: 10px 15px; 
                text-align: center;
                background-color: black; 
                border-radius: 15px;
            }
            QPushButton:hover { 
                background-color: rgba(71, 70, 70, 0.7); 
            }
        """

        #Boton atrás
        self.boton_atras = QPushButton("Atrás")
        self.boton_atras.setFont(QFont("Arial", 12))
        self.boton_atras.setStyleSheet(estilo_boton)
        self.boton_atras.setFixedSize(150,50)

        #Boton siguiente
        self.boton_siguiente = QPushButton("Siguiente")
        self.boton_siguiente.setFont(QFont("Arial", 12))
        self.boton_siguiente.setStyleSheet(estilo_boton)    
        self.boton_siguiente.setFixedSize(150,50)   

        # Añadir los botones al layout de botones
        self.botones_layout.addWidget(self.boton_atras)
        self.botones_layout.addStretch(1)
        self.botones_layout.addWidget(self.boton_siguiente) 
        self.botones_layout.addStretch(1)        

        principal_layout.addStretch(1)
        

        # ------------------- 6. Conexiones de botones ------------------- 
        self.boton_voz.clicked.connect(self.cambiar_color_voz)

        # Añadir el widgets al layout principal
        principal_layout.addWidget(self.pregunta_widget)
        principal_layout.addSpacing(20)
        principal_layout.addWidget(self.texto_pregunta)
        principal_layout.addSpacing(10)
        principal_layout.addWidget(self.respuesta_widget, alignment=Qt.AlignCenter)
        principal_layout.addSpacing(10)
        principal_layout.addWidget(self.boton_voz, alignment=Qt.AlignCenter)
        principal_layout.addSpacing(100)
        principal_layout.addWidget(self.botones_widget)

        
        principal_layout.addStretch(2)

    def cambiar_color_voz(self):           
        grabando_ahora = self.boton_voz.property("estado_grabando")
            
        #Invertir el estado
        nuevo_estado = not grabando_ahora
            
        # Aplicar el nuevo estado al botón
        self.boton_voz.setProperty("estado_grabando", nuevo_estado)
            
        # Forzar la actualización del estilo
        self.boton_voz.style().polish(self.boton_voz)