# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 15:51:01 2017

Automata Celular Functions

@author: Kopaka
"""

from random import randint
from PyQt5 import QtCore, QtGui, uic, QtWidgets

def new_row(Data_Table, row):
    Data_Table.insertRow(row)
    item = QtWidgets.QTableWidgetItem()
    item.setText("0")
    #TODO
    #Data_Table.setItem(row, 1, item)
    #Data_Table.setItem(row, 2, item)
    Data_Table.setItem(row, 3, item)
    #Data_Table.setItem(row, 6, item)

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
    
def change_item(Data_Table,x,y,text):
    item = QtWidgets.QTableWidgetItem()           
    item.setText(text)
    Data_Table.setItem(x, y, item)

def inicial_set(Data_Especies, N_Nichos, N_Especies, Especies_Nicho):

    for i in range(0,N_Especies):
        for j in range(0,int(Data_Especies[i,1])):
            k = randint(0, N_Nichos-1)
            Especies_Nicho[k,i,0] = Especies_Nicho[k,i,0]+1

    
