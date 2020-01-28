import sys
from PyQt5.QtWidgets import QApplication
from CustomeWidget import MainWindow

#Intefaz gráfica de la aplicación del proyecto
app = QApplication(sys.argv)

window = MainWindow()
app.exec_()