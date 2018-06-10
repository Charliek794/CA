# -*- coding: utf-8 -*-
"""
Automata Celular File Functions
v0.4.1
@author: Carlos Villagrasa Guerrero
"""
import csv
from PyQt5 import QtWidgets

def data_write(window, sim, Data_Especies, Especies_Nicho, N_Especies, mode):
    print("DATOS")
    try:
        with open(window.CSV_NAME.text() + '_datos.csv', mode, newline='') as csvfile: 
            spamwriter = csv.writer(csvfile)
            for i in range(0,len(Data_Especies[:,0])):
                spamwriter.writerow(Data_Especies[i,:])
    except IOError:
        QtWidgets.QMessageBox.about(sim, "ERROR", "Oops! Something is wrong with the file. Try again...")
      
    print("RESULTADOS")    
    try:
        with open(window.CSV_NAME.text() + '_resultados.csv', mode, newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['GENERACIÓN INICIAL'])
            spamwriter.writerow(['--------------------------------'])
            for i in range(0,N_Especies):
                spamwriter.writerow([sim.Display_Table.item(i, 0).text()] +
                                     ['nan'] +
                                     [sim.Display_Table.item(i, 3).text()])
    except IOError:
        QtWidgets.QMessageBox.about(sim, "ERROR", "Oops! Something is wrong with the file. Try again...")
        
    print("NICHOS")    
    try:
        with open(window.CSV_NAME.text() + '_nichos.csv', mode, newline='') as csvfile:
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
        QtWidgets.QMessageBox.about(sim, "ERROR", "Oops! Something is wrong with the file. Try again...")
    