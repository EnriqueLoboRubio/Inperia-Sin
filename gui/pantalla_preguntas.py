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
        self.numero_pregunta = 1
        
        # Título de la pregunta
        self.titulo_pregunta = QLabel("Pregunta "+ str(self.numero_pregunta) + " :")
        self.titulo_pregunta.setFont(QFont("Arial", 18, QFont.Bold))
        self.titulo_pregunta.setAlignment(Qt.AlignLeft)
        self.pregunta_layout.addWidget(self.titulo_pregunta)

        # Añadir el botón de información y el título al layout de la pregunta
        self.pregunta_layout.addWidget(self.boton_info)
        self.pregunta_layout.setSpacing(10)
        self.pregunta_layout.addWidget(self.titulo_pregunta)

        # ------------------- 2. Texto con la pregunta -------------------
        # Preguntas 
        self.texto_pregunta_content = ["¿Usted reside en España? ¿Es usted tiene residencia legal o no?\n¿Tiene determinada la expulsión judicial de España?\n¿Tiene usted algún vínculo personal, familiar o profesional con personas españolas o residentes en España?\n¿Puede detallarlo?",
                                  "¿Usted ha consumido drogas a lo largo de su vida? ¿Qué ha consumido?\n¿Cuándo se inició en dichos consumos?\n¿Ha participado usted en programas de deshabituación en los centros penitenciarios o en centros externos?\n¿Cuándo ha sido su último consumo? ¿Sigue consumiendo en la actualidad? ¿Ha tenido recaídas en consumos?",
                                  "¿Por qué cometió los delitos que figuran en su expediente? ¿Fue algo puntual o ha reincidido en su vida?",
                                  "¿Este es tu primer ingreso en prisión o has tenido otras condenas anteriormente?\n¿El cumplimiento de la condena actual es por delitos cometidos recientemente o\npor delitos cometidos hace tiempo y que estaban recurridos judicialmente?",
                                  "¿En algún momento has intentado evitar el cumplimiento de una condena o fugarte? ¿Por qué?",
                                  "¿Alguna vez has estado clasificado en primer grado o se te ha aplicado el artículo 10 de la LOGP?\n¿Qué recuerdas de esa etapa?",
                                  "¿Has tenido acceso a permisos penitenciarios?\n¿Qué impacto han tenido o crees que tendrían en ti? ¿Has quebrantado algún permiso? ¿por qué?",
                                  "¿Cómo describirías la relación con tu familia u otras personas cercanas desde que estás en prisión?\n¿Qué rol tienes en tu familia? ¿Recibes visitas o apoyo externo?\n¿Tu familia o amigos te ingresan dinero en tu cuenta de peculio?",
                                  "¿Dónde te gustaría disfrutar del permiso en caso de ser concedido? ¿Por qué has elegido ese lugar?\nEn caso de no tener familiares o amigos que los acojan:\n¿tiene acogida por alguna ONG? ¿Cuál y dónde? ¿Te has comprometido al cumplimiento de las normas de acogida de dicha ONG?",
                                  "¿Cómo es tu relación con otros internos y con el personal del centro? ¿Has vivido situaciones conflictivas? ¿Cuáles?\n¿Cómo es su cumplimiento de las normas de convivencia de su módulo?\n¿En qué actividades participas y qué destinos desempeñas en el módulo?"]
        
        self.lista_respuestas = [""] * 10  # Lista para almacenar las respuestas de las 10 preguntas

        self.texto_pregunta = QLabel(self.texto_pregunta_content[self.numero_pregunta - 1])
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

        #estilos botones
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

        estilo_finalizar = estilo_boton.replace("black", "#1E5631").replace("rgba(71, 70, 70, 0.7)", "#3A9D5A")    

        #Boton atrás
        self.boton_atras = QPushButton("Atrás")
        self.boton_atras.setFont(QFont("Arial", 12))
        self.boton_atras.setStyleSheet(estilo_boton)
        self.boton_atras.setFixedSize(150,50)
        self.boton_atras.hide()  # Ocultar el botón atrás inicialmente

        #Boton siguiente
        self.boton_siguiente = QPushButton("Siguiente")
        self.boton_siguiente.setFont(QFont("Arial", 12))
        self.boton_siguiente.setStyleSheet(estilo_boton)    
        self.boton_siguiente.setFixedSize(150,50)   

        #boton finalizar
        self.boton_finalizar = QPushButton("Finalizar")
        self.boton_finalizar.setFont(QFont("Arial", 12))
        self.boton_finalizar.setStyleSheet(estilo_finalizar)
        self.boton_finalizar.setFixedSize(150,50)
        self.boton_finalizar.hide()  # Ocultar el botón finalizar inicialmente

        # Añadir los botones al layout de botones
        self.botones_layout.addWidget(self.boton_atras)
        self.botones_layout.addStretch(1)
        self.botones_layout.addWidget(self.boton_siguiente)
        self.botones_layout.addWidget(self.boton_finalizar)
        self.botones_layout.addStretch(1)        

        principal_layout.addStretch(1)
        

        # ------------------- 6. Conexiones de botones ------------------- 
        self.boton_voz.clicked.connect(self.cambiar_color_voz)
        self.boton_atras.clicked.connect(self.ir_pregunta_atras)
        self.boton_siguiente.clicked.connect(self.ir_pregunta_siguiente)
        self.boton_finalizar.clicked.connect(self.finalizar_entrevista)

        # ------------------- 7. Añadir el widgets al layout principal -------------------
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

    # ------------------- 8. Funciones -------------------

    #Cambiar color del botón de voz al grabar
    def cambiar_color_voz(self):           
        grabando_ahora = self.boton_voz.property("estado_grabando")
            
        #Invertir el estado
        nuevo_estado = not grabando_ahora
            
        # Aplicar el nuevo estado al botón
        self.boton_voz.setProperty("estado_grabando", nuevo_estado)
            
        # Forzar la actualización del estilo
        self.boton_voz.style().polish(self.boton_voz)

    def cargar_pregunta(self):
        self.titulo_pregunta.setText("Pregunta "+ str(self.numero_pregunta) + " :")
        self.texto_pregunta.setText(self.texto_pregunta_content[self.numero_pregunta - 1])

    # Ir a la pregunta anterior
    def ir_pregunta_atras(self):
        # Guardar la respuesta actual
        self.lista_respuestas[self.numero_pregunta-1] = self.respuesta_widget.toPlainText()

        self.numero_pregunta = self.numero_pregunta - 1

        if self.numero_pregunta == 1:
            self.boton_atras.hide()
        else:
            self.boton_atras.show()        

        # Cargar la respuesta guardada si existe
        if(self.lista_respuestas[self.numero_pregunta - 1] != ""):
            self.respuesta_widget.setText(self.lista_respuestas[self.numero_pregunta - 1]) 
        else:
            self.respuesta_widget.clear() 

        self.cargar_pregunta()   

    def ir_pregunta_siguiente(self):
        # Guardar la respuesta actual
        self.lista_respuestas[self.numero_pregunta-1] = self.respuesta_widget.toPlainText()

        self.numero_pregunta = self.numero_pregunta + 1

        if self.numero_pregunta > 1:
            self.boton_atras.show()

        if self.numero_pregunta == 10:
            self.boton_siguiente.hide()
            self.boton_finalizar.show()
        else:
            self.boton_siguiente.show()
            self.boton_finalizar.hide()
    
        # Cargar la respuesta guardada si existe
        if(self.lista_respuestas[self.numero_pregunta - 1] != ""):
            self.respuesta_widget.setText(self.lista_respuestas[self.numero_pregunta - 1]) 
        else:
            self.respuesta_widget.clear() 

        self.cargar_pregunta()    

    def finalizar_entrevista(self):
        # Guardar la respuesta actual
        self.lista_respuestas[self.numero_pregunta] = self.respuesta_widget.toPlainText()

        #Guardar info en base de datos

        # Señal para pasar a la pantalla de resumen
        self.entrevista_finalizada.emit()


