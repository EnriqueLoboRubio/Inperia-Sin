from PyQt5.QtWidgets import QApplication
from gui.login import VentanaLogin
import sys

app = QApplication(sys.argv)
ventana_login = VentanaLogin()
ventana_login.show()

sys.exit(app.exec_())
