# -*- coding: utf-8 -*-
"""
Automata Celular File Functions
v0.4.1
@author: Carlos Villagrasa Guerrero
"""
import csv
import os
from PyQt5 import QtWidgets

def data_write(Name, Data_Especies, Especies_Nicho, N_Especies, mode):
    """
    data_write(Name, Data_Especies, Especies_Nicho, N_Especies, mode)
    Description:
        -This function writes data on some files
    Input:
        -Data_Table: QT table handler
    Output:
        -x, y: Position of the item to be changed
    """  
    print("DATOS")
    fpath = os.path.join("results", Name)

    if not os.path.isdir(fpath):
        os.mkdir(fpath)
    try:
        with open(os.path.join(fpath, "datos.csv") , mode, newline='') as csvfile: 
            spamwriter = csv.writer(csvfile)
            for i in range(0,len(Data_Especies[:,0])):
                spamwriter.writerow(Data_Especies[i,:])
    except IOError:
        print("ERROR: Oops! Something is wrong with the file. Try again...")
        #QtWidgets.QMessageBox.about(sim, "ERROR", "Oops! Something is wrong with the file. Try again...")
      
    """  
    print("RESULTADOS")    
    try:
        with open(os.path.join(fpath, "resultados.csv"), mode, newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['GENERACIÓN INICIAL'])
            spamwriter.writerow(['--------------------------------'])
            for i in range(0,N_Especies):
                spamwriter.writerow([sim.Display_Table.item(i, 0).text()] +
                                     ['nan'] +
                                     [sim.Display_Table.item(i, 3).text()])
    except IOError:
        print("ERROR: Oops! Something is wrong with the file. Try again...")
        #QtWidgets.QMessageBox.about(sim, "ERROR", "Oops! Something is wrong with the file. Try again...")
        
    print("NICHOS")    
    try:
        with open(os.path.join(fpath, "nichos.csv"), mode, newline='') as csvfile:
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
        print("ERROR: Oops! Something is wrong with the file. Try again...")
        #QtWidgets.QMessageBox.about(sim, "ERROR", "Oops! Something is wrong with the file. Try again...")

    """

def Load(File):
    """
    Load(File)
    Description:
        -This function loads data from a csv file
    Input:
        -File: Name of the csv file
    Output:
        -Names: List with the names of the species
        -Datos: 2D list with the data for the species
        -Nodes: Integer with the quantity of nodes
        -Resources: Integer with the resources generated on each generation on each node
        -Consumption: Integer with the % of consumption based on the inclusive fitness
        -Deaths: Integer with the % of death from group selection
    """  
    print("LOAD")
    fpath = os.path.join("data", File + ".csv")
    try:
        with open(fpath, 'r', newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            Datos = [[] for _ in range(6)]
            Names = []
            Nodes = 0
            Resources = 0
            Consumption = 0
            Deaths = 0
            i = 0
            for row in spamreader:
                if i == 0:
                    Nodes = int(row[7])
                    Resources = int(row[8])
                    Consumption = int(row[9])
                    Deaths = int(row[10])
                Names.append(row[0])
                Datos[0].append(row[1])
                Datos[1].append(row[2])
                Datos[2].append(row[3])
                Datos[3].append(row[4])
                Datos[4].append(row[5])
                Datos[5].append(row[6])
                i += 1  
            return [Names, Datos, Nodes, Resources, Consumption, Deaths]          
    except IOError:
        print("ERROR: Oops! Something is wrong with the file. Try again...")
        #QtWidgets.QMessageBox.about(self, "ERROR", "Oops! Something is wrong with the file. Try again...")

def Save(File, Names, Datos, Nodes, Resources, Reproduction, Deaths):
    """
    Save(File, Names, Datos, Nodes, Resources, Reproduction, Deaths)
    Description:
        -This function loads data from a csv file
    Input:
        -File: Name of the csv file
        -Names: List with the names of the species
        -Datos: 2D list with the data for the species
        -Nodes: Integer with the quantity of nodes
        -Resources: Integer with the resources generated on each generation on each node
        -Consumption: Integer with the % of consumption based on the inclusive fitness
        -Deaths: Integer with the % of death from group selection
    """  
    print("SAVE")
    fpath = os.path.join("data", File + ".csv")
    try:
        with open(fpath, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)

            for i in range(0,len(Names)):
                print([Names[i]]  + 
                         [Datos[0][i]]  +
                         [Datos[1][i]]  +
                         [Datos[2][i]]  +
                         [Datos[3][i]]  +
                         [Datos[4][i]]  +
                         [Datos[5][i]])
                if i == 0:
                    spamwriter.writerow([Names[i]]  + 
                                         [Datos[0][i]]  +
                                         [Datos[1][i]]  +
                                         [Datos[2][i]]  +
                                         [Datos[3][i]]  +
                                         [Datos[4][i]]  +
                                         [Datos[5][i]]  +
                                         [Nodes] + [Resources] + 
                                         [Reproduction] + [Deaths] )
                    
                else:
                    spamwriter.writerow([Names[i]]  + 
                                         [Datos[0][i]]  +
                                         [Datos[1][i]]  +
                                         [Datos[2][i]]  +
                                         [Datos[3][i]]  +
                                         [Datos[4][i]]  +
                                         [Datos[5][i]])
    except IOError:
        print("ERROR: Oops! Something is wrong with the file. Try again...")
        #QtWidgets.QMessageBox.about(self, "ERROR", "Oops! Something is wrong with the file. Try again...")

