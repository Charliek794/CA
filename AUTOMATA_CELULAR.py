# -*- coding: utf-8 -*-
"""
Automata Celular Main
v0.7.1
@author: Carlos Villagrasa Guerrero

python 3
numpy
pip3 install matplotlib
pip3 install pyqt5
"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nogui", help="Run the program without GUI (must enter file [-f] name that exist on data folder and generations [-g] to run)", 
					default=False, action="store_true")
parser.add_argument("-f", "--file", help="File name")
parser.add_argument("-g", "--gen", help="Generations to run", type=int)


args = parser.parse_args()

import warnings
warnings.filterwarnings("ignore")

from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from sip import SIP_VERSION_STR

print("Qt version:", QT_VERSION_STR)
print("SIP version:", SIP_VERSION_STR)
print("PyQt version:", PYQT_VERSION_STR)

import sys
import os

from PyQt5 import uic, QtWidgets

import numpy
import ACF, ACF_QT, ACF_FILE

numpy.set_printoptions(threshold=numpy.inf)

if not os.path.isdir("data"):
    os.mkdir("data")
if not os.path.isdir("results"):
    os.mkdir("results")
    
if not args.nogui:
    if __name__ == '__main__':     
        app = QtWidgets.QApplication(sys.argv)
        window = ACF_QT.MyApp()
        window.show()
        app.exec_()
else:
    [Names, Datos, N_Nichos, Resources, Consumption, Deaths] = ACF_FILE.Load(args.file)
    N_Especies = len(Names)

    #Set matrix for data of the species
    Data_Especies = ACF.convert_data(Names, Datos)
    
    #Initialize Deaths array and Species array
    Muertes = numpy.zeros((N_Nichos, N_Especies, 2))
    Especies_Nicho = numpy.zeros((N_Nichos, N_Especies, 4), dtype=numpy.int)

    #Initial setup for species
    Especies_Nicho = ACF.inicial_set(Data_Especies, N_Nichos, N_Especies, Especies_Nicho)

    #Write initial data 
    ACF_FILE.data_write(args.file, Data_Especies, Especies_Nicho, N_Especies, 'w')

    #Greed calculation
    Egoismo_Relativo = ACF.greed_calc(Data_Especies, N_Nichos, N_Especies)

    #Initialize Historic data
    Historic = [[] for _ in range(6)]
    Historic[0].append(Names)
    Historic[1].append(Data_Especies)
    Historic[2].append(Especies_Nicho)
    Historic[3].append([]) #Individual selective pressure
    Historic[4].append(Egoismo_Relativo) #Greed
    Historic[5].append([]) #Species quantity for Greed
    
    #Output files for data checking
    f = open("out.txt",'w')
    f.close()
    f = open("flex.txt",'w')
    f.close()



    for t in range(1, args.gen + 1):
        print(t)
        f = open("out.txt",'a')
        g = open("flex.txt",'a')

        print(t, file = f)
        print("GENERACIÓN " + str(t), file = f)
        print("--------------------------------------------------------------------------------------------", file = f)
        print(t, file = g)
        print("GENERACIÓN " + str(t), file = g)
        print("--------------------------------------------------------------------------------------------", file = g)

        print(Especies_Nicho, file = f)
        print("AGR", file = f)
        print("Aggrupation", file = g)
        print("-------------------------------------------------", file = g)

        for i in range(0,N_Nichos):

            Especies_Nicho[i,:,:] = ACF.node_agrupation_percentage(Especies_Nicho[i,:,:], Muertes[i,:,:], Data_Especies)
                    
            Especies_Nicho[i,:,:] = ACF.node_asociation(Especies_Nicho[i,:,:], Muertes[i,:,:], Data_Especies)

        print("FIN DE ASO/AGR", file = f)
        print(Especies_Nicho, file = f)

        Egoismo_Especies = Especies_Nicho.copy()

        #Greed calculation
        Egoismo_Relativo = ACF.greed_calc(Especies_Nicho, Data_Especies, N_Nichos, N_Especies)

        #Resets deaths for this generation
        Muertes = numpy.zeros((N_Nichos,N_Especies,2))
        
        for i in range(0,N_Nichos):
            #Order by greed
            order = numpy.dstack(numpy.unravel_index(numpy.argsort(Egoismo_Relativo[i,:,:].ravel()), (N_Especies, 4)))

            print(order, file = f)

            order = ACF.reorder_Greed(order, Egoismo_Relativo[i,:,:])
            
            print("reordenado", file = f)   
            print(order, file = f) 
            [Especies_Nicho[i,:,:], Muertes[i,:,:]] = ACF.node_GS_Greed(order, Especies_Nicho[i,:,:], Muertes[i,:,:], Deaths)
        
        print("FIN DE SG", file = f)
        print(Especies_Nicho, file = f)

        """
        Individual selection
        """
        if Consumption != 0:
            for i in range(0,N_Nichos):

                [Especies_Nicho[i,:,:], Muertes[i,:,:]] = ACF.node_consumption(Especies_Nicho[i,:,:], Resources, Data_Especies, N_Especies, Muertes[i,:,:], Consumption)
            
        print("FIN DE SI", file = f)
        print(Especies_Nicho, file = f)

        """     
        Reproduction
        """
        for i in range(0,N_Nichos):
            Especies_Nicho[i,:,:] = ACF.node_reproduction(Especies_Nicho[i,:,:], Data_Especies, N_Especies)

        print("FIN DE REPRODUCCIÓN", file = f)
        print(Especies_Nicho, file = f)

        """
        Flexibility
        """

        for i in range(0,N_Nichos):
            Especies_Nicho[i,:,:] = ACF.node_flexibility(Especies_Nicho[i,:,:], Data_Especies, N_Especies, Muertes[i,:,:])

        print("FIN DE FLEXIBILIDAD", file = f)
        print(Especies_Nicho, file = f)    

        Especies_Nicho = ACF.distribution(Especies_Nicho, N_Nichos,N_Especies)

        print("FIN DE REPARTO", file = f)
        print(Especies_Nicho, file = f)
        print("MUERTES", file = f)
        print(Muertes, file = f) 

        """
        Individual selection pressure
        """
        P = ACF.IS_pressure(Especies_Nicho, Muertes, N_Especies, N_Nichos)

        Historic[0].append(Names) #Names
        Historic[1].append(Data_Especies) #Actual data
        Historic[2].append(Especies_Nicho) #Species on each node
        Historic[3].append(P) #Individual selective pressure (DEATHS)
        Historic[4].append(Egoismo_Relativo) #Greed
        Historic[5].append(Egoismo_Especies) #Species quantity for Greed 
        
    ACF_FILE.bubbles_write(Historic, args.file, N_Especies, N_Nichos)








        


















        
    
    
    