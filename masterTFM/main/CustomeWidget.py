
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QLabel, QMainWindow, QPushButton, QGridLayout, QPlainTextEdit, QWidget, \
    QLineEdit, QTabWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QAbstractScrollArea, \
    QSizePolicy
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.patches as mpatches
from qtpy import QtWidgets, QtCore
import numpy as np


from funcionesAuxiliares import Utils
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

class MainWindow(QMainWindow):

    def __init__(self,*args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("TFM - Inversión Bolsa")

        self.file = ""
        self.area = QPlainTextEdit()
        self.lineaFichero = QLineEdit()
        self.validacion = ""

        layout = QGridLayout()
        self.createlayoutMain(layout)

        self.window = QWidget()
        self.window.setLayout(layout)
        self.window.show()
        self.window.setFixedSize(self.window.size())


    def createlayoutMain(self,layout):

        #Icono
        label = QLabel("Ayuda Broker")
        label.setFont(QFont("Helvetica", 30))
        layout.addWidget(label, 0, 5)

        #Dialogo Carga Fichero
        lineaFichero = QLineEdit()
        lineaFichero.setReadOnly(True)
        self.lineaFichero = lineaFichero

        botonFile = QPushButton("Cargar Fichero")
        botonFile.clicked.connect(self.filedialog)

        layout.addWidget(lineaFichero, 1, 0,1,12)
        layout.addWidget(botonFile, 1, 12)

        #Boton ejecutar algoritmo
        botonMain = QPushButton("Ejecutar Algoritmo")
        botonMain.clicked.connect(self.ejecuta_algoritmo)
        layout.addWidget(botonMain, 2, 0)

        #Cuadro de logs oculto por defecto
        logarea = QPlainTextEdit()
        logarea.setReadOnly(True)
        logarea.setVisible(False)
        self.area = logarea
        layout.addWidget(logarea,3,0,3,18)

        #Tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "Gráfica Red Neuronal Entrenada")
        self.tabs.addTab(self.tab2, "Datos útiles")
        self.tabs.addTab(self.tab3, "Predecir otro valor")

        #Tab Gráfica
        self.tab1.layout = QVBoxLayout()
        self.labelGraph = QLabel(self)
        self.tab1.layout.addWidget(self.labelGraph)
        self.tab1.setLayout(self.tab1.layout)

        #Tab Datos Útiles
        self.tab2.layout = QGridLayout()
        self.tab2.setLayout(self.tab2.layout)

        self.font = QFont("Helvetica", 15)
        self.font.setBold(True)

        self.lTendenciaActual = QLabel("Tendencia Actual:")
        self.lTendenciaActual.setFont(self.font)
        self.tab2.layout.addWidget(self.lTendenciaActual, 1, 1)

        self.lAscendente = QLabel("Ascendente:")
        self.lAscendente.setFont(self.font)

        self.lDescendente = QLabel("Descendente:")
        self.lDescendente.setFont(self.font)

        self.lMayorNumDiasSubiendo = QLabel("Mayor nº de días subiendo:")
        self.lMayorNumDiasSubiendo.setFont(self.font)
        self.tab2.layout.addWidget(self.lMayorNumDiasSubiendo, 5, 1)

        self.lMayorNumDiasBajando = QLabel("Mayor nº de días bajando:")
        self.lMayorNumDiasBajando.setFont(self.font)
        self.tab2.layout.addWidget(self.lMayorNumDiasBajando, 7, 1)

        self.lPrecioMinimo = QLabel("Precio Mínimo:")
        self.lPrecioMinimo.setFont(self.font)
        self.tab2.layout.addWidget(self.lPrecioMinimo, 9, 1)

        self.lPrecioMaximo = QLabel("Precio Máximo:")
        self.lPrecioMaximo.setFont(self.font)
        self.tab2.layout.addWidget(self.lPrecioMaximo, 11, 1)

        fontvalor = QFont("Helvetica", 15)

        self.lTendenciaActual = QLabel("")
        self.lTendenciaActual.setFont(fontvalor)
        self.tab2.layout.addWidget(self.lTendenciaActual, 1, 2)

        self.lAscendenteDescendente = QLabel("")
        self.lAscendenteDescendente.setFont(fontvalor)
        self.tab2.layout.addWidget(self.lAscendenteDescendente, 3, 2)

        self.lMayorNumDiasBajando = QLabel("")
        self.lMayorNumDiasBajando.setFont(fontvalor)
        self.tab2.layout.addWidget(self.lMayorNumDiasBajando, 5, 2)

        self.lMayorNumDiasSubiendo = QLabel("")
        self.lMayorNumDiasSubiendo.setFont(fontvalor)
        self.tab2.layout.addWidget(self.lMayorNumDiasSubiendo, 7, 2)

        self.lPrecioMinimo = QLabel("")
        self.lPrecioMinimo.setFont(fontvalor)
        self.tab2.layout.addWidget(self.lPrecioMinimo, 9, 2)

        self.lPrecioMaximo = QLabel("")
        self.lPrecioMaximo.setFont(fontvalor)
        self.tab2.layout.addWidget(self.lPrecioMaximo, 11, 2)

        self.lprediccion = QLabel("")
        self.tab2.layout.addWidget(self.lprediccion, 13, 1, 1, 2)

        self.tab2.layout.setRowStretch(0, 1)
        self.tab2.layout.setRowStretch(2, 1)
        self.tab2.layout.setRowStretch(4, 1)
        self.tab2.layout.setRowStretch(6, 1)
        self.tab2.layout.setRowStretch(8, 1)
        self.tab2.layout.setRowStretch(10, 1)
        self.tab2.layout.setRowStretch(12, 1)

        self.tab2.layout.setColumnStretch(0, 1)
        self.tab2.layout.setColumnStretch(3, 1)

        #Tab otro valor
        self.tab3.layout = QGridLayout()
        self.tab3.setLayout(self.tab3.layout)

        self.precio1 = QLineEdit()
        self.precio2 = QLineEdit()
        self.precio3 = QLineEdit()
        self.precio4 = QLineEdit()
        self.precio5 = QLineEdit()
        self.precio6 = QLineEdit()
        self.precio7 = QLineEdit()
        self.precio8 = QLineEdit()

        self.lprecio1 = QLabel("Día 1: ")
        fontN = self.lprecio1.font()
        fontN.setBold(True)
        self.lprecio1.setFont(fontN)
        self.tab3.layout.addWidget(self.lprecio1, 3, 1)

        self.lprecio2 = QLabel("Día 2: ")
        self.lprecio2.setFont(fontN)
        self.tab3.layout.addWidget(self.lprecio2, 3, 3)

        self.lprecio3 = QLabel("Día 3: ")
        self.lprecio3.setFont(fontN)
        self.tab3.layout.addWidget(self.lprecio3, 4, 1)

        self.lprecio4 = QLabel("Día 4: ")
        self.lprecio4.setFont(fontN)
        self.tab3.layout.addWidget(self.lprecio4, 4, 3)

        self.lprecio5 = QLabel("Día 5: ")
        self.lprecio5.setFont(fontN)
        self.tab3.layout.addWidget(self.lprecio5, 5, 1)

        self.lprecio6 = QLabel("Día 6: ")
        self.lprecio6.setFont(fontN)
        self.tab3.layout.addWidget(self.lprecio6, 5, 3)

        self.lprecio7 = QLabel("Día 7: ")
        self.lprecio7.setFont(fontN)
        self.tab3.layout.addWidget(self.lprecio7, 6, 1)

        self.lprecio8 = QLabel("Día 8: ")
        self.lprecio8.setFont(fontN)
        self.tab3.layout.addWidget(self.lprecio8, 6, 3)

        self.tab3.layout.setRowStretch(0, 1)
        self.tab3.layout.setRowStretch(1, 1)
        self.tab3.layout.setRowStretch(7, 1)
        self.tab3.layout.setRowStretch(9, 1)
        self.tab3.layout.setRowStretch(11, 1)
        self.tab3.layout.setColumnStretch(0, 1)
        self.tab3.layout.setColumnStretch(5, 1)

        self.ltituloTab3 = QLabel("Para predecir otro precio, es necesario indicar los precios de los 8 días anteriores")
        self.tab3.layout.addWidget(self.ltituloTab3, 1, 1, 1, 4)

        self.tab3.layout.addWidget(self.precio1, 3, 2)
        self.tab3.layout.addWidget(self.precio2, 3, 4)

        self.tab3.layout.addWidget(self.precio3, 4, 2)
        self.tab3.layout.addWidget(self.precio4, 4, 4)

        self.tab3.layout.addWidget(self.precio5, 5, 2)
        self.tab3.layout.addWidget(self.precio6, 5, 4)

        self.tab3.layout.addWidget(self.precio7, 6, 2)
        self.tab3.layout.addWidget(self.precio8, 6, 4)

        self.botonNuevoValor = QPushButton("Predecir Precio")
        self.botonNuevoValor.clicked.connect(self.predecirNuevoValor)
        self.tab3.layout.addWidget(self.botonNuevoValor, 8, 3)

        self.lnuevoPrecioTab3 = QLabel("")
        self.tab3.layout.addWidget(self.lnuevoPrecioTab3, 10, 1, 1, 4)

        layout.addWidget(self.tabs, 6, 0, 2, 18)
        self.tabs.setVisible(False)

    def predecirNuevoValor(self):
        if not ((self.precio1.text().strip() == "") or (self.precio2.text().strip() == "") or (self.precio3.text().strip() == "") or  (self.precio4.text().strip() == "") or (self.precio5.text().strip() == "") or (self.precio6.text().strip() == "") or (self.precio7.text().strip() == "") or (self.precio8.text().strip() == "")):
            prediccion = np.asarray([self.precio1.text().strip(),self.precio2.text().strip(),self.precio3.text().strip(),self.precio4.text().strip(),self.precio5.text().strip(),self.precio6.text().strip(),self.precio7.text().strip(),self.precio8.text().strip()])
            entradaPrediccion = []
            entradaPrediccion.append(prediccion)
            try:
                res = self.modelo.predict([entradaPrediccion])
                self.lnuevoPrecioTab3.setText("El próximo precio es: " + str(res[0][0]))
            except Exception as p:
                self.area.insertPlainText("Algo fue mal durante la ejecución del algoritmo, revisa los datos de entrada...\n")
                self.area.repaint()
                print(str(p))
        else:
            self.area.insertPlainText("Todos los campos deben estar rellenos...\n")
            self.area.repaint()

    def filedialog(self):
        # Cargar Archivo
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*.csv')
        if fileName:
            self.file = fileName
            self.lineaFichero.setText(self.file)
            self.lineaFichero.repaint()

    def initAlgoritmo(self):
        self.area.setPlainText("")
        self.area.repaint()
        self.tabs.hide()
        plt.cla()

        if os.path.exists("grafico.jpg"):
            os.remove("grafico.jpg")

    def ejecuta_algoritmo(self):

        self.area.show()

        #Limpiamos las areas de logs, gráfica y datos
        self.initAlgoritmo()

        if Utils.rutaFicheroValido(self):

            try:
                # Leemos el CSV completo que contiene los datos
                self.datos_csv = pd.read_csv(self.file, delimiter=",", index_col=0, parse_dates=["date"])

                if Utils.validaExcel(self, self.datos_csv):
                    self.area.insertPlainText("El Formato del excel es correcto...\n")
                    self.area.repaint()
                    # Creamos la Red Neuronal

                    # Tomamos todos los datos y los dividimos en un 80% para entrenat y 20% para validar
                    # year2017 = datos_csv.close['2017-01-01':'2017-12-31']
                    year = self.datos_csv.precio

                    # count2017 = len(datos_csv.close['2017-01-01':'2017-12-31'])
                    count = len(self.datos_csv.precio)

                    numEntradas = 8
                    numDatosEntrenamiento = round(count * 0.8)
                    numDatosValidacion = round(count * 0.2)

                    self.area.insertPlainText("El número total de datos son: " + str(count) + "\n")
                    self.area.insertPlainText("Los datos de entrenamiento son: " + str(numDatosEntrenamiento) + "\n")
                    self.area.insertPlainText("Los datos de validacion son: " + str(numDatosValidacion) + "\n")
                    self.area.repaint()

                    dfEntrenamiento = year[:numDatosEntrenamiento]
                    dfValidacion = year[numDatosEntrenamiento:]

                    print(" Entrenamiento: Elementos sobrantes del array será: " + str(
                        numDatosEntrenamiento % numEntradas) + " y se usaran " + str(
                        round(numDatosEntrenamiento / numEntradas)))
                    print(" Validacion: Elementos sobrantes del array será: " + str(
                        numDatosValidacion % numEntradas) + " y se usaran " + str(
                        round(numDatosValidacion / numEntradas)))
                    listaEntrenamiento = Utils.listaTransformada(numEntradas, numDatosEntrenamiento, dfEntrenamiento)
                    listaValidacion = Utils.listaTransformada(numEntradas, numDatosValidacion, dfValidacion)

                    print(str(listaEntrenamiento[0][:2]))
                    print(str(listaEntrenamiento[1][:2]))

                    try:
                        self.modelo = Utils.modeloRedNeuronal(numEntradas)
                        self.historic = self.modelo.fit(listaEntrenamiento[0], listaEntrenamiento[1], epochs=40,
                                                        validation_data=(listaValidacion[0], listaValidacion[1]),
                                                        batch_size=numEntradas)
                        self.area.insertPlainText("FIN: La red neuronal ha sido entrenada\n")
                        self.area.repaint()

                        # Generamos la gráfica y rellenamos la tab 1
                        results = self.modelo.predict(listaValidacion[0])
                        if len(results) > 100:
                            plt.scatter(range(len(listaValidacion[1][:100])), (listaValidacion[1])[:100], c='g')
                            plt.scatter(range(len(results[:100])), results[:100], c='r')
                        else:
                            plt.scatter(range(len(listaValidacion[1])), listaValidacion[1], c='g')
                            plt.scatter(range(len(results)), results, c='r')

                        plt.xlabel("Punto Evaluado")
                        plt.ylabel("Precio")
                        plt.title('Red Neuronal entrenada vs realidad')

                        score = self.modelo.evaluate(listaEntrenamiento[0], listaEntrenamiento[1], batch_size=128)
                        print(str(self.modelo.metrics_names))
                        print("La efectividad ha sido del: " + str(score))

                        red_patch = mpatches.Patch(color='red', label='Precios predichos')
                        green_patch = mpatches.Patch(color='green', label='Precios reales')
                        plt.legend(handles=[red_patch, green_patch])
                        plt.savefig('grafico.jpg')
                        pixmap = QPixmap('grafico.jpg')
                        self.labelGraph.setPixmap(pixmap)
                        self.tabs.setVisible(True)

                        # Generamos los datos útiles y rellenamos la tab 2
                        Utils.dataExcel(self, self.datos_csv)

                        fontvalor = QFont("Helvetica", 15)

                        self.lTendenciaActual.setText(str(self.tendenciaActual))
                        self.lMayorNumDiasBajando.setText(str(self.mayorTendenciaDescentente))
                        self.lMayorNumDiasSubiendo.setText(str(self.mayorTendenciaAscendente))
                        self.lPrecioMinimo.setText(str(self.precioMinimo))
                        self.lPrecioMaximo.setText(str(self.precioMaximo))

                        if self.tendenciaActual == "Ascendente":

                            self.tab2.layout.addWidget(self.lAscendente, 3, 1)
                            self.lAscendenteDescendente.setText(str(self.tendenciaAscendente))

                        else:

                            self.tab2.layout.addWidget(self.lDescendente, 3, 1)
                            self.lAscendenteDescendente.setText(str(self.tendenciaDescentente))

                        prediccionArray = np.asarray(self.datos_csv.tail(8).precio.values.tolist())
                        entradaPrediccion = []
                        entradaPrediccion.append(prediccionArray)

                        res = self.modelo.predict([entradaPrediccion])
                        self.lprediccion.setText(
                            "La red Neuronal predice que el próximo precio será: " + str(res[0][0]))
                    except Exception as e:
                        self.area.insertPlainText("Hubo algun error durante la ejecución del algritmo\n")
                        self.area.repaint()
                        print(str(e))
                else:
                    self.area.insertPlainText(self.validacion)
                    self.area.repaint()
                    
            except Exception as b:
                self.area.insertPlainText("Algo fue mal durante la lectura del CSV, revisa que sea correcto\n")
                self.area.repaint()
                print(str(b))

        else:
            self.area.insertPlainText(self.validacion)
            self.area.repaint()
