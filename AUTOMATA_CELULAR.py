# -*- coding: utf-8 -*-
"""
Automata Celular Main
v0.4.1
@author: Carlos Villagrasa Guerrero

python 3
numpy
pip3 install matplotlib
pip3 install pyqt5
"""
"""
Comprobación de librerías y ficheros necesarios
Argument vectors comandos de ejecución optparse

"""
import argparse
parser = argparse.ArgumentParser()
parser.parse_args()


import matplotlib.pyplot as plt #for plot
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from sip import SIP_VERSION_STR 

print("Qt version:", QT_VERSION_STR)
print("SIP version:", SIP_VERSION_STR)
print("PyQt version:", PYQT_VERSION_STR)

import sys
import math

"""
# libraries
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# create data
x = np.random.rand(15)
y = x+np.random.rand(15)
z = x+np.random.rand(15)
z=z*z

# Change color with c and alpha. I map the color to the X axis value.
plt.scatter(x, y, s=z*2000, c=x, cmap="Blues", alpha=0.4, edgecolors="grey", linewidth=2)

# Add titles (main and on axis)
plt.xlabel("the X axis")
plt.ylabel("the Y axis")
plt.title("A colored bubble plot")

plt.show()
"""

from PyQt5 import uic, QtWidgets


#import pyqtgraph as pg
import numpy
import ACF, ACF_QT, ACF_FILE
import csv
from random import randint, shuffle

numpy.set_printoptions(threshold=numpy.inf)

qtMain = "AUTOMATA_CELULAR.ui" # Enter file here.
qtSimulation = "SIMULATION.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtMain)
Ui_SimWindow, QtBaseClass = uic.loadUiType(qtSimulation)

class Sim(QtWidgets.QMainWindow, Ui_SimWindow):
    """
    Data_Especies
    Row -> different species
    col0 -> Direct fitness
    col1 -> Starting quantity
    col2 -> Asociation
    col3 -> Agrupation partner
    col4 -> Indirect fitness
    col5 -> Fenotipic flexibility
    col6 -> -
    col7 -> Agrupation new species
    col8 -> Parent for agrupation
    """
    """
    Matrix of species
    0->Individuos
    1->Recipientes asociación
    2->Actores asociación
    3->Asociados Recíprocos
    """
    """
    Muertes 0 SG
    Muertes 1 SI
    """
    global Data_Especies, Especies_Nicho, N_Nichos, N_Especies, Muertes
    
    def __init__(self):
        super().__init__()
        #Set UI
        self.setupUi(self)
        global Data_Especies, Especies_Nicho, N_Nichos, N_Especies, Muertes

        #Get input Data and set Qt window for simulation
        [Data_Especies, N_Nichos, N_Especies] = ACF.read_data_from_qt(window, self)
        
        #Initialize Deaths array and Species array
        Muertes = numpy.zeros((N_Nichos, N_Especies, 2))
        Especies_Nicho = numpy.zeros((N_Nichos, N_Especies, 4), dtype=numpy.int)

        #Initial setup for species
        ACF.inicial_set(Data_Especies, N_Nichos, N_Especies, Especies_Nicho) 
        ACF_QT.update_table(self.Display_Table, Especies_Nicho, Muertes, N_Nichos, N_Especies)
        
        """
        ACF_QT.potential(self, Data_Especies, N_Especies)
        """
        
        #Current generation
        self.GEN.display(1)
        
        #Buttons setup
        self.NEXT_Button.clicked.connect(self.NEXT)
        self.MUT_Button.clicked.connect(self.MUT)
        
        #Write initial data 
        ACF_FILE.data_write(window, self, Data_Especies, Especies_Nicho, N_Especies, 'w')
        
        #Output files for data checking
        f = open("out.txt",'w')
        f.close()
        f = open("flex.txt",'w')
        f.close()
    
    
    def MUT(self):        
        
        window.Continue_Button.setEnabled(True)
        window.Nodes.setEnabled(True)
        window.Resources.setEnabled(True)
        window.Reproduction.setEnabled(True)
        window.Deaths.setEnabled(True)
        window.Data_Table.setEnabled(True)
        for i in range(0,N_Especies):
            ACF_QT.change_item(window.Data_Table,i,1,"0") 
        
        self.hide()
        window.show()
        
    def MUT_Changes(self):
        
        global Data_Especies,Especies_Nicho, N_Nichos, N_Especies, Muertes
        
        N_Especies_temp = N_Especies
        N_Nichos_temp = N_Nichos
        
        [Data_Especies, N_Nichos, N_Especies] = ACF.read_data_from_qt(window, self)

        Especies_Nicho = ACF.resize_matrix_3d(Especies_Nicho, N_Nichos_temp, N_Especies_temp, N_Nichos, N_Especies)
        Muertes = ACF.resize_matrix_3d(Muertes, N_Nichos_temp, N_Especies_temp, N_Nichos, N_Especies)
        
        #Generación inicial de los nuevos seres
        ACF.inicial_set(Data_Especies, N_Nichos, N_Especies, Especies_Nicho) 

        ACF_QT.update_table(self.Display_Table, Especies_Nicho, Muertes, N_Nichos, N_Especies)    

        ACF_FILE.data_write(window, self, Data_Especies, Especies_Nicho, N_Especies, 'a')
        
    def NEXT(self):
        
        global Data_Especies,Especies_Nicho, N_Nichos, Muertes
        for t in range(0,self.GEN_STEP.value()):
            f = open("out.txt",'a')
            g = open("flex.txt",'a')
            """
            Asociación agrupación
            Actualmente en orden de índice ( TBU - orden aleatorio )
            Realizar una función para facilitar la lectura
            """
            print(t, file = f)
            print("GENERACIÓN " + str(self.GEN.intValue()), file = f)
            print("--------------------------------------------------------------------------------------------", file = f)
            print(t, file = g)
            print("GENERACIÓN " + str(self.GEN.intValue()), file = g)
            print("--------------------------------------------------------------------------------------------", file = g)
            """
            Muertes
            0 -> SG
            1 -> SI
            """
            
            #Eficacia = numpy.zeros((N_Nichos,N_Especies,4))
            #E_Total = 0
            
            self.Actual.setText("ASOCIACIÓN/AGRUPACIÓN")
            print(Especies_Nicho, file = f)
            for i in range(0,N_Nichos):
                self.progressBar.setValue((i/N_Nichos)*100)
                
                order1 = ACF.random_order(Especies_Nicho[i,:,:])
                temp_sin_asociar = Especies_Nicho[i,:,0].copy()
                k = 0
                print("AGR", file = f)
                print("Aggrupation", file = g)
                print("-------------------------------------------------", file = g)
                if len(order1) > 0:
                    while k < len(order1):
                        j = int(order1[k] / 10)
                        #print(j)
                        #if randint(0, 100) * Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]) <= Data_Especies[j,5]:
                        if Data_Especies[j,3] != -1 and temp_sin_asociar[j] > 0:
                            R = randint(0, 100)
                            
                            if Muertes[i,j,1] == 0 and Muertes[i,j,0] == 0:
                                #print(R)
                                if R <= Data_Especies[j,5]:
                                    if int(Data_Especies[j,3]) != j:
                                        if temp_sin_asociar[int(Data_Especies[j,3])] > 0:
                                            Especies_Nicho[i,int(Data_Especies[j,7]),0] = Especies_Nicho[i,int(Data_Especies[j,7]),0] + 1
                                            
                                            Especies_Nicho[i,int(Data_Especies[j,3]),0] = Especies_Nicho[i,int(Data_Especies[j,3]),0] - 1
                                            temp_sin_asociar[int(Data_Especies[j,3])] = temp_sin_asociar[int(Data_Especies[j,3])] - 1
                                            
                                            Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - 1
                                            temp_sin_asociar[j] = temp_sin_asociar[j] - 1
                                    else:
                                        if temp_sin_asociar[j] > 1:
                                            Especies_Nicho[i,int(Data_Especies[j,7]),0] = Especies_Nicho[i,int(Data_Especies[j,7]),0] + 1
                                            Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - 2
                                            temp_sin_asociar[j] = temp_sin_asociar[j] - 2  
                            else:
                                
                                print('NICHO {0} and ESPECIE{1}'.format(i, j), file = g)
                                R = randint(-10, 10)
                                print(R + (Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]))*100, file = g)
                                #print(R + (Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]))*100)
                                if R + (Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]))*100 <= Data_Especies[j,5]: #Agrupación 
                                    if int(Data_Especies[j,3]) != j:
                                        if temp_sin_asociar[int(Data_Especies[j,3])] > 0:
                                            Especies_Nicho[i,int(Data_Especies[j,7]),0] = Especies_Nicho[i,int(Data_Especies[j,7]),0] + 1
                                            
                                            Especies_Nicho[i,int(Data_Especies[j,3]),0] = Especies_Nicho[i,int(Data_Especies[j,3]),0] - 1
                                            temp_sin_asociar[int(Data_Especies[j,3])] = temp_sin_asociar[int(Data_Especies[j,3])] - 1
                                            
                                            Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - 1
                                            temp_sin_asociar[j] = temp_sin_asociar[j] - 1
                                    else:
                                        if temp_sin_asociar[j] > 1:
                                            Especies_Nicho[i,int(Data_Especies[j,7]),0] = Especies_Nicho[i,int(Data_Especies[j,7]),0] + 1
                                            Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - 2
                                            temp_sin_asociar[j] = temp_sin_asociar[j] - 2    
                        
                            
                            
                        """
                        else:
                            #REVISAR
                            Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] + Especies_Nicho[i,j,2]
                            Especies_Nicho[i,int(Data_Especies[j,3]),0] = Especies_Nicho[i,int(Data_Especies[j,3]),0] + Especies_Nicho[i,j,2]
                            Especies_Nicho[i,j,2] = 0
                        """
                        k = k +1
                        
                order2 = ACF.random_order(Especies_Nicho[i,:,:])
                temp_sin_asociar = Especies_Nicho[i,:,0].copy()
                
                k = 0
                print("ASO", file = f)
                if len(order2) > 0:
                    while k < len(order2):
                        j = int(order2[k] / 10)
                        
                        if Data_Especies[j,2] != -1 and temp_sin_asociar[j] > 0: #Asociación
                            if temp_sin_asociar[int(Data_Especies[j,2])] > 0:
                                if int(Data_Especies[int(Data_Especies[j,2]),2]) != j:
                                    Especies_Nicho[i,j,1] += 1
                                    temp_sin_asociar[j] -= 1
                                    Especies_Nicho[i,int(Data_Especies[j,2]),2] += 1 
                                    Especies_Nicho[i,int(Data_Especies[j,2]),0] -= 1
                                    temp_sin_asociar[int(Data_Especies[j,2])] -= 1
                                    Especies_Nicho[i,j,0] -= 1 
                                else:              
                                    if temp_sin_asociar[j] != 1 or int(Data_Especies[j,2]) != j:
                                        Especies_Nicho[i,j,3] += 1
                                        temp_sin_asociar[j] -= 1
                                        Especies_Nicho[i,int(Data_Especies[j,2]),3] += 1 
                                        Especies_Nicho[i,int(Data_Especies[j,2]),0] -= 1
                                        temp_sin_asociar[int(Data_Especies[j,2])] -= 1
                                        Especies_Nicho[i,j,0] -= 1 
                        
                        k = k +1
                
            print("FIN DE ASO/AGR", file = f)
            print(Especies_Nicho, file = f)
            #print(Especies_Nicho)
            #print(str(Especies_Nicho)) 
            
            """
            Cálculo de E
            """
            """
            CORREGIR
            for i in range(0,N_Nichos):
                E_Total = 0
                for j in range(0,N_Especies):
                    Eficacia[i,j,0] = Especies_Nicho[i,j,0]
                    Eficacia[i,j,1] = Especies_Nicho[i,j,1]
                    Eficacia[i,j,2] = Data_Especies[i,0]/(Data_Especies[i,0]+Data_Especies[i,4]) * Especies_Nicho[i,j,2]
                    Eficacia[i,j,3] = Data_Especies[i,0]/(Data_Especies[i,0]+Data_Especies[i,4]) * Especies_Nicho[i,j,3]
                    E_Total += Eficacia[i,j,:].sum()
                #print(Eficacia, file = f)
                for j in range(0,N_Especies):
                    Eficacia[i,j,0] = Eficacia[i,j,0]/E_Total
                    Eficacia[i,j,1] = Eficacia[i,j,1]/E_Total
                    Eficacia[i,j,2] = Eficacia[i,j,2]/E_Total
                    Eficacia[i,j,3] = Eficacia[i,j,3]/E_Total
            """
            #T = numpy.zeros((N_Especies))
            """
            for i in range(0,N_Especies): 

                for j in range(0, N_Nichos):
                    
                    T[i] += (Eficacia[j,i,0] * Especies_Nicho[j,i,0] +
                         Eficacia[j,i,1] * Especies_Nicho[j,i,1] +
                         Eficacia[j,i,2] * Especies_Nicho[j,i,2] +
                         Eficacia[j,i,3] * Especies_Nicho[j,i,3])

                T[i] = T[i]/Especies_Nicho[:,i,:].sum(axis = 1).sum() 
            print("EFICACIA", file = f)
            print(Eficacia, file = f)
            """
            """
            Selección de grupo
            """

            #}Ordenar por la proporción direct fitness/indirect fitness
            self.Actual.setText("SELECCIÓN DE GRUPO")
            Muertes = numpy.zeros((N_Nichos,N_Especies,2))
            
            order_if = numpy.argsort(Data_Especies[:,0]/Data_Especies[:,4])
            order = numpy.argsort(Data_Especies[:,0])
            
            print(order_if, file = f)    
            print(order, file = f)

            T_min = 0
            T_max = 0
            for i in range(1,len(order_if)): 
                if (Data_Especies[int(order_if[i]), 0]/Data_Especies[int(order_if[i]), 4]) > (Data_Especies[int(order_if[i - 1]), 0]/Data_Especies[int(order_if[i - 1]), 4]):               
                    shuffle(order_if[T_min:(T_max+1)])
                    T_min = i
                    T_max = i
                else:
                    T_max = i
            shuffle(order_if[T_min:(len(order_if)+1)])
            T_min = 0
            T_max = 0
            for i in range(1,len(order)): 
                if (Data_Especies[int(order[i]), 0]) > Data_Especies[int(order[i - 1]), 0]:   
                    shuffle(order[T_min:(T_max+1)])
                    T_min = i
                    T_max = i
                else:
                    T_max = i
            shuffle(order[T_min:(len(order)+1)])
            print("reordenado: 1->DF/IF; 2->DF", file = f)
            print(order_if, file = f)    
            print(order, file = f) 
            print("-------------------------------")
            print(Especies_Nicho)
            print("reordenado: 1->DF/IF; 2->DF")
            print(order_if)    
            print(order) 
            
            for i in range(0,N_Nichos):
                #print(i)
                self.progressBar.setValue((i/N_Nichos)*100)
                o = len(order) - 1
                k = window.Deaths.value()/100 * Especies_Nicho[i,:,:].sum(axis = 0).sum()
                k = math.ceil(k)
                print(k)
                
                while o >= 0 and k > 0: #individuos y recipientes
                    if Data_Especies[order[o],8] != -2:
                        no_zero = numpy.nonzero(Especies_Nicho[i,order[o],:2])
                        while len(no_zero[0]) != 0 and k > 0:
                            Random = randint(0, len(no_zero[0])-1)
                            
                            if Especies_Nicho[i,order[o],no_zero[0][Random]] >= k:
                                Especies_Nicho[i,order[o],no_zero[0][Random]] = Especies_Nicho[i,order[o],no_zero[0][Random]] - k
                                Muertes[i,order[o],0] += k
                                k = 0
                            else:
                                k = k - Especies_Nicho[i,order[o],no_zero[0][Random]]
                                Muertes[i,order[o],0] += Especies_Nicho[i,order[o],no_zero[0][Random]]
                                Especies_Nicho[i,order[o],no_zero[0][Random]] = 0
                            no_zero = numpy.nonzero(Especies_Nicho[i,order[o],:2])
                            
                    if k > 0:
                        o = o - 1
                o = len(order_if) - 1
                #print(k)
                print(Especies_Nicho)
                while o >= 0 and k > 0: # actores y reciprocos
                    print(k)
                    if Data_Especies[order_if[o],8] != -2:
                        no_zero = numpy.nonzero(Especies_Nicho[i,order_if[o],2:])
                        print(Especies_Nicho[i,order_if[o],2:])
                        print(no_zero[:])
                        while len(no_zero[0]) != 0 and k > 0:
                            Random = randint(0, len(no_zero[0])-1)
                            if Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] >= k:
                                Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] = Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] - k
                                Muertes[i,order_if[o],0] += k
                                k = 0
                            else:
                                k = k - Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2]
                                Muertes[i,order_if[o],0] += Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2]
                                Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] = 0
                            no_zero = numpy.nonzero(Especies_Nicho[i,order_if[o],2:])
                            print(Especies_Nicho)
                    if k > 0:
                        o = o - 1
            
            print("FIN DE SG", file = f)
            print(Especies_Nicho, file = f)
            """
            Alimentación
            """
            self.Actual.setText("SELECCIÓN DE INDIVIDUAL")
            if window.Reproduction.value() != 0:
                for i in range(0,N_Nichos):
                    self.progressBar.setValue((i/N_Nichos)*100)
                    temp_rec = window.Resources.value()
                    Feeded = numpy.zeros((N_Especies,4))
                    
                    ORDER = ACF.random_order(Especies_Nicho[i,:,:])

                    j = 0
                    if len(ORDER) > 0:
                        while temp_rec > 0 and j < len(ORDER):

                            if Especies_Nicho[i, int(ORDER[j] / 10), int(ORDER[j] % 10)] > 0:

                                if ORDER[j] % 10 == 0: #individual
                                    temp_rec = temp_rec - (Data_Especies[int(ORDER[j] / 10),0] * int(window.Reproduction.value())/100)
                                if ORDER[j] % 10 == 1: #asociación recipiente
                                    temp_rec = temp_rec - (Data_Especies[int(ORDER[j] / 10),0] * int(window.Reproduction.value())/100)
                                if ORDER[j] % 10 == 2 or ORDER[j] % 10 == 3: #asociación actor o reciproca
                                    temp_rec = temp_rec - ((Data_Especies[int(ORDER[j] / 10),4] + Data_Especies[ORDER[j] // 10,0]) * int(window.Reproduction.value())/100)
                                if temp_rec >= 0:
                                    Feeded[ORDER[j] // 10,ORDER[j] % 10] = Feeded[ORDER[j] // 10,ORDER[j] % 10] + 1
                                    
                            j = j +1
                        
                        Muertes[i,:,1] = Especies_Nicho[i,:,:].sum(axis = 1) - Feeded.sum(axis = 1)
                        
                        Especies_Nicho[i,:,:] = Feeded
                
            print("FIN DE SI", file = f)
            print(Especies_Nicho, file = f)
            """
            Reproducción
            """
            self.Actual.setText("REPRODUCCIÓN")
            temp_Especies = numpy.zeros((N_Nichos,N_Especies,4), dtype=int)
            for i in range(0, N_Nichos):
                self.progressBar.setValue((i/N_Nichos)*100)
                for j in range(0, N_Especies):
                    for k in range(0, 4):
                        
                        if k == 0:
                            temp_Especies[i,j,0] += Especies_Nicho[i,j,k] * Data_Especies[j,0]
   
                        if (k == 1 or k==3) and Data_Especies[j,2] != -1:
                            temp_Especies[i,j,0] += Especies_Nicho[i,j,k] * (Data_Especies[j,0] + Data_Especies[int(Data_Especies[j,2]),4])
      
                        if k == 2:
                            temp_Especies[i,j,0] += Especies_Nicho[i,j,k] * Data_Especies[j,0]
            Especies_Nicho = temp_Especies
            print("FIN DE REPRODUCCIÓN", file = f)
            print(Especies_Nicho, file = f)
            print("Deaggrupation", file = g)
            print("----------------------------------------------------", file = g)
            for i in range(0, N_Nichos):
                self.progressBar.setValue((i/N_Nichos)*100)
                for j in range(0, N_Especies):
                    
                    if Data_Especies[j,8] != -1: 
                        
                        print('NICHO {0} and ESPECIE{1}'.format(i, j), file = g)
                        print((Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]))*100, file = g)
                        print("random flex", file = g)
                        #print("random flex")
                        for l in range(0, Especies_Nicho[i,j,0]):
                            R = randint(0, 100)
                            #print(R)
                            print((R*0.2 - 10) + (Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]))*100, file = g)
                            #print((R*0.2 - 10) + (Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]))*100)
                            #if Muertes[i,j,0] > 0 and Data_Especies[int(Data_Especies[int(Data_Especies[j,8]),3]),4] < Data_Especies[int(Data_Especies[j,8]),0] and randint(0, 100) < Data_Especies[j,5]:
                            if Muertes[i,j,1] == 0 and Muertes[i,j,1] == 0:
                                if R > Data_Especies[j,5]:
                                    Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - 1
                                    Especies_Nicho[i,int(Data_Especies[j,8]),0] = Especies_Nicho[i,int(Data_Especies[j,8]),0] + 1
                                    Especies_Nicho[i,int(Data_Especies[int(Data_Especies[j,8]),3]),0] = Especies_Nicho[i,int(Data_Especies[int(Data_Especies[j,8]),3]),0] + 1
                            elif (R*0.2 - 10) + (Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]))*100 > Data_Especies[j,5]:
                                Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - 1
                                Especies_Nicho[i,int(Data_Especies[j,8]),0] = Especies_Nicho[i,int(Data_Especies[j,8]),0] + 1
                                Especies_Nicho[i,int(Data_Especies[int(Data_Especies[j,8]),3]),0] = Especies_Nicho[i,int(Data_Especies[int(Data_Especies[j,8]),3]),0] + 1
            print("FIN DE FLEXIBILIDAD", file = f)
            print(Especies_Nicho, file = f)                    
            
            temp_Especies = numpy.zeros((N_Nichos,N_Especies,4), dtype=int)
            for i in range(0, N_Nichos):
                self.progressBar.setValue((i/N_Nichos)*100)
                for j in range(0, N_Especies):
                    for I in range(0,int(Especies_Nicho[i,j,0])):

                        if N_Nichos > 4:
                            l = randint(-2, 2)
                            if i + l >= N_Nichos:    
                                temp_Especies[i + l - N_Nichos,j,0] += 1
                            elif i + l < 0:
                                temp_Especies[i + l + N_Nichos,j,0] += 1
                            else:
                                temp_Especies[i + l,j,0] += 1
                        else:
                            l = randint(0, N_Nichos - 1)
                            temp_Especies[l,j,0] += 1
                        
              

            Especies_Nicho = temp_Especies
            #print("FIN DE GEN")
            #print(str(Especies_Nicho))
            print("FIN DE REPARTO", file = f)
            print(Especies_Nicho, file = f)
            print("MUERTES", file = f)
            print(Muertes, file = f)
            #print(Especies_Nicho)
                

            ACF_QT.update_table(self.Display_Table, Especies_Nicho, Muertes, N_Nichos, N_Especies)
            
            """
            for i in range(0,N_Especies):
                
                # Potencial biótico
                
                if Data_Especies[i,2] == -1:  #direct fitness + Indirect fitness del asociado
                    
                    Temp = Data_Especies[i,0] * float(self.Display_Table.item(i,3).text()) # Falta el multiplicador
                    Temp_Acc = Data_Especies[i,0] * float(self.Display_Table.item(i,2).text()) # Falta el multiplicador
                else:
                    Temp = (Data_Especies[i,0] + Data_Especies[int(Data_Especies[i,2]),4]) * float(self.Display_Table.item(i,3).text()) # Falta el multiplicador
                    Temp_Acc = (Data_Especies[i,0] + Data_Especies[int(Data_Especies[i,2]),4]) * float(self.Display_Table.item(i,2).text()) # Falta el multiplicador
                
                #ACF.change_item(self.Display_Table,i,1,str(Temp)) #Actual
                #ACF.change_item(self.Display_Table,i,2,str(Temp_Acc)) #Accumulado
            """  
            
            
            #Graphic representation does'nt work on pyinstaller

            if self.Graph_Check.isChecked():
                self.Actual.setText("GRÁFICO")
                app.processEvents()
                
                # create data
                x = numpy.arange(N_Nichos*N_Especies)
                y = numpy.arange(N_Nichos*N_Especies)
                z = numpy.arange(N_Nichos*N_Especies)
                c = numpy.arange(N_Nichos*N_Especies)
               
                #print(Especies_Nicho)
                
                for i in range(0,N_Nichos):
                    for j in range(0,N_Especies):
                        #print(i+1)
                        #print(j+1)
                        #print(Especies_Nicho[i,j,:].sum())
                        
                        x[i*N_Especies+j] = i+1
                        y[i*N_Especies+j] = j+1
                        z[i*N_Especies+j] = Especies_Nicho[i,j,:].sum()
                       
                        self.progressBar.setValue((i/N_Nichos)*100)
                        #print(x)
                        #print(y)
                        #print(z)       
                
                plt.figure(self.GEN.intValue())
                # Change color with c and alpha. I map the color to the X axis value.
                plt.scatter(x, y, s=z, c=c, cmap="rainbow", alpha=0.4, edgecolors="grey", linewidth=2)
                
                # Add titles (main and on axis)
                plt.xlabel("Nichos")
                plt.ylabel("Especies")
                plt.title('A colored bubble plot {0}'.format(self.GEN.intValue()))
                
                plt.show()

            self.Actual.setText("")
            self.progressBar.setValue(0)
            
            print("RESULTADOS", file = f)    
            try:
                with open(window.CSV_NAME.text() + '_resultados.csv', 'a', newline='') as csvfile:
                    spamwriter = csv.writer(csvfile)
                    spamwriter.writerow(['GENERACIÓN ' + str(self.GEN.intValue())])
                    spamwriter.writerow(['--------------------------------'])
                    for i in range(0,N_Especies):
                        
                        spamwriter.writerow([self.Display_Table.item(i, 0).text()] +
                                            [self.Display_Table.item(i, 1).text()] +
                                            [self.Display_Table.item(i, 3).text()])
            except IOError:
                QtWidgets.QMessageBox.about(self, "ERROR", "Oops! Something is wrong with the file. Try again...")
                
            print("NICHOS", file = f)    
            try:
                with open(window.CSV_NAME.text() + '_nichos.csv', 'a', newline='') as csvfile:
                    spamwriter = csv.writer(csvfile)
                    spamwriter.writerow(['GENERACIÓN ' + str(self.GEN.intValue())])
                    spamwriter.writerow(['--------------------------------'])
                    for i in range(0,len(Especies_Nicho[:,0,0])): 
                        spamwriter.writerow(['NICHO ' + str(i)])
                        spamwriter.writerow(['--------------------------------'])
                        for j in range(0,len(Especies_Nicho[0,:,0])):
                            spamwriter.writerow(['ESPECIE ' + str(j)])
                            spamwriter.writerow(Especies_Nicho[i,j,:])
            except IOError:
                QtWidgets.QMessageBox.about(self, "ERROR", "Oops! Something is wrong with the file. Try again...")
                
            self.GEN.display(self.GEN.intValue() + 1)
            f.close()
        #self.GEN.display(self.GEN.intValue() + self.GEN_STEP.value())

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        ACF_QT.new_row(self.Data_Table, self.Data_Table.rowCount())
        
        self.Data_Table.cellChanged.connect(self.data_modified)
        
        self.Start_Button.clicked.connect(self.Start)
        self.Continue_Button.clicked.connect(self.Continue)
        self.Load_Button.clicked.connect(self.Load)
        self.Save_Button.clicked.connect(self.Save)
        self.EXIT_Button.clicked.connect(self.EXIT)
        self.Reset_Button.clicked.connect(self.Reset)
       
    def data_modified(self):
        self.Data_Table.cellChanged.disconnect(self.data_modified)
        if self.Data_Table.currentColumn() == 0:
            if self.Data_Table.item(self.Data_Table.currentRow(),self.Data_Table.currentColumn()).text():
                if self.Data_Table.currentRow() == self.Data_Table.rowCount() - 1:
                    ACF_QT.new_row(self.Data_Table, self.Data_Table.rowCount())
                    
            else:
                if self.Data_Table.currentRow() != 0:
                    print("NO")
        elif self.Data_Table.currentColumn() == 1:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un número entero positivo")
                ACF_QT.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
                
        elif self.Data_Table.currentColumn() == 2:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un número entero positivo")
                ACF_QT.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
                
        elif self.Data_Table.currentColumn() == 3:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un número entero positivo")
                ACF_QT.Tdelete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
        elif self.Data_Table.currentColumn() == 6: 
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un número entero positivo")  
                ACF_QT.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
        
        elif self.Data_Table.currentColumn() == 4:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text():
                found = False
                for i in range(0,self.Data_Table.rowCount() - 1):
                    if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text() == self.Data_Table.item(i, 0).text():
                        found = True
                        break
                if found == False:
                    QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un nombre de especie que ya exista")
                    ACF_QT.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
        elif self.Data_Table.currentColumn() == 5:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text():
                found = ACF_QT.find_item(self.Data_Table, self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text())
                if found == -1:
                    QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un nombre de especie que ya exista")
                    ACF_QT.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                    
                else:
                    if self.Data_Table.item(self.Data_Table.currentRow(), 3).text() and self.Data_Table.item(found, 3).text():
                        nombre = self.Data_Table.item(self.Data_Table.currentRow(), 0).text() + "(" + self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text() + ")"
                        
                        final = self.Data_Table.rowCount() - 1
                        ACF_QT.new_row(self.Data_Table, final)
                         
                        ACF_QT.change_item(self.Data_Table,final,0,nombre)
                        ACF_QT.change_item(self.Data_Table,final,1,"0")
                        found = ACF_QT.find_item(self.Data_Table, self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text())
                        ACF_QT.change_item(self.Data_Table,final,2,self.Data_Table.item(found, 3).text())
                        ACF_QT.change_item(self.Data_Table,final,3,self.Data_Table.item(self.Data_Table.currentRow(), 2).text())
                        ACF_QT.change_item(self.Data_Table,final,6,self.Data_Table.item(self.Data_Table.currentRow(), 6).text())
                        
                        
                        
                        
                        
                        
                    elif self.Data_Table.item(found, 3).text():
                        QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un indirect fitness en el recipiente")
                        ACF_QT.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                        
                    else:
                        QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un indirect fitness en el actor")
                        ACF_QT.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())

                #self.Data_Table.setRowCount(self.Data_Table.rowCount() + 1)
                    
            else:
                if self.Data_Table.currentRow() != 0:
                   print("NO")
                
        self.Data_Table.cellChanged.connect(self.data_modified)
            

    def Start(self):
        
        """
        for i in range (0,5):
            Data_Names[0] = self.Name_00.toPlainText()
            Data_Especies    

        
        Data_Especies[0,0] = self.Name_00.toPlainText()
        self.Name_01.setPlainText(self.Name_00.toPlainText())

        W_Sim = Sim()
        W_Sim.show()
        app.exec_()
        """
        self.CSV_NAME.setEnabled(False)
        self.Start_Button.setEnabled(False)
        self.Save_Button.setEnabled(False)
        self.Load_Button.setEnabled(False)
        self.Nodes.setEnabled(False)
        self.Resources.setEnabled(False)
        self.Reproduction.setEnabled(False)
        self.Deaths.setEnabled(False)
        self.Data_Table.setEnabled(False)
        self.dialog = Sim() 
        self.dialog.show()
        
    def Continue(self):
        
        """
        for i in range (0,5):
            Data_Names[0] = self.Name_00.toPlainText()
            Data_Especies    

        
        Data_Especies[0,0] = self.Name_00.toPlainText()
        self.Name_01.setPlainText(self.Name_00.toPlainText())

        W_Sim = Sim()
        W_Sim.show()
        app.exec_()
        """
        self.Continue_Button.setEnabled(False)

        self.Nodes.setEnabled(False)
        self.Resources.setEnabled(False)
        self.Reproduction.setEnabled(False)
        self.Deaths.setEnabled(False)
        self.Data_Table.setEnabled(False)
        
        self.dialog.MUT_Changes()
        self.dialog.show()
      
    def Reset(self):

        self.Continue_Button.setEnabled(False)

        self.Nodes.setEnabled(True)
        self.Resources.setEnabled(True)
        self.Reproduction.setEnabled(True)
        self.Deaths.setEnabled(True)
        self.Data_Table.setEnabled(True)
        
        self.CSV_NAME.setEnabled(True)
        self.Start_Button.setEnabled(True)
        self.Save_Button.setEnabled(True)
        self.Load_Button.setEnabled(True)
        
        self.Data_Table.setRowCount(0)
        ACF_QT.new_row(self.Data_Table, self.Data_Table.rowCount())
        
        self.dialog.hide()
        
    def Load(self):
        print("LOAD")
        try:
            with open(self.CSV_NAME.text() + '.csv', 'r', newline='') as csvfile:
                spamreader = csv.reader(csvfile)
                self.Data_Table.setRowCount(0)
                ACF_QT.new_row(self.Data_Table, self.Data_Table.rowCount())
                i = 0
                for row in spamreader:
                    if i == 0:
                        self.Nodes.setValue(int(row[7]))
                        self.Resources.setValue(int(row[8]))
                        self.Reproduction.setValue(int(row[9]))
                        self.Deaths.setValue(int(row[10]))
                    ACF_QT.change_item(self.Data_Table,i,0,row[0])
                    ACF_QT.change_item(self.Data_Table,i,1,row[1])
                    ACF_QT.change_item(self.Data_Table,i,2,row[2])
                    ACF_QT.change_item(self.Data_Table,i,3,row[3])
                    ACF_QT.change_item(self.Data_Table,i,4,row[4])
                    ACF_QT.change_item(self.Data_Table,i,5,row[5])
                    ACF_QT.change_item(self.Data_Table,i,6,row[6])
                    ACF_QT.new_row(self.Data_Table, self.Data_Table.rowCount())
                    i += 1
                
        except IOError:
            QtWidgets.QMessageBox.about(self, "ERROR", "Oops! Something is wrong with the file. Try again...")
    
    def Save(self):
        print("SAVE")
        try:
            with open(self.CSV_NAME.text() + '.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile)
                for i in range(0,self.Data_Table.rowCount() - 1):
                    print([self.Data_Table.item(i, 0).text()]  + 
                                         [self.Data_Table.item(i, 1).text()]  +
                                         [self.Data_Table.item(i, 2).text()]  +
                                         [self.Data_Table.item(i, 3).text()]  +
                                         [self.Data_Table.item(i, 4).text()]  +
                                         [self.Data_Table.item(i, 5).text()]  +
                                         [self.Data_Table.item(i, 6).text()])
                    if i == 0:
                        spamwriter.writerow([self.Data_Table.item(i, 0).text()]  + 
                                             [self.Data_Table.item(i, 1).text()]  +
                                             [self.Data_Table.item(i, 2).text()]  +
                                             [self.Data_Table.item(i, 3).text()]  +
                                             [self.Data_Table.item(i, 4).text()]  +
                                             [self.Data_Table.item(i, 5).text()]  +
                                             [self.Data_Table.item(i, 6).text()]  +
                                             [self.Nodes.value()] + [self.Resources.value()] + 
                                             [self.Reproduction.value()] + [self.Deaths.value()] )
                        
                    else:
                        spamwriter.writerow([self.Data_Table.item(i, 0).text()]  + 
                                             [self.Data_Table.item(i, 1).text()]  +
                                             [self.Data_Table.item(i, 2).text()]  +
                                             [self.Data_Table.item(i, 3).text()]  +
                                             [self.Data_Table.item(i, 4).text()]  +
                                             [self.Data_Table.item(i, 5).text()]  +
                                             [self.Data_Table.item(i, 6).text()])
        except IOError:
            QtWidgets.QMessageBox.about(self, "ERROR", "Oops! Something is wrong with the file. Try again...")
        
    def EXIT(self):
        sys.exit(0)
    """    
    def closeEvent(self, event):
        #Your desired functionality here
        print('Close button pressed')
        import sys
        sys.exit(0)
    """
    
    
if __name__ == '__main__':     
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()
    
    