# -*- coding: utf-8 -*-
"""
Automata Celular Main
v0.1.2
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
from random import randint, sample

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
    col5 -> Optimism
    col6 -> Fenotipic flexibility
    col7 -> Agrupation new species
    """
    global Data_Especies,Especies_Nicho, N_Nichos, N_Especies
    
    def __init__(self):
        super().__init__()
        #Set UI
        self.setupUi(self)
        
        global Data_Especies,Especies_Nicho, N_Nichos, N_Especies
        N_Especies = window.Data_Table.rowCount() - 1
        
        """
        # create plot
        plt = pg.plot()
        plt.showGrid(x=True,y=True)
        plt.addLegend()
        """

        #Adjust table to number of species
        self.Display_Table.setRowCount(N_Especies + 1)
        #Set matrix for data of the species
        Data_Especies = numpy.zeros((N_Especies, 8))
        
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
                Data_Especies[i,7] = ACF.find_item(window.Data_Table, window.Data_Table.item(i,0).text() + "_" + window.Data_Table.item(i,5).text())
            else:
                Data_Especies[i,3] = -1
                Data_Especies[i,7] = -1
        
            Data_Especies[i,5] = int(window.Data_Table.item(i,6).text())
            
            if window.Data_Table.item(i,7).text():
                Data_Especies[i,6] = 1
            else:
                Data_Especies[i,6] = 0
           
        #Number of niches?
        N_Nichos = window.Nodes.value()
        """
        Matrix of species
        0->Individuos
        1->Recipientes asociación
        2->Agrupados (TO BE DELETED)
        3->Actores asociación
        """
        
        Especies_Nicho = numpy.zeros((N_Nichos,N_Especies,3))
        
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
        
    #def MUT(self):        
        
        
        
    def NEXT(self):
        global Data_Especies,Especies_Nicho, N_Nichos
        for t in range(0,self.GEN_STEP.value()):
            """
            Asociación agrupación
            Actualmente en orden de índice ( TBU - orden aleatorio )
            Realizar una función para facilitar la lectura
            """
            print(t)
            for i in range(0,N_Nichos):
                
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
            print("FIN DE ASO/AGR")
            #print(str(Especies_Nicho)) 
            
            """
            Selección de grupo
            """
            
            #}Ordenar por la proporción direct fitness/indirect fitness
            

            order = numpy.argsort(Data_Especies[:,0]/Data_Especies[:,4])
            #print("SG")
            for i in range(0,N_Nichos):
                o = len(order) - 1
                k = window.Deaths.value()/100 * Especies_Nicho[i,:,:].sum(axis = 0).sum()
                k = math.ceil(k)
                #print(k)
                while o >= 0 and k > 0:
                    no_zero = numpy.nonzero(Especies_Nicho[i,order[o],:])
                    if len(no_zero[0]) != 0:
                        Random = randint(0, len(no_zero[0])-1)
                        if Especies_Nicho[i,order[o],Random] >= k:
                            Especies_Nicho[i,order[o],Random] = Especies_Nicho[i,order[o],Random] - k
                            k = 0
                        else:
                            k = k - Especies_Nicho[i,order[o],Random]
                            Especies_Nicho[i,order[o],Random] = 0
                    if k > 0:
                        o = o - 1

                        
                    
            #k = window.Deaths.Value() * Especies_Nicho[:,:,:].sum(axis = 0).sum()            

            
                
            
            #while 
            
            #if self.GEN.intValue() > 1:
                
                #if numpy.argmax(Data_Especies[:,0]) == j:
                #            Especies_Nicho[i,j,k] = int(Especies_Nicho[i,j,k]*(100-int(window.Deaths.toPlainText()))/100)
            
            print("FIN DE SG")
            """
            Alimentación
            """

            for i in range(0,N_Nichos):
                
                temp_rec = int(window.Resources.value())
                Feeded = numpy.zeros((N_Especies,3))
                print("NICHO")
                print(int(Especies_Nicho[i,:,:].sum(axis = 0).sum()))
                A = sample(range(1, int(Especies_Nicho[i,:,:].sum(axis = 0).sum()) + 1), int(Especies_Nicho[i,:,:].sum(axis = 0).sum()))
                print(A)
                print(Especies_Nicho[i,:,:])
                j = 0

                while temp_rec > 0 and j < len(A):
                        
                    no_zero = numpy.nonzero(Especies_Nicho[i,:,:])
                    print(no_zero)
                    if len(no_zero[0]) == 0:
                        break
                    k = 0
                    #A = randint(0, Especies_Nicho[i,:,:].sum(axis = 0).sum())
                    T = int(Especies_Nicho[i,no_zero[0][k],no_zero[1][k]])
                    """
                    print("PPP")
                    print(i)
                    print(Especies_Nicho)
                    print(Especies_Nicho[i,:,:].sum(axis = 0).sum())
                    print(no_zero)
                    print(A)
                    print(T)
                    """
                    
                    while A[j] > T:
                        
                        k = k + 1
                        T = T + int(Especies_Nicho[i,no_zero[0][k],no_zero[1][k]])
                        """
                        print("WWWW")
                        print(k)
                        print(A)
                        print(T)
                        """
                    #k = randint(0, len(no_zero[0])-1)
                    print(k)
                    if Especies_Nicho[i,no_zero[0][k],no_zero[1][k]]>0:
                        
                        
                        if no_zero[1][k] == 0: #individual
                            temp_rec = temp_rec - int(Data_Especies[no_zero[0][k],0] * int(window.Reproduction.value())/100)
                        if no_zero[1][k] == 1: #asociación recipiente
                            temp_rec = temp_rec - int(Data_Especies[no_zero[0][k],0] * int(window.Reproduction.value())/100)
                        if no_zero[1][k] == 2: #asociación actor
                            temp_rec = temp_rec - int((Data_Especies[no_zero[0][k],4] + Data_Especies[no_zero[0][k],0]) * int(window.Reproduction.value())/100)
                        if temp_rec >= 0:
                            Feeded[no_zero[0][k],no_zero[1][k]] = Feeded[no_zero[0][k],no_zero[1][k]] + 1
                            #Especies_Nicho[i,no_zero[0][k],no_zero[1][k]] = Especies_Nicho[i,no_zero[0][k],no_zero[1][k]] - 1
                    j = j +1
                Especies_Nicho[i,:,:] = Feeded
                
            print("FIN DE SI")
            #print(Especies_Nicho)
            """
            Reproducción
            
            Mínimo de nichos actualmente 3

            """
            temp_Especies = numpy.zeros((N_Nichos,N_Especies,3))
            for i in range(0, N_Nichos):
                for j in range(0, N_Especies):
                    for k in range(0, 3):
                                            
                        if k == 0:
                            
                            for I in range(0,int(Especies_Nicho[i,j,k]*Data_Especies[j,0])):
                                l = randint(-2, 3)
                                if i + l >= N_Nichos:    
                                    temp_Especies[i + l - N_Nichos,j,k] += 1
                                elif i + l < 0:
                                    temp_Especies[i + l + N_Nichos,j,k] += 1
                                else:
                                    temp_Especies[i + l,j,k] += 1
                                
                        if k == 1 and Data_Especies[j,2] != -1:
                            
                            for I in range(0,int(Especies_Nicho[i,j,k] * (Data_Especies[j,0] + Data_Especies[int(Data_Especies[j,2]),4]))):
                                l = randint(-2, 3)
                                if i + l >= N_Nichos:    
                                    temp_Especies[i + l - N_Nichos,j,0] += 1
                                elif i + l < 0:
                                    temp_Especies[i + l + N_Nichos,j,0] += 1
                                else:
                                    temp_Especies[i + l,j,0] += 1
                                    
                        if k == 2:
                            
                            for I in range(0,int(Especies_Nicho[i,j,k] * Data_Especies[j,0])):
                                l = randint(-2, 3)
                                if i + l >= N_Nichos:    
                                    temp_Especies[i + l - N_Nichos,j,0] += 1
                                elif i + l < 0:
                                    temp_Especies[i + l + N_Nichos,j,0] += 1
                                else:
                                    temp_Especies[i + l,j,0] += 1
            
            Especies_Nicho = temp_Especies
            #print("FIN DE GEN")
            #print(str(Especies_Nicho))
            print("FIN DE REP")
            for i in range(0,N_Especies):
                # Display species
                for j in range(0, N_Nichos):
                    ACF.change_item(self.Display_Table,i,j+4,str(Especies_Nicho[j,i,0]))
                ACF.change_item(self.Display_Table,i,3,str(Especies_Nicho[:,i,:].sum(axis = 1).sum()))
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
            
            #self.GEN.display(self.GEN.intValue() + 1)
        self.GEN.display(self.GEN.intValue() + self.GEN_STEP.value())

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        ACF.new_row(self.Data_Table, self.Data_Table.rowCount())
        
        self.Data_Table.cellChanged.connect(self.data_modified)
        
        self.Start_Button.clicked.connect(self.Start)
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
                    item = QtWidgets.QTableWidgetItem()
                    if self.Data_Table.item(self.Data_Table.currentRow(), 3).text() and self.Data_Table.item(found, 3).text():
                        nombre = self.Data_Table.item(self.Data_Table.currentRow(), 0).text() + "_" + self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text()
                        
                        item.setText(nombre)
                        ACF.new_row(self.Data_Table, self.Data_Table.currentRow() + 1)
                        
                        final = self.Data_Table.currentRow() + 1 
                        self.Data_Table.setItem(final, 0, item)
                        
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
        elif self.Data_Table.currentColumn() == 7:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text() != "x" and self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text():
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir una x o nada")
                ACF.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                #item = self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                #item.setText("X")
                
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
    
    