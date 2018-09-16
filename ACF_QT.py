# -*- coding: utf-8 -*-

"""
Automata Celular Qt Functions
v0.7.2
@author: Carlos Villagrasa Guerrero
"""

import os
import csv
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import math
import ACF, ACF_FILE
from random import randint, shuffle
import numpy
import matplotlib.pyplot as plt #for plot

qtMain = "AUTOMATA_CELULAR.ui" # Main window file
qtSimulation = "SIMULATION.ui" # Simulation window file

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtMain)
Ui_SimWindow, QtBaseClass = uic.loadUiType(qtSimulation)

def change_item(Data_Table, x, y, text):
    """
    change_item(Data_Table, x, y, text)
    Description:
        -This function changes the text from one cell of the data table
    Input:
        -Data_Table: QT table handler
        -x, y: Position of the item to be changed
        -text: string with the text to be writen on the position x, y
    """
    item = QtWidgets.QTableWidgetItem()           
    item.setText(text)
    Data_Table.setItem(x, y, item)    
    
def new_row(Data_Table, row):
    """
    new_row(Data_Table, row)
    Description:
        -This function creates a new row on the data table
    Input:
        -Data_Table: QT table handler
        -row: Index for the new row
    """
    Data_Table.insertRow(row)

    for i in range(0, 8):
        change_item(Data_Table,row,i,"0")
        change_item(Data_Table,row,i,"")
    
def find_item(Data_Table, nombre):
    """
    find_item(Data_Table, nombre)
    Description:
        -This function finds the first row where there is a name and returns it
    Input:
        -Data_Table: QT table handler
        -nombre: Name to be found
    Output:
        -row: Index where the name was found
    """
    for i in range(0,Data_Table.rowCount() - 1):
        if nombre == Data_Table.item(i, 0).text():
            return i
    return -1

def delete_item(Data_Table, x, y):
    """
    delete_item(Data_Table, x, y)
    Description:
        -This function delete the text of a cell in a position
    Input:
        -Data_Table: QT table handler
        -x, y: Position of the item to be deleted
    """    
    item = QtWidgets.QTableWidgetItem()   
    nombre = ""        
    item.setText(nombre)
    Data_Table.setItem(x, y, item)
    
def update_table(Display_Table, Especies_Nicho, Muertes, N_Nichos, N_Especies):
    """
    update_table(Display_Table, Especies_Nicho, Muertes, N_Nichos, N_Especies)
    Description:
        -This function updates the table with the lastest data 
    Input:
        -Display_Table: QT table handler
        -Especies_Nicho: Array with all the individuals and its positions on the nodes
        -Muertes: Array with all the deaths on a generation
        -N_Nichos: Number of nodes
        -N_Especies: Number of species
    """

    for i in range(0,N_Especies):

        for j in range(0, N_Nichos):
            change_item(Display_Table,i,j+2,str(Especies_Nicho[j,i,0]))

        change_item(Display_Table,i,1,str(Especies_Nicho[:,i,:].sum(axis = 1).sum()))
  
    change_item(Display_Table,N_Especies,0,"Total")

    for i in range(0,N_Nichos):
        change_item(Display_Table,N_Especies,i + 2,str(Especies_Nicho[i,:,:].sum(axis = 0).sum()))
    change_item(Display_Table,N_Especies,1,str(Especies_Nicho[:,:,:].sum(axis = 0).sum()))

def potential(Display_Table, Data_Especies, N_Especies):
    """
    potential(sim, Data_Especies, N_Especies)
    Description:
        -This function updates the table with the lastest potential value (DEPRECATED) 
    Input:
        -Display_Table: QT table handler
        -Data_Especies: Array with data for the species
        -N_Especies: Number of species
    """
    for i in range(0,N_Especies):
        # Potencial biótico
        
        if Data_Especies[i,2] == -1:  #direct fitness + Indirect fitness del asociado
            Temp = Data_Especies[i,0] * Data_Especies[i,1] # Falta el multiplicador
        else:
            Temp = (Data_Especies[i,0] + Data_Especies[int(Data_Especies[i,2]),4]) * Data_Especies[i,1] # Falta el multiplicador
        change_item(Display_Table, i, 1, str(Temp)) #actual
        change_item(Display_Table, i, 2, str(Temp)) #acumulado       
        
def read_data_from_qt(window, sim):
    """
    read_data_from_qt(window, sim)
    Description:
        -This function reads and write data from the Qt GUI
    Input:
        -window: Main window handler
        -sim: Simulation window handler
    Output:
        -Data_Especies: 2D array with all the data from the species
        -N_Nichos: Number of nodes
        -N_Especies: Number of species
        -Deaths: % of group selection deaths
        -Reproduction: % of proportion between consumption and reproduction
        -Resources: Quantity of resources on each generation/step
    """
    Names = []
    N_Especies = window.Data_Table.rowCount() - 1
    N_Nichos = window.Nodes.value()
    Deaths = window.Deaths.value()
    Reproduction = window.Reproduction.value()
    Resources = window.Resources.value()
    Lambda = window.Lambda.value()
    
    #Adjust table to number of species
    sim.Display_Table.setRowCount(N_Especies + 1)
    
    #Set matrix for data of the species
    Data_Especies = numpy.zeros((N_Especies, 9))
        
    for i in range(0,N_Especies):
        Data_Especies[i,8] = -1
        Data_Especies[i,6] = -1
            
    #Get data for the species
    for i in range(0,N_Especies):
        #Set name on the table
         
        change_item(sim.Display_Table,i,0,window.Data_Table.item(i,0).text())
         
        Names.append(window.Data_Table.item(i,0).text())

        Data_Especies[i,1] = int(window.Data_Table.item(i,1).text())    #Catidad inicial
        Data_Especies[i,0] = int(window.Data_Table.item(i,2).text())    #direct fitness
        Data_Especies[i,4] = int(window.Data_Table.item(i,3).text())    #indirect fitness

        if window.Data_Table.item(i,6).text(): #flexibility
            Data_Especies[i,5] = int(window.Data_Table.item(i,6).text())    
        else:
            Data_Especies[i,5] = 0
            
        if window.Data_Table.item(i,4).text(): #Asociación
            Data_Especies[i,2] = find_item(window.Data_Table, window.Data_Table.item(i,4).text())
        else:
            Data_Especies[i,2] = -1

        if window.Data_Table.item(i,5).text(): #Agrupación
            #compañero
            Data_Especies[i,3] = find_item(window.Data_Table, window.Data_Table.item(i,5).text())
            #destino de agrupación
            Data_Especies[i,7] = find_item(window.Data_Table, window.Data_Table.item(i,0).text() + "(" + window.Data_Table.item(i,5).text() + ")")
            #origen de agrupación
            Data_Especies[int(Data_Especies[i,7]),8] = i
        else:
            Data_Especies[i,3] = -1
            Data_Especies[i,7] = -1
       
        
        
    sim.Display_Table.setColumnCount(N_Nichos + 2)

    for i in range(0,N_Nichos):
        sim.Display_Table.setHorizontalHeaderItem(i + 2, QtWidgets.QTableWidgetItem("Nicho " + str(i + 1)))
  
    return [Names, Data_Especies, N_Nichos, N_Especies, Deaths, Reproduction, Resources, Lambda]

class Sim(QtWidgets.QMainWindow, Ui_SimWindow):
    """
    Class Sim
    Description:
    -This class manages everything for the simulation window GUI
    """
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
    Especies_Nicho
    0->Individuals
    1->Asociation receptors
    2->Asociation actors
    3->Reciprocal asociation
    """
    """
    Muertes
    0->Group selection deaths
    1->Individual selection deaths
    """
    global Data_Especies, Especies_Nicho, N_Nichos, N_Especies, Muertes, window, Names
    
    def __init__(self, parent):
        """
        Simulation window inicialization
        """
        super().__init__()

        #Set UI
        self.setupUi(self)
        global Data_Especies, Especies_Nicho, N_Nichos, N_Especies, Muertes, Deaths, Reproduction, Resources, window, Historic, Names, Sim_name, Egoismo_Relativo, Lambda
        
        window = parent
        Sim_name = window.CSV_NAME.text()
        
        

        #Get input Data and set Qt window for simulation
        [Names, Data_Especies, N_Nichos, N_Especies, Deaths, Reproduction, Resources, Lambda] = read_data_from_qt(window, self)

        #Initialize Deaths array and Species array
        Muertes = numpy.zeros((N_Nichos, N_Especies, 2))
        Especies_Nicho = numpy.zeros((N_Nichos, N_Especies, 4), dtype=numpy.int)

        #Initial setup for species
        Especies_Nicho = ACF.inicial_set(Data_Especies, N_Nichos, N_Especies, Especies_Nicho) 
        
        update_table(self.Display_Table, Especies_Nicho, Muertes, N_Nichos, N_Especies)

        """
        Deprecated
        ACF_QT.potential(self, Data_Especies, N_Especies)
        """
        
        #Current generation
        self.GEN.display(1)
        
        #Buttons setup
        self.NEXT_Button.clicked.connect(self.NEXT)
        self.MUT_Button.clicked.connect(self.MUT)

        #Write initial data 
        ACF_FILE.data_write(window.CSV_NAME.text(), Data_Especies, Especies_Nicho, N_Especies, 'w')
        
        #Greed calculation
        Egoismo_Relativo = ACF.greed_calc(Especies_Nicho, Data_Especies, N_Nichos, N_Especies)

        #Initialize Historic data
        Historic = [[] for _ in range(7)]
        Historic[0].append(Names)
        Historic[1].append(Data_Especies)
        Historic[2].append(Especies_Nicho)
        Historic[3].append([]) #Individual selective pressure
        Historic[4].append(Egoismo_Relativo) #Greed
        Historic[5].append([]) #Species quantity for Greed
        Historic[6].append([]) #Deaths

        #Output files for data checking
        f = open("out.txt",'w')
        f.close()
        
    def MUT(self):
        """
        Mutation button behaviour
        """
        global window

        window.Continue_Button.setEnabled(True)
        window.Nodes.setEnabled(True)
        window.Resources.setEnabled(True)
        window.Reproduction.setEnabled(True)
        window.Deaths.setEnabled(True)
        window.Data_Table.setEnabled(True)
        #Reset initial quantity for each specie
        for i in range(0,N_Especies):
            change_item(window.Data_Table,i,1,"0") 
        
        self.hide()
        window.show()
        
    def MUT_Changes(self):
        """
        Mutation return behaviour
        """
        global Data_Especies,Especies_Nicho, N_Nichos, N_Especies, Muertes, Deaths ,Reproduction, Resources, window, Names, Egoismo_Relativo
        
        [Names, Data_Especies, N_Nichos, N_Especies, Deaths, Reproduction, Resources] = read_data_from_qt(window, self)

        #Greed calculation
        Egoismo_Relativo = ACF.greed_calc(Especies_Nicho, Data_Especies, N_Nichos, N_Especies)

        Especies_Nicho = ACF.resize_matrix_3d(Especies_Nicho, N_Nichos, N_Especies)
        Muertes = ACF.resize_matrix_3d(Muertes, N_Nichos, N_Especies)
        
        #Generación inicial de los nuevos seres
        Especies_Nicho = ACF.inicial_set(Data_Especies, N_Nichos, N_Especies, Especies_Nicho) 

        update_table(self.Display_Table, Especies_Nicho, Muertes, N_Nichos, N_Especies)    

        ACF_FILE.data_write(window.CSV_NAME.text(), Data_Especies, Especies_Nicho, N_Especies, 'a')
        
    def NEXT(self):
        """
        Next button behaviour
        """
        global Data_Especies,Especies_Nicho, N_Nichos, Muertes, Deaths, Reproduction, Resources, Graphic_greed, Historic, Names, Sim_name, Egoismo_Relativo, Lambda
        for t in range(0,self.GEN_STEP.value()):
            f = open("out.txt",'a')

            print(t, file = f)
            print("GENERACIÓN " + str(self.GEN.intValue()), file = f)
            print("--------------------------------------------------------------------------------------------", file = f)
            
            """
            Aggrupation/Association
            """
            self.Actual.setText("ASOCIACIÓN/AGRUPACIÓN")
            print(Especies_Nicho, file = f)
            print("AGR", file = f)
            print("ASO", file = f)

            for i in range(0,N_Nichos):
                self.progressBar.setValue((i/N_Nichos)*100)
                
                Especies_Nicho[i,:,:] = ACF.node_agrupation(Especies_Nicho[i,:,:], Data_Especies, N_Especies)
                        
                Especies_Nicho[i,:,:] = ACF.node_asociation(Especies_Nicho[i,:,:],  Muertes[i,:,:], Data_Especies)
                
            print("FIN DE ASO/AGR", file = f)
            print(Especies_Nicho, file = f) 

            """
            Greed calculation
            """
            Egoismo_Especies = Especies_Nicho.copy()

            #Greed calculation
            Egoismo_Relativo = ACF.greed_calc(Especies_Nicho, Data_Especies, N_Nichos, N_Especies)

            print("GREED", file = f)
            print(Egoismo_Especies, file = f)
            print(Egoismo_Relativo, file = f)

            """
            Group selection
            """
            """
            self.Actual.setText("SELECCIÓN DE GRUPO")

            #Resets deaths for this generation
            Muertes = numpy.zeros((N_Nichos,N_Especies,2))
            
            for i in range(0,N_Nichos):
                #Order by greed
                order = numpy.dstack(numpy.unravel_index(numpy.argsort(Egoismo_Relativo[i,:,:].ravel()), (N_Especies, 4)))
     
                print(order, file = f)

                order = ACF.reorder_Greed(order, Egoismo_Relativo[i,:,:])
                
                print("reordenado", file = f)   
                print(order, file = f) 
                self.progressBar.setValue((i/N_Nichos)*100)
                [Especies_Nicho[i,:,:], Muertes[i,:,:]] = ACF.node_GS_Greed(order, Especies_Nicho[i,:,:], Muertes[i,:,:], Deaths)
            """
            self.Actual.setText("SELECCIÓN DE GRUPO")

            #Resets deaths for this generation
            Muertes = numpy.zeros((N_Nichos,N_Especies,2))
            
            for i in range(0,N_Nichos):
                
                self.progressBar.setValue((i/N_Nichos)*100)
                [Especies_Nicho[i,:,:], Muertes[i,:,:]] = ACF.node_GS(Especies_Nicho[i,:,:], Muertes[i,:,:], Deaths, Egoismo_Relativo[i,:,:], Lambda, N_Especies)



            print("FIN DE SG", file = f)
            print(Especies_Nicho, file = f)

            """
            Individual selection
            """
            self.Actual.setText("SELECCIÓN DE INDIVIDUAL")
            if Reproduction != 0:
                for i in range(0,N_Nichos):
                    self.progressBar.setValue((i/N_Nichos)*100)

                    [Especies_Nicho[i,:,:], Muertes[i,:,:]] = ACF.node_consumption(Especies_Nicho[i,:,:], Resources, Data_Especies, N_Especies, Muertes[i,:,:], Reproduction)
                
            print("FIN DE SI", file = f)
            print(Especies_Nicho, file = f)

            """
            Reproduction
            """
            self.Actual.setText("REPRODUCCIÓN")
            for i in range(0, N_Nichos):
                self.progressBar.setValue((i/N_Nichos)*100)
                Especies_Nicho [i,:,:] = ACF.node_reproduction(Especies_Nicho[i,:,:], Data_Especies, N_Especies)

            print("FIN DE REPRODUCCIÓN", file = f)
            print(Especies_Nicho, file = f)

            self.Actual.setText("FLEXIBILIDAD")
            for i in range(0, N_Nichos):
                self.progressBar.setValue((i/N_Nichos)*100)

                Especies_Nicho [i,:,:] = ACF.node_flexibility(Especies_Nicho[i,:,:], Data_Especies, N_Especies)

            print("FIN DE FLEXIBILIDAD", file = f)
            print(Especies_Nicho, file = f)    
            
            self.Actual.setText("FINISHING")
            self.progressBar.setValue(99)

            Especies_Nicho = ACF.distribution(Especies_Nicho, N_Nichos,N_Especies)

            print("FIN DE REPARTO", file = f)
            print(Especies_Nicho, file = f)
            print("MUERTES", file = f)
            print(Muertes, file = f) 

            update_table(self.Display_Table, Especies_Nicho, Muertes, N_Nichos, N_Especies)
            
            self.Actual.setText("FINISHING")
            self.progressBar.setValue(99)

            """
            Individual selection pressure
            """
            P = ACF.IS_pressure(Egoismo_Especies, Muertes, N_Especies, N_Nichos)

            """
            On the fly graphic representation
            """
            if self.Graph_Check.isChecked():
                plt.ion()
                plt.show()
                self.Actual.setText("GRÁFICO")
                gen = self.GEN.intValue()
                
                # create data
                x = numpy.zeros(N_Nichos*N_Especies*4)
                y = numpy.zeros(N_Nichos*N_Especies*4)
                z = numpy.zeros(N_Nichos*N_Especies*4)
                c = numpy.zeros(N_Nichos*N_Especies*4)

                for i in range(0,N_Nichos):
                    self.progressBar.setValue((i/N_Nichos)*100)
                    for j in range(0,N_Especies):
                        for k in range(0,4):

                            if ((Muertes[i,j,0]+Muertes[i,j,1]) == 0):
                                x[i*N_Especies*4 + j*4 + k] = 50

                            else:

                                x[i*N_Especies*4 + j*4 + k] = P[i] * 100
                            y[i*N_Especies*4 + j*4 + k] = Egoismo_Relativo[i,j,k] * 100 
                            z[i*N_Especies*4 + j*4 + k] = Egoismo_Especies[i,j,k]
                            c[i*N_Especies*4 + j*4 + k] = j

                plt.figure("Graphic")
                plt.clf()
                # Change color with c and alpha. I map the color to the X axis value.
                plt.scatter(x, y, s=z, c=c, cmap=plt.cm.jet, alpha=0.4, edgecolors="grey", linewidth=2)
                
                # Add titles (main and on axis)
                plt.xlabel("Individual pressure [%]")
                plt.ylabel("Greed [%]")
                plt.xlim([-10,110])
                plt.ylim([-10,110])
                plt.colorbar(cmap=plt.cm.jet)
                plt.title('Relative graphic representation {0}'.format(gen))

                plt.pause(0.001) 

            Historic[0].append(Names) #Names
            Historic[1].append(Data_Especies) #Actual data
            Historic[2].append(Especies_Nicho) #Species on each node
            Historic[3].append(P) #Individual selective pressure (DEATHS)
            Historic[4].append(Egoismo_Relativo) #Greed
            Historic[5].append(Egoismo_Especies) #Species quantity for Greed
            Historic[6].append(Muertes) #Species quantity for Greed 
            
            ACF_FILE.bubbles_write(Historic, Sim_name, N_Especies, N_Nichos)

            print("FIN")
            self.Actual.setText("")
            self.progressBar.setValue(0)
            self.GEN.display(self.GEN.intValue() + 1)
            
            f.close()
        #self.GEN.display(self.GEN.intValue() + self.GEN_STEP.value())
        plt.show(block = True)  
        
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Class MyApp
    Description:
    -This class manages everything for the main window GUI
    """
    def __init__(self, parent=None):
        """
        Inicialization
        """
        QtWidgets.QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        new_row(self.Data_Table, self.Data_Table.rowCount())
        
        self.Data_Table.cellChanged.connect(self.data_modified)
        
        self.Start_Button.clicked.connect(self.Start)
        self.Continue_Button.clicked.connect(self.Continue)
        self.Load_Button.clicked.connect(self.Load)
        self.Save_Button.clicked.connect(self.Save)
        self.EXIT_Button.clicked.connect(self.EXIT)
        self.Reset_Button.clicked.connect(self.Reset)
       
    def data_modified(self):
        """
        Change item behaviour
        """
        self.Data_Table.cellChanged.disconnect(self.data_modified)
        if self.Data_Table.currentColumn() == 0:
            if self.Data_Table.item(self.Data_Table.currentRow(),self.Data_Table.currentColumn()).text():
                if self.Data_Table.currentRow() == self.Data_Table.rowCount() - 1:
                    new_row(self.Data_Table, self.Data_Table.rowCount())
                    
            else:
                if self.Data_Table.currentRow() != 0:
                    print("NO")
        elif self.Data_Table.currentColumn() == 1:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un número entero positivo")
                delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
                
        elif self.Data_Table.currentColumn() == 2:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un número entero positivo")
                delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
                
        elif self.Data_Table.currentColumn() == 3:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Tenga en cuenta que el fitness resultante debe ser positivo para el correcto funcionamiento de la simulación")
                #ACF_QT.delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
        elif self.Data_Table.currentColumn() == 6: 
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text().isdigit() != True:
                QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un número entero positivo")  
                delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
        
        elif self.Data_Table.currentColumn() == 4:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text():
                found = False
                for i in range(0,self.Data_Table.rowCount() - 1):
                    if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text() == self.Data_Table.item(i, 0).text():
                        found = True
                        break
                if found == False:
                    QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un nombre de especie que ya exista")
                    delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                
        elif self.Data_Table.currentColumn() == 5:
            if self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text():
                found = find_item(self.Data_Table, self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text())
                if found == -1:
                    QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un nombre de especie que ya exista")
                    delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                    
                else:
                    if self.Data_Table.item(self.Data_Table.currentRow(), 3).text() and self.Data_Table.item(found, 3).text():
                        nombre = self.Data_Table.item(self.Data_Table.currentRow(), 0).text() + "(" + self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text() + ")"
                        
                        final = self.Data_Table.rowCount() - 1
                        new_row(self.Data_Table, final)
                         
                        change_item(self.Data_Table,final,0,nombre)
                        change_item(self.Data_Table,final,1,"0")
                        found = find_item(self.Data_Table, self.Data_Table.item(self.Data_Table.currentRow(), self.Data_Table.currentColumn()).text())
                        change_item(self.Data_Table,final,2,self.Data_Table.item(found, 3).text())
                        change_item(self.Data_Table,final,3,self.Data_Table.item(self.Data_Table.currentRow(), 2).text())
                        change_item(self.Data_Table,final,6,self.Data_Table.item(self.Data_Table.currentRow(), 6).text())
  
                    elif self.Data_Table.item(found, 3).text():
                        QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un indirect fitness en el recipiente")
                        delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())
                        
                    else:
                        QtWidgets.QMessageBox.about(self, "Title", "Debe introducir un indirect fitness en el actor")
                        delete_item(self.Data_Table,self.Data_Table.currentRow(), self.Data_Table.currentColumn())

                #self.Data_Table.setRowCount(self.Data_Table.rowCount() + 1)
                    
            else:
                if self.Data_Table.currentRow() != 0:
                   print("NO")
                
        self.Data_Table.cellChanged.connect(self.data_modified)
            
    def Start(self):
        """
        Start button behaviour
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
        self.dialog = Sim(self) 
        self.dialog.show()
        
    def Continue(self):
        """
        Continue button behaviour
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
        """
        Reset button behaviour
        """
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
        new_row(self.Data_Table, self.Data_Table.rowCount())
        
        self.dialog.hide()
        
    def Load(self):
        """
        Load button behaviour
        """
        [Names, Data, node, res, rep, sg] = ACF_FILE.Load(self.CSV_NAME.text())
        self.Nodes.setValue(node)
        self.Resources.setValue(res)
        self.Reproduction.setValue(rep)
        self.Deaths.setValue(sg)
        self.Data_Table.setRowCount(0)
        new_row(self.Data_Table, self.Data_Table.rowCount())
        for i in range(0, len(Names)):
            change_item(self.Data_Table,i,0,Names[i])
            change_item(self.Data_Table,i,1,Data[0][i])
            change_item(self.Data_Table,i,2,Data[1][i])
            change_item(self.Data_Table,i,3,Data[2][i])
            change_item(self.Data_Table,i,4,Data[3][i])
            change_item(self.Data_Table,i,5,Data[4][i])
            change_item(self.Data_Table,i,6,Data[5][i])
            new_row(self.Data_Table, self.Data_Table.rowCount())

    def Save(self):
        """
        Save Button behaviour
        """
        Datos = [[] for _ in range(6)]
        Names = []
        for i in range(0,self.Data_Table.rowCount() - 1):
            Names.append(self.Data_Table.item(i, 0).text())
            Datos[0].append(self.Data_Table.item(i, 1).text())
            Datos[1].append(self.Data_Table.item(i, 2).text())
            Datos[2].append(self.Data_Table.item(i, 3).text())
            Datos[3].append(self.Data_Table.item(i, 4).text())
            Datos[4].append(self.Data_Table.item(i, 5).text())
            Datos[5].append(self.Data_Table.item(i, 6).text())

        ACF_FILE.Save(self.CSV_NAME.text(), Names, Datos, 
            self.Nodes.value(), self.Resources.value(), 
            self.Reproduction.value(), self.Deaths.value())
        
    def EXIT(self):
        """
        Exit button behaviour
        """
        QtWidgets.QMessageBox.about(self, "ERROR", "TO EXIT CLICK ON THE X")
