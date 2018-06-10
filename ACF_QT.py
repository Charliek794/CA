# -*- coding: utf-8 -*-
"""
Automata Celular Qt Functions
v0.4.1
@author: Carlos Villagrasa Guerrero
"""

from PyQt5 import QtCore, QtGui, uic, QtWidgets

def change_item(Data_Table, x, y, text):
    """
    change_item(Data_Table, x, y, text)
    Description:
        -This function changes the text from one cell of the data table
    Input:
        -Data_Table: QT table handler
        -x, y: Position of the item to be changed
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

    change_item(Data_Table,row,0,"0")
    change_item(Data_Table,row,1,"0")
    change_item(Data_Table,row,2,"0")
    change_item(Data_Table,row,3,"0")
    change_item(Data_Table,row,4,"0")
    change_item(Data_Table,row,5,"0")
    change_item(Data_Table,row,6,"0")
    change_item(Data_Table,row,7,"0")
    
    change_item(Data_Table,row,0,"")
    change_item(Data_Table,row,1,"")
    change_item(Data_Table,row,2,"")
    change_item(Data_Table,row,3,"")
    change_item(Data_Table,row,4,"")
    change_item(Data_Table,row,5,"")
    change_item(Data_Table,row,6,"")
    change_item(Data_Table,row,7,"")
    
    
    
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
    Output:
        -x, y: Position of the item to be changed
    """    
    item = QtWidgets.QTableWidgetItem()   
    nombre = ""        
    item.setText(nombre)
    Data_Table.setItem(x, y, item)
    
def update_table(Display_Table, Especies_Nicho, Muertes, N_Nichos, N_Especies):
    """
    refresh_total(Display_Table, N_Nichos, N_Especies, Especies_Nicho)
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
            change_item(Display_Table,i,j+4,str(Especies_Nicho[j,i,0]))

        change_item(Display_Table,i,3,str(Especies_Nicho[:,i,:].sum(axis = 1).sum()))
        #Presión selectiva individual
        change_item(Display_Table,i,1,str(Muertes.sum(axis = 0)[i,1]/Muertes.sum(axis = 0)[i].sum(axis = 0)))
        # Potencial biótico
        #change_item(sim.Display_Table,i,2,str(T[i]))
  
    change_item(Display_Table,N_Especies,0,"Total")

    for i in range(0,N_Nichos):
        change_item(Display_Table,N_Especies,i + 4,str(Especies_Nicho[i,:,:].sum(axis = 0).sum()))
    change_item(Display_Table,N_Especies,3,str(Especies_Nicho[:,:,:].sum(axis = 0).sum()))

def potential(sim, Data_Especies, N_Especies):
    for i in range(0,N_Especies):
        # Potencial biótico
        
        if Data_Especies[i,2] == -1:  #direct fitness + Indirect fitness del asociado
            Temp = Data_Especies[i,0] * Data_Especies[i,1] # Falta el multiplicador
        else:
            Temp = (Data_Especies[i,0] + Data_Especies[int(Data_Especies[i,2]),4]) * Data_Especies[i,1] # Falta el multiplicador
        change_item(sim.Display_Table, i, 1, str(Temp)) #actual
        change_item(sim.Display_Table, i, 2, str(Temp)) #acumulado