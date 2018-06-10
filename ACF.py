# -*- coding: utf-8 -*-
"""
Automata Celular Functions
v0.4.1
@author: Carlos Villagrasa Guerrero
"""

import numpy
import ACF_QT
from random import randint, shuffle
from PyQt5 import QtCore, QtGui, uic, QtWidgets

def random_order(ESPECIE):
    """
    random_order(ESPECIE)
    Description:
        -This function receives every specie on a node and returns and array with every individual shuffled
    Input:
        -2D array
    Output:
        -1D array
    """
    ORDER = []
    X = 0
    Y = 0

    for j in ESPECIE:

       X = 0
       for l in j:

           ORDER += [X + 10*Y] * int(l)  
           X += 1

       Y += 1

    shuffle(ORDER)
    return ORDER

def inicial_set(Data_Especies, N_Nichos, N_Especies, Especies_Nicho):
    """
    inicial_set(Data_Especies, N_Nichos, N_Especies, Especies_Nicho)
    Description:
        -This function Creates the first set of individuals on the species array
    Input:
        -Data_Especies: Array with data for the species
        -N_Nichos: Number of nodes
        -N_Especies: Number of species
        -Especies_Nicho: Array with all the individuals and its positions on the nodes
    """
    for i in range(0,N_Especies):
        for j in range(0,int(Data_Especies[i,1])):
            k = randint(0, N_Nichos-1)
            Especies_Nicho[k,i,0] = Especies_Nicho[k,i,0]+1
    
def read_data_from_qt(window, sim):
    print("HEY")
    N_Especies = window.Data_Table.rowCount() - 1
    N_Nichos = window.Nodes.value()
    
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
         
        ACF_QT.change_item(sim.Display_Table,i,0,window.Data_Table.item(i,0).text())
         
        Data_Especies[i,1] = int(window.Data_Table.item(i,1).text())    #Catidad inicial
        Data_Especies[i,0] = int(window.Data_Table.item(i,2).text())    #direct fitness
        Data_Especies[i,4] = int(window.Data_Table.item(i,3).text())    #indirect fitness
       
            
        if window.Data_Table.item(i,4).text(): #Asociación
            Data_Especies[i,2] = ACF_QT.find_item(window.Data_Table, window.Data_Table.item(i,4).text())
        else:
            Data_Especies[i,2] = -1

        if window.Data_Table.item(i,5).text(): #Agrupación
            #compañero
            Data_Especies[i,3] = ACF_QT.find_item(window.Data_Table, window.Data_Table.item(i,5).text())
            #destino de agrupación
            Data_Especies[i,7] = ACF_QT.find_item(window.Data_Table, window.Data_Table.item(i,0).text() + "(" + window.Data_Table.item(i,5).text() + ")")
            #origen de agrupación
            Data_Especies[int(Data_Especies[i,7]),8] = i
        else:
            Data_Especies[i,3] = -1
            Data_Especies[i,7] = -1
       
        Data_Especies[i,5] = int(window.Data_Table.item(i,6).text())
        
    sim.Display_Table.setColumnCount(N_Nichos + 4)
    for i in range(0,N_Nichos):
        sim.Display_Table.setHorizontalHeaderItem(i + 4, QtWidgets.QTableWidgetItem("Nicho " + str(i + 1)))
  
    return [Data_Especies, N_Nichos, N_Especies]

def resize_matrix_3d(matrix, original_x, original_y, new_x, new_y):
    matrix_temp = numpy.zeros((new_x, new_y, int(len(matrix[0, 0, :]))), dtype=numpy.int)
    matrix_temp[0:original_x, 0:original_y, :] = matrix[:, :, :]
    matrix = numpy.zeros((new_x, new_y, int(len(matrix[0, 0, :]))), dtype=numpy.int)
    matrix = matrix_temp
    return matrix


    
    
    
    
