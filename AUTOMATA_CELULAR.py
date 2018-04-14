# -*- coding: utf-8 -*-
"""
Automata Celular Main
v0.2.0
@author: Carlos Villagrasa Guerrero
"""
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from sip import SIP_VERSION_STR 
print("Qt version:", QT_VERSION_STR)
print("SIP version:", SIP_VERSION_STR)
print("PyQt version:", PYQT_VERSION_STR)

import sys
import math
from PyQt5 import QtCore, QtGui, uic, QtWidgets
#import pyqtgraph as pg
import numpy
import ACF
import csv
from random import randint, sample, shuffle

numpy.set_printoptions(threshold=numpy.inf)

qtMain = "AUTOMATA_CELULAR.ui" # Enter file here.
qtSimulation = "SIMULATION.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtMain)
Ui_SimWindow, QtBaseClass = uic.loadUiType(qtSimulation)

class Sim(QtWidgets.QMainWindow,Ui_SimWindow):
    
    """
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
    global Data_Especies,Especies_Nicho, N_Nichos, N_Especies, Muertes
    
    """
    Muertes 0 SG
    Muertes 1 SI
    """
    
    def __init__(self):
        super().__init__()
        #Set UI
        self.setupUi(self)
        global Data_Especies,Especies_Nicho, N_Nichos, N_Especies, Muertes
        N_Especies = window.Data_Table.rowCount() - 1
        #Number of niches?
        N_Nichos = window.Nodes.value()
        Muertes = numpy.zeros((N_Nichos,N_Especies,2))
        """
        # create plot
        plt = pg.plot()
        plt.showGrid(x=True,y=True)
        plt.addLegend()
        """
        #Adjust table to number of species
        self.Display_Table.setRowCount(N_Especies + 1)
        #Set matrix for data of the species
        Data_Especies = numpy.zeros((N_Especies, 9))
        
        for i in range(0,N_Especies):
            Data_Especies[i,8] = -1
            Data_Especies[i,6] = -1
            
        #Get data for the species
        for i in range(0,N_Especies):
            #Set name on the table
            
            ACF.change_item(self.Display_Table,i,0,window.Data_Table.item(i,0).text())
         
            Data_Especies[i,1] = int(window.Data_Table.item(i,1).text())    #Catidad inicial
            Data_Especies[i,0] = int(window.Data_Table.item(i,2).text())    #direct fitness
            Data_Especies[i,4] = int(window.Data_Table.item(i,3).text())    #indirect fitness
       
            
            if window.Data_Table.item(i,4).text(): #Asociación
                Data_Especies[i,2] = ACF.find_item(window.Data_Table, window.Data_Table.item(i,4).text())
            else:
                Data_Especies[i,2] = -1

            if window.Data_Table.item(i,5).text(): #Agrupación
                #compañero
                Data_Especies[i,3] = ACF.find_item(window.Data_Table, window.Data_Table.item(i,5).text())
                #destino de agrupación
                Data_Especies[i,7] = ACF.find_item(window.Data_Table, window.Data_Table.item(i,0).text() + "(" + window.Data_Table.item(i,5).text() + ")")
                #origen de agrupación
                Data_Especies[int(Data_Especies[i,7]),8] = i
            else:
                Data_Especies[i,3] = -1
                Data_Especies[i,7] = -1
        
            Data_Especies[i,5] = int(window.Data_Table.item(i,6).text())
             
        
        """
        Matrix of species
        0->Individuos
        1->Recipientes asociación
        2->Actores asociación
        """
        print(Data_Especies)
        Especies_Nicho = numpy.zeros((N_Nichos,N_Especies,4), dtype=numpy.int)
        
        
        #Generación inicial
        
        ACF.inicial_set(Data_Especies, N_Nichos, N_Especies, Especies_Nicho) 
        
        self.Display_Table.setColumnCount(N_Nichos + 4)
        for i in range(0,N_Nichos):
            self.Display_Table.setHorizontalHeaderItem(i + 4, QtWidgets.QTableWidgetItem("Nicho " + str(i + 1)))
        
        for i in range(0,N_Especies):
            # Potencial biótico
            """
            if Data_Especies[i,2] == -1:  #direct fitness + Indirect fitness del asociado
                Temp = Data_Especies[i,0] * Data_Especies[i,1] # Falta el multiplicador
            else:
                Temp = (Data_Especies[i,0] + Data_Especies[int(Data_Especies[i,2]),4]) * Data_Especies[i,1] # Falta el multiplicador
            ACF.change_item(self.Display_Table,i,1,str(Temp)) #actual
            ACF.change_item(self.Display_Table,i,2,str(Temp)) #acumulado
            """
            for j in range(0, N_Nichos):
                ACF.change_item(self.Display_Table,i,j+4,str(Especies_Nicho[j,i,0]))
            ACF.change_item(self.Display_Table,i,3,str(Especies_Nicho[:,i,:].sum(axis = 1).sum()))
        
        ACF.change_item(self.Display_Table,N_Especies,0,"Total")
        
        ACF.refresh_total(self.Display_Table, N_Nichos, N_Especies, Especies_Nicho)
        
        #Current generation
        self.GEN.display(1)
        #Next step button
        self.NEXT_Button.clicked.connect(self.NEXT)
        #self.MUT_Button.clicked.connect(self.MUT)
        print("DATOS")
        try:
            with open(window.CSV_NAME.text() + '_datos.csv', 'w', newline='') as csvfile: 
                spamwriter = csv.writer(csvfile)
                for i in range(0,len(Data_Especies[:,0])):
                    spamwriter.writerow(Data_Especies[i,:])
        except IOError:
            QtWidgets.QMessageBox.about(self, "ERROR", "Oops! Something is wrong with the file. Try again...")
       
        print("RESULTADOS")    
        try:
            with open(window.CSV_NAME.text() + '_resultados.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile)
                spamwriter.writerow(['GENERACIÓN INICIAL'])
                spamwriter.writerow(['--------------------------------'])
                for i in range(0,N_Especies):
                    spamwriter.writerow([self.Display_Table.item(i, 0).text()] +
                                        ['nan'] +
                                        [self.Display_Table.item(i, 3).text()])
        except IOError:
            QtWidgets.QMessageBox.about(self, "ERROR", "Oops! Something is wrong with the file. Try again...")
                
        print("NICHOS")    
        try:
            with open(window.CSV_NAME.text() + '_nichos.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile)
                spamwriter.writerow(['GENERACIÓN INICIAL'])
                spamwriter.writerow(['--------------------------------'])
                for i in range(0,len(Especies_Nicho[:,0,0])): 
                    spamwriter.writerow(['NICHO ' + str(i)])
                    spamwriter.writerow(['--------------------------------'])
                    for j in range(0,len(Especies_Nicho[0,:,0])):
                        spamwriter.writerow(['ESPECIE ' + str(j)])
                        spamwriter.writerow(Especies_Nicho[i,j,:])
        except IOError:
            QtWidgets.QMessageBox.about(self, "ERROR", "Oops! Something is wrong with the file. Try again...")
        
        f = open("out.txt",'w')
        f.close()
    #def MUT(self):        
        
        
        
    def NEXT(self):
        
        
        global Data_Especies,Especies_Nicho, N_Nichos, Muertes
        for t in range(0,self.GEN_STEP.value()):
            f = open("out.txt",'a')
            
            """
            Asociación agrupación
            Actualmente en orden de índice ( TBU - orden aleatorio )
            Realizar una función para facilitar la lectura
            """
            print(t, file = f)
            print("GENERACIÓN " + str(self.GEN.intValue()), file = f)
            print("--------------------------------------------------------------------------------------------", file = f)
            """
            Muertes
            0 -> SG
            1 -> SI
            """
            
            Eficacia = numpy.zeros((N_Nichos,N_Especies,4))
            E_Total = 0
            
            self.Actual.setText("ASOCIACIÓN/AGRUPACIÓN")
            print(Especies_Nicho, file = f)
            for i in range(0,N_Nichos):
                self.progressBar.setValue((i/N_Nichos)*100)
                
                order1 = ACF.random_order(Especies_Nicho[i,:,:])
                temp_sin_asociar = Especies_Nicho[i,:,0].copy()
                k = 0
                print("AGR", file = f)
                if len(order1) > 0:
                    while k < len(order1):
                        j = int(order1[k] / 10)
                        #print(j)
                        #if randint(0, 100) * Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]) <= Data_Especies[j,5]:
                        if Data_Especies[j,3] != -1 and temp_sin_asociar[j] > 0:
                            if Muertes[i,j,1] == 0 and Muertes[i,j,0] == 0:
                                print("")
                            else:
                                
                                print('NICHO {0} and ESPECIE{1}'.format(i, j), file = f)
                                R = randint(0, 100)
                                print(R * Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]), file = f)
                                if R * Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]) <= Data_Especies[j,5]: #Agrupación 
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
                                    if temp_sin_asociar[j] != 1:
                                        Especies_Nicho[i,j,3] += 1
                                        temp_sin_asociar[j] -= 1
                                        Especies_Nicho[i,int(Data_Especies[j,2]),3] += 1 
                                        Especies_Nicho[i,int(Data_Especies[j,2]),0] -= 1
                                        temp_sin_asociar[int(Data_Especies[j,2])] -= 1
                                        Especies_Nicho[i,j,0] -= 1 
                        
                        k = k +1
                
                
                
                
                
                
                
                
                
                
                """
                temp_sin_asociar = Especies_Nicho[i,:,0].copy()
                #print("TEMPORAL")
                #print(str(temp_sin_asociar))
                for j in range(0,N_Especies):
                    
                    if Data_Especies[j,3] != -1 and temp_sin_asociar[j] >= 0 and (Data_Especies[j,6] == 0 or Data_Especies[j,5] >= int(window.Deaths.toPlainText())): #Agrupación                
                    
                        if temp_sin_asociar[int(Data_Especies[j,3])]-Especies_Nicho[i,j,0] >= 0:
                            Especies_Nicho[i,int(Data_Especies[j,7]),0] = Especies_Nicho[i,int(Data_Especies[j,7]),0] + Especies_Nicho[i,j,0]
                            
                            Especies_Nicho[i,int(Data_Especies[j,3]),0] = temp_sin_asociar[int(Data_Especies[j,3])] - Especies_Nicho[i,j,0]
                            temp_sin_asociar[int(Data_Especies[j,3])] = temp_sin_asociar[int(Data_Especies[j,3])] - Especies_Nicho[i,j,0]
                            
                            Especies_Nicho[i,j,0] = 0
                            temp_sin_asociar[j] = 0
                        else:
                            Especies_Nicho[i,int(Data_Especies[j,7]),0] = Especies_Nicho[i,int(Data_Especies[j,7]),0] + temp_sin_asociar[int(Data_Especies[j,3])]
                            Especies_Nicho[i,int(Data_Especies[j,3]),0] = 0
                            Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - temp_sin_asociar[int(Data_Especies[j,3])]
                            temp_sin_asociar[j] = Especies_Nicho[i,j,0]
                            temp_sin_asociar[int(Data_Especies[j,3])] = 0
                    else:
                        #REVISAR
                        Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] + Especies_Nicho[i,j,2]
                        Especies_Nicho[i,int(Data_Especies[j,3]),0] = Especies_Nicho[i,int(Data_Especies[j,3]),0] + Especies_Nicho[i,j,2]
                        Especies_Nicho[i,j,2] = 0
                
                for j in range(0,N_Especies):
                    
                    if Data_Especies[j,2] != -1 and temp_sin_asociar[j] >= 0: #Asociación
                        if temp_sin_asociar[int(Data_Especies[j,2])]-Especies_Nicho[i,j,0] >= 0:
                            Especies_Nicho[i,j,1] = Especies_Nicho[i,j,1] + Especies_Nicho[i,j,0]
                            temp_sin_asociar[j] = 0
                            Especies_Nicho[i,int(Data_Especies[j,2]),2] = Especies_Nicho[i,int(Data_Especies[j,2]),2] + Especies_Nicho[i,j,0]
                            Especies_Nicho[i,int(Data_Especies[j,2]),0] = Especies_Nicho[i,int(Data_Especies[j,2]),0] - Especies_Nicho[i,int(Data_Especies[j,2]),2]
                            temp_sin_asociar[int(Data_Especies[j,2])] = temp_sin_asociar[int(Data_Especies[j,2])] - Especies_Nicho[i,j,0]
                            Especies_Nicho[i,j,0] = 0
                        else:
                            Especies_Nicho[i,j,1] = Especies_Nicho[i,j,1] + temp_sin_asociar[int(Data_Especies[j,2])]
                            Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - temp_sin_asociar[int(Data_Especies[j,2])]
                            Especies_Nicho[i,int(Data_Especies[j,2]),2] = Especies_Nicho[i,int(Data_Especies[j,2]),2] + temp_sin_asociar[int(Data_Especies[j,2])]
                            Especies_Nicho[i,int(Data_Especies[j,2]),0] = Especies_Nicho[i,int(Data_Especies[j,2]),0] - Especies_Nicho[i,int(Data_Especies[j,2]),2]
                            temp_sin_asociar[j] = Especies_Nicho[i,j,0]
                            temp_sin_asociar[int(Data_Especies[j,2])] = 0
                    
                    #print("TEMPORAL_ESPECIE")
                    #print(str(temp_sin_asociar))
                    #print(str(Especies_Nicho))
                """
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
            T = numpy.zeros((N_Especies))
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
            
            
            for i in range(0,N_Nichos):
                #print(i)
                self.progressBar.setValue((i/N_Nichos)*100)
                o = len(order) - 1
                k = window.Deaths.value()/100 * Especies_Nicho[i,:,:].sum(axis = 0).sum()
                k = math.ceil(k)
                
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
                while o >= 0 and k > 0: # actores y reciprocos
                    if Data_Especies[order[o],8] != -2:
                        no_zero = numpy.nonzero(Especies_Nicho[i,order_if[o],2:])
                        while len(no_zero[0]) != 0 and k > 0:
                            Random = randint(0, len(no_zero[0])-1)
                            if Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] >= k:
                                Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] = Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] - k
                                Muertes[i,order_if[o],0] += k
                                k = 0
                            else:
                                k = k - Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2]
                                Muertes[i,order_if[o],0] += Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2]
                                Especies_Nicho[i,order[o],no_zero[0][Random] + 2] = 0
                            no_zero = numpy.nonzero(Especies_Nicho[i,order_if[o],2:])
                    if k > 0:
                        o = o - 1
                """       
                o = len(order) - 1  
                while o >= 0 and k > 0: #individuos y recipientes agrupados
                    if Data_Especies[order[o],8] != -1:
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
                while o >= 0 and k > 0: # actores y reciprocos agrupados
                    if Data_Especies[order[o],8] != -1:
                        no_zero = numpy.nonzero(Especies_Nicho[i,order_if[o],2:])
                        while len(no_zero[0]) != 0 and k > 0:
                            Random = randint(0, len(no_zero[0])-1)
                            if Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] >= k:
                                Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] = Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] - k
                                Muertes[i,order_if[o],0] += k
                                k = 0
                            else:
                                k = k - Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2]
                                Muertes[i,order_if[o],0] += Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2]
                                Especies_Nicho[i,order[o],no_zero[0][Random] + 2] = 0
                            no_zero = numpy.nonzero(Especies_Nicho[i,order_if[o],2:])
                    if k > 0:
                        o = o - 1
                """
                        
                    
            #k = window.Deaths.Value() * Especies_Nicho[:,:,:].sum(axis = 0).sum()            

            
                
            
            #while 
            
            #if self.GEN.intValue() > 1:
                
                #if numpy.argmax(Data_Especies[:,0]) == j:
                #            Especies_Nicho[i,j,k] = int(Especies_Nicho[i,j,k]*(100-int(window.Deaths.toPlainText()))/100)
            
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
            for i in range(0, N_Nichos):
                self.progressBar.setValue((i/N_Nichos)*100)
                for j in range(0, N_Especies):
                    if Data_Especies[j,8] != -1:    
                        for l in range(0, Especies_Nicho[i,j,0]):
                            #if Muertes[i,j,0] > 0 and Data_Especies[int(Data_Especies[int(Data_Especies[j,8]),3]),4] < Data_Especies[int(Data_Especies[j,8]),0] and randint(0, 100) < Data_Especies[j,5]:
                            if Muertes[i,j,1] == 0 and Muertes[i,j,1] == 0:
                                Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - 1
                                Especies_Nicho[i,int(Data_Especies[j,8]),0] = Especies_Nicho[i,int(Data_Especies[j,8]),0] + 1
                                Especies_Nicho[i,int(Data_Especies[int(Data_Especies[j,8]),3]),0] = Especies_Nicho[i,int(Data_Especies[int(Data_Especies[j,8]),3]),0] + 1
                            elif randint(0, 100) * Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]) <= Data_Especies[j,5]:
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
                

            
            for i in range(0,N_Especies):
                # Display species
                for j in range(0, N_Nichos):
                    ACF.change_item(self.Display_Table,i,j+4,str(Especies_Nicho[j,i,0]))
                ACF.change_item(self.Display_Table,i,3,str(Especies_Nicho[:,i,:].sum(axis = 1).sum()))
                ACF.change_item(self.Display_Table,i,1,str(Muertes.sum(axis = 0)[i,1]/Muertes.sum(axis = 0)[i].sum(axis = 0)))
                
                    
                ACF.change_item(self.Display_Table,i,2,str(T[i]))
                # Potencial biótico
                """
                if Data_Especies[i,2] == -1:  #direct fitness + Indirect fitness del asociado
                    
                    Temp = Data_Especies[i,0] * float(self.Display_Table.item(i,3).text()) # Falta el multiplicador
                    Temp_Acc = Data_Especies[i,0] * float(self.Display_Table.item(i,2).text()) # Falta el multiplicador
                else:
                    Temp = (Data_Especies[i,0] + Data_Especies[int(Data_Especies[i,2]),4]) * float(self.Display_Table.item(i,3).text()) # Falta el multiplicador
                    Temp_Acc = (Data_Especies[i,0] + Data_Especies[int(Data_Especies[i,2]),4]) * float(self.Display_Table.item(i,2).text()) # Falta el multiplicador
                """
                #ACF.change_item(self.Display_Table,i,1,str(Temp)) #Actual
                #ACF.change_item(self.Display_Table,i,2,str(Temp_Acc)) #Accumulado
                
            ACF.refresh_total(self.Display_Table, N_Nichos, N_Especies, Especies_Nicho)
            self.Actual.setText("")
            self.progressBar.setValue(0)
            
            app.processEvents()
            
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
        
        ACF.new_row(self.Data_Table, self.Data_Table.rowCount())
        
        self.Data_Table.cellChanged.connect(self.data_modified)
        
        self.Start_Button.clicked.connect(self.Start)
        self.Load_Button.clicked.connect(self.Load)
        self.Save_Button.clicked.connect(self.Save)
        self.EXIT_Button.clicked.connect(self.EXIT)
       
    def data_modified(self):
        self.Data_Table.cellChanged.disconnect(self.data_modified)
        if self.Data_Table.currentColumn() == 0:
            if self.Data_Table.item(self.Data_Table.currentRow(),self.Data_Table.currentColumn()).text():
                if self.Data_Table.currentRow() == self.Data_Table.rowCount() - 1:
                    ACF.new_row(self.Data_Table, self.Data_Table.rowCount())
                    
            else:
                if self.Data_Table.currentRow() != 0:
                    print("NO")
        elif self.Data_Table.currentColumn() == 1:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un número entero positivo")
                ACF.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
                
        elif self.Data_Table.currentColumn() == 2:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un número entero positivo")
                ACF.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
                
        elif self.Data_Table.currentColumn() == 3:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un número entero positivo")
                ACF.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
        elif self.Data_Table.currentColumn() == 6: 
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un número entero positivo")  
                ACF.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
        
        elif self.Data_Table.currentColumn() == 4:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text():
                found = False
                for i in range(0,self.Data_Table.rowCount() - 1):
                    if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text() == self.Data_Table.item(i, 0).text():
                        found = True
                        break
                if found == False:
                    QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un nombre de especie que ya exista")
                    ACF.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
        elif self.Data_Table.currentColumn() == 5:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text():
                found = ACF.find_item(self.Data_Table, self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text())
                if found == -1:
                    QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un nombre de especie que ya exista")
                    ACF.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                    
                else:
                    if self.Data_Table.item(self.Data_Table.currentRow(), 3).text() and self.Data_Table.item(found, 3).text():
                        nombre = self.Data_Table.item(self.Data_Table.currentRow(), 0).text() + "(" + self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text() + ")"
                        
                        final = self.Data_Table.rowCount() - 1
                        ACF.new_row(self.Data_Table, final)
                         
                        ACF.change_item(self.Data_Table,final,0,nombre)
                        ACF.change_item(self.Data_Table,final,1,"0")
                        found = ACF.find_item(self.Data_Table, self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text())
                        ACF.change_item(self.Data_Table,final,2,self.Data_Table.item(found, 3).text())
                        ACF.change_item(self.Data_Table,final,3,self.Data_Table.item(self.Data_Table.currentRow(), 2).text())
                        ACF.change_item(self.Data_Table,final,6,self.Data_Table.item(self.Data_Table.currentRow(), 6).text())
                        
                        
                        
                        
                        
                        
                    elif self.Data_Table.item(found, 3).text():
                        QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un indirect fitness en el recipiente")
                        ACF.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                        
                    else:
                        QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un indirect fitness en el actor")
                        ACF.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())

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
        self.dialog = Sim() 
        self.dialog.show()
        
    def Load(self):
        print("LOAD")
        try:
            with open(self.CSV_NAME.text() + '.csv', 'r', newline='') as csvfile:
                spamreader = csv.reader(csvfile)
                self.Data_Table.setRowCount(0)
                ACF.new_row(self.Data_Table, self.Data_Table.rowCount())
                i = 0
                for row in spamreader:
                    if i == 0:
                        self.Nodes.setValue(int(row[7]))
                        self.Resources.setValue(int(row[8]))
                        self.Reproduction.setValue(int(row[9]))
                        self.Deaths.setValue(int(row[10]))
                    ACF.change_item(self.Data_Table,i,0,row[0])
                    ACF.change_item(self.Data_Table,i,1,row[1])
                    ACF.change_item(self.Data_Table,i,2,row[2])
                    ACF.change_item(self.Data_Table,i,3,row[3])
                    ACF.change_item(self.Data_Table,i,4,row[4])
                    ACF.change_item(self.Data_Table,i,5,row[5])
                    ACF.change_item(self.Data_Table,i,6,row[6])
                    ACF.new_row(self.Data_Table, self.Data_Table.rowCount())
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
    
    