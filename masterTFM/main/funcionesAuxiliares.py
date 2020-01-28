import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import tensorflow as tf
from keras.layers import Dense, Flatten
from keras.models import Sequential
from copy import copy
import os
from keras.layers import LeakyReLU
from sklearn.preprocessing import MinMaxScaler


class Utils:

    # Función para definir la red neuronal
    def modeloRedNeuronal(numEntradas):
        modelo = Sequential()
        modelo.add(Dense(numEntradas, input_dim=numEntradas))
        modelo.add(Dense(64,  activation='relu',name="oculta_1"))
        modelo.add(Dense(32, activation='relu', name="oculta_2"))
        modelo.add(Dense(1,  name="salida"))
        modelo.compile(loss='mean_absolute_error', optimizer='Adam',metrics=['mse'])
        modelo.summary()
        return modelo


    def listaTransformada(numEntradas, numeroDatos, dfDatos):
        # Variables auxiliares
        listaEntradas = []
        listaSalidas = []
        auxInicio = 0
        auxFin = numEntradas

        while (auxFin + 1) <= numeroDatos:
            # print("El inicio del rango es: " + str(auxInicio) + " , y el fin es: " + str(auxFin))
            listaEntradas.append(dfDatos[auxInicio:auxFin].values.tolist())
            listaSalidas.append([dfDatos[auxFin]])
            auxInicio = auxInicio + 1
            auxFin = auxFin + 1

        return [np.asarray(listaEntradas), np.asarray(listaSalidas)]

    def dibujaFigura(self,listaEntrenamiento,listaValidacion,results):
        plt.scatter(range(len(listaValidacion[1])), listaValidacion[1], c='g')
        plt.scatter(range(len(results)), results, c='r')
        plt.title('validate')


    def rutaFicheroValido(self):

        if os.path.exists(self.file):

            if os.path.isdir(self.file):

                self.validacion = "Hay que seleccionar un fichero, no un directorio... \n"
                return False

            elif os.path.isfile(self.file):

                return True

            else:

                self.validacion = "Tienes que seleccionar un fichero válido... \n"
                return False
        else:

            self.validacion = "No existe el fichero seleccionado... \n"
            return False

    def validaExcel(self,excel):

        if len(excel.columns) >= 2:

            if len(excel.index) > 0:

                if not True in excel.isnull().values:

                    if not False in excel.apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all()).values:
                        return True

                    else:
                        self.validacion = "Todos los valores deben ser numéricos... \n"
                        return True

                else:
                    self.validacion = "No puede haber valores nulos... \n"
                    return True

            else:
                self.validacion = "El excel tiene que contener registros... \n"
                return False

        else:
            self.validacion = "El número de columnas no puede ser menos de 2... \n"
            return False

    def dataExcel(self,excel):

        self.precioMaximo = excel.precio.max()
        self.precioMinimo = excel.precio.min()

        tendenciaActual = ""

        mayorTendenciaDescendente  = 0
        mayorTendenciaAscendente = 0

        tendenciaAscendente = 0
        tendenciaDescendente = 0

        anteriorValor = 0
        anterior2Valor = 0

        j = 0
        for i in excel.precio:

            j = j +1
            if j==1:

                tendenciaActual = "Ascendente"
                tendenciaAscendente = 1
            else:

                if i > anteriorValor:

                    if i > anterior2Valor:
                        tendenciaActual = "Ascendente"
                        tendenciaAscendente = tendenciaAscendente + 1

                    elif i < anterior2Valor:
                        tendenciaActual = "Descendente"
                        tendenciaDescendente = 1

                        if tendenciaAscendente > mayorTendenciaAscendente:
                            mayorTendenciaAscendente = copy(tendenciaAscendente)

                        tendenciaAscendente = 0
                    else:
                        tendenciaActual = "Ascendente"
                        tendenciaAscendente = 1
                        tendenciaDescendente = 0

                else:

                    if i > anterior2Valor:
                        tendenciaActual = "Descentente"
                        tendenciaDescendente = tendenciaDescendente + 1

                    elif i < anterior2Valor:
                        tendenciaActual = "Ascendente"
                        tendenciaAscendente = 1

                        if tendenciaDescendente > mayorTendenciaDescendente:
                            mayorTendenciaDescendente = copy(tendenciaDescendente)

                        tendenciaDescendente = 0

                    else:

                        tendenciaActual = "Descendente"
                        tendenciaDescendente = 1
                        tendenciaAscendente = 0

            anterior2Valor = copy(anteriorValor)
            anteriorValor = copy(i)

        self.tendenciaActual = tendenciaActual
        self.tendenciaAscendente = tendenciaAscendente
        self.tendenciaDescentente = tendenciaDescendente
        self.mayorTendenciaAscendente = mayorTendenciaAscendente
        self.mayorTendenciaDescentente = mayorTendenciaDescendente
        self.ultimoValor = anteriorValor