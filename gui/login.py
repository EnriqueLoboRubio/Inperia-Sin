from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QGraphicsOpacityEffect
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, QSequentialAnimationGroup, QEasingCurve, QPropertyAnimation
from db.db import crear_bd, agregar_usuario, verificar_login, eliminar_usuario, encontrar_usuario
import re

#crear_bd()
#agregar_usuario("usuario1", "a@gmail.com", "1234", "usuario")
#agregar_usuario("profesional1", "b@gmail.com", "1234", "profesional")
#agregar_usuario("1", "1", "1", "usuario")
#agregar_usuario("2", "2", "2", "profesional")

class VentanaLogin(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("INPERIA")
        self.showMaximized() # maximizar la ventana
        self.showFullScreen() # pantalla completa
        self.setWindowIcon(QIcon("assets/icono_pest.ico"))
        self.initUI()
        self.tipo_pantalla = "usuario"
        self.intentos_fallidos = 0

    def initUI(self):        
        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QHBoxLayout()
        central.setLayout(layout_principal)

        #----Panel Izquierdo----
        self.izq = QLabel()
        pixmap = QPixmap("assets/inicio_usuario.jpg")
        self.izq.setPixmap(pixmap)
        self.izq.setAlignment(Qt.AlignCenter)
        self.izq.setScaledContents(True)
        self.izq.setMaximumSize(800, 1000) 
        
        # Overlay      
        self.texto_over = QLabel("INPERIA\nUSUARIO", self.izq)
        self.texto_over.setFont(QFont("Arial", 32, QFont.Bold))
        self.texto_over.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0.4);
                color: white;
                font-size: 32px;
                font-weight: bold;
                border-radius: 18px;
                padding: 18px;
                padding-top: 10px;
                padding-bottom: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        self.texto_over.setAlignment(Qt.AlignCenter)
        self.texto_over.setFixedSize(300, 100)
        self.texto_over.move(255,350)             

        #----Panel Derecho----
        der = QWidget()
        layout_der = QVBoxLayout()
        layout_der.setAlignment(Qt.AlignCenter)
        der.setLayout(layout_der)

        # Tipo de usuario        
        icono_usuario = QIcon("assets/usuario.png")
        icono_profesional = QIcon("assets/profesional.png")
        
        boton_usuario = QPushButton()
        boton_usuario.setIcon(icono_usuario)
        boton_usuario.setIconSize(QSize(50, 50))
        boton_usuario.setStyleSheet("""
            QPushButton {
                background-color: rgba(128, 128, 128, 0.4);
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(128, 128, 128, 0.6);
            }
        """)   
                  
        boton_profesional = QPushButton()
        boton_profesional.setIcon(icono_profesional)        
        boton_profesional.setIconSize(QSize(50, 50))        
        boton_profesional.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(128, 128, 128, 0.6);
            }
        """)

        iconos = QHBoxLayout()
        iconos.addStretch()
        iconos.addWidget(boton_usuario)
        iconos.addSpacing(30)
        iconos.addWidget(boton_profesional)
        layout_der.addLayout(iconos)

        layout_der.setContentsMargins(1, 1, 1, 1)
        layout_der.addStretch(1)

        # Campos de entrada
        self.input_correo = QLineEdit()
        self.input_correo.setFont(QFont("Arial", 12))
        self.input_correo.setPlaceholderText("correo@gmail.com")
        self.input_correo.setFixedHeight(40)
        self.input_correo.setStyleSheet("padding-left: 10px; border-radius: 8px;")
        self.input_correo.setFixedWidth(500)

        self.input_contraseña = QLineEdit()
        self.input_contraseña.setFont(QFont("Arial", 12))
        self.input_contraseña.setEchoMode(QLineEdit.Password)
        self.input_contraseña.setPlaceholderText("************")
        self.input_contraseña.setFixedHeight(40)
        self.input_contraseña.setStyleSheet("padding-left: 10px; border-radius: 8px;")
        self.input_contraseña.setFixedWidth(500)

        label_correo = QLabel("Correo")
        label_correo.setFont(QFont("Arial", 16))
        label_correo.setFixedWidth(500)
        label_contraseña = QLabel("Contraseña")
        label_contraseña.setFont(QFont("Arial", 16))
        label_contraseña.setFixedWidth(500)

        boton_entrar = QPushButton("Entrar")
        boton_entrar.setFont(QFont("Arial", 12))
        boton_entrar.setFixedHeight(50)
        boton_entrar.setFixedWidth(200)        
        boton_entrar.setStyleSheet("background-color: #222; color: white; border-radius: 8px;")
        boton_entrar.setCursor(Qt.PointingHandCursor)  
        boton_entrar.clicked.connect(self.verificar_usuario)      

        formulario = QVBoxLayout()
        formulario.setSpacing(20) 
        
        formulario.addWidget(label_correo, alignment=Qt.AlignCenter)
        formulario.addWidget(self.input_correo, alignment=Qt.AlignCenter)
        formulario.addWidget(label_contraseña, alignment=Qt.AlignCenter)
        formulario.addWidget(self.input_contraseña, alignment=Qt.AlignCenter)
        formulario.addWidget(boton_entrar, alignment=Qt.AlignCenter)
        
        contenedor_formulario = QWidget()
        contenedor_formulario.setLayout(formulario)
        contenedor_formulario.setMaximumWidth(1100)
        contenedor_formulario.setMinimumWidth(1050)
        
        layout_der.addWidget(contenedor_formulario, alignment=Qt.AlignVCenter | Qt.AlignHCenter)
        layout_der.addStretch()
        layout_der.addSpacing(300)
        layout_der.setSizeConstraint(QVBoxLayout.SetMinimumSize)      

        layout_principal.addWidget(self.izq, 1)
        layout_principal.addWidget(der, 2)
        
        # Cambio de tipo de usuario
        def cambiar_profesional():
            if self.tipo_pantalla != "profesional":
                self.intentos_fallidos = 0
                self.input_correo.clear()
                self.input_contraseña.clear()            
                self.tipo_pantalla = "profesional"            
                self.animacion_cambio_panel(QPixmap("assets/inicio_profesional.jpg"), "INPERIA\nPROFESIONAL")
                
                # Cambiar estilos de los botones
                boton_profesional.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(128, 128, 128, 0.4);
                        border: none;
                        border-radius: 10px;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: rgba(128, 128, 128, 0.6); 
                    }
                """)        
                boton_usuario.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        border: none;
                        padding: 0px;
                    }
                    QPushButton:hover {
                        background-color: rgba(128, 128, 128, 0.6);
                    }
                """)  

        def cambiar_usuario():   
            if self.tipo_pantalla != "usuario":    
                self.intentos_fallidos = 0
                self.input_correo.clear()
                self.input_contraseña.clear()
                self.tipo_pantalla = "usuario"          
                self.animacion_cambio_panel(QPixmap("assets/inicio_usuario.jpg"), "INPERIA\nUSUARIO")

                # Cambiar estilos de los botones
                boton_usuario.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(128, 128, 128, 0.4);
                        border: none;
                        border-radius: 10px;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: rgba(128, 128, 128, 0.6); 
                    }
                """)        
                boton_profesional.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        border: none;
                        padding: 0px;
                    }
                    QPushButton:hover {
                        background-color: rgba(128, 128, 128, 0.6);
                    }
                """)          

        boton_profesional.clicked.connect(cambiar_profesional)
        boton_usuario.clicked.connect(cambiar_usuario)  
   
    def animacion_cambio_panel(self, nuevo_pixmap, nuevo_texto):
            efecto_img = QGraphicsOpacityEffect()
            self.izq.setGraphicsEffect(efecto_img)
            animacion_img = QPropertyAnimation(efecto_img, b"opacity")
            animacion_img.setDuration(500)
            animacion_img.setStartValue(1)
            animacion_img.setEndValue(0)
            animacion_img.setEasingCurve(QEasingCurve.InOutQuad)

            efecto_txt = QGraphicsOpacityEffect()
            self.texto_over.setGraphicsEffect(efecto_txt)
            animacion_txt = QPropertyAnimation(efecto_txt, b"opacity")
            animacion_txt.setDuration(500)
            animacion_txt.setStartValue(1)
            animacion_txt.setEndValue(0)
            animacion_txt.setEasingCurve(QEasingCurve.InOutQuad)        
            
            self.izq.setPixmap(nuevo_pixmap)
            self.texto_over.setText(nuevo_texto)
        
            def animar_aparicion():
                animacion_img2 = QPropertyAnimation(efecto_img, b"opacity")
                animacion_img2.setDuration(400)
                animacion_img2.setStartValue(0)
                animacion_img2.setEndValue(1)
                animacion_img2.start()

                animacion_txt2 = QPropertyAnimation(efecto_txt, b"opacity")
                animacion_txt2.setDuration(400)
                animacion_txt2.setStartValue(0)
                animacion_txt2.setEndValue(1)
                animacion_txt2.start()
        
            """grupo = QSequentialAnimationGroup
            grupo.addAnimation(animacion_img)
            grupo.addAnimation(animacion_txt)
            grupo.finished.connect(actualizar_contenido)
            grupo.finished.connect(animar_aparicion)
            grupo.start()        """

    def verificar_usuario(self):

        def validar_formato_correo(correo):
            patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
            return re.match(patron, correo) is not None
            
        correo = self.input_correo.text()
        contrasena = self.input_contraseña.text()
        usuario = encontrar_usuario(correo)
        tipo_usuario = verificar_login(correo, contrasena)

        #verificar campos rellenos
        if not correo or not contrasena:
            QMessageBox.warning(self, "Error", "Por favor, completa todos los campos.")
            return
        
        #verificar formato de correo y contraseña
        if not validar_formato_correo(correo):
            QMessageBox.warning(self, "Error", "Formato del correo electrónico no válido")        
            return
        
        if usuario is not None:
            if tipo_usuario is not None:              
                if self.tipo_pantalla == tipo_usuario:
                    QMessageBox.information(self, "Inicio de sesión", f"Bienvenido, {tipo_usuario.capitalize()}")

                    if tipo_usuario == "usuario":
                        from gui.usuario_inicio import VentanaUsuario
                        self.ventana_usuario = VentanaUsuario()                    
                        self.ventana_usuario.show()                    
                        self.close()
                    else:
                        from gui.profesional_inicio import VentanaProfesional
                        self.ventana_profesional = VentanaProfesional()
                        self.ventana_profesional.show()
                        self.close()
                else:
                    QMessageBox.warning(self, "Error", f"Tipo de usuario incorrecto.")            
            else:        
                QMessageBox.warning(self, "Error", f"Usuario o contraseña incorrectos. \n Tiene {3 - self.intentos_fallidos} intentos restantes.")                          
                self.intentos_fallidos += 1
            if self.intentos_fallidos >= 3:
                QMessageBox.critical(self, "Cuenta suprimida", "Ha superado el número máximo de intentos. La cuenta ha sido elimnaada.\n Contacte con el administrador.")
                eliminar_usuario(correo)
                self.input_correo.clear()
                self.input_contraseña.clear()
                self.intentos_fallidos = 0
        else:
            QMessageBox.warning(self, "Error", "El usuario no existe")
            self.input_correo.clear()
            self.input_contraseña.clear()
            self.intentos_fallidos = 0

