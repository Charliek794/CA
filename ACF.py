# -*- coding: utf-8 -*-
"""
Automata Celular Functions
v0.1.5
@author: Carlos Villagrasa Guerrero
"""

from random import randint
from PyQt5 import QtCore, QtGui, uic, QtWidgets

def change_item(Data_Table,x,y,text):
    item = QtWidgets.QTableWidgetItem()           
    item.setText(text)
    Data_Table.setItem(x, y, item)

def new_row(Data_Table, row):
    Data_Table.insertRow(row)
    #TODO
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
    for i in range(0,Data_Table.rowCount() - 1):
        if nombre == Data_Table.item(i, 0).text():
            return i
    return -1

def delete_item(Data_Table,x,y):
    item = QtWidgets.QTableWidgetItem()   
    nombre = ""        
    item.setText(nombre)
    Data_Table.setItem(x, y, item)

def inicial_set(Data_Especies, N_Nichos, N_Especies, Especies_Nicho):

    for i in range(0,N_Especies):
        for j in range(0,int(Data_Especies[i,1])):
            k = randint(0, N_Nichos-1)
            Especies_Nicho[k,i,0] = Especies_Nicho[k,i,0]+1

def refresh_total(Display_Table, N_Nichos, N_Especies, Especies_Nicho):
    for i in range(0,N_Nichos):
        change_item(Display_Table,N_Especies,i + 4,str(Especies_Nicho[i,:,:].sum(axis = 0).sum()))
    change_item(Display_Table,N_Especies,3,str(Especies_Nicho[:,:,:].sum(axis = 0).sum()))
    
