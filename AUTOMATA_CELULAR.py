# -*- coding: utf-8 -*-
"""
Automata Celular Main
v0.5.1
@author: Carlos Villagrasa Guerrero

python 3
numpy
pip3 install matplotlib
pip3 install pyqt5
"""
"""
Comprobación de librerías y ficheros necesarios
Argument vectors comandos de ejecución optparse

"""
import argparse
parser = argparse.ArgumentParser()
#parser.add_argument("echo", help="echo the string you use here")
#parser.add_argument("square", help="display a square of a given number", type=int)
#parser.add_argument("-v", "--verbose", help="increase output verbosity", default=False, action="store_true")
parser.add_argument("-n", "--nogui", help="Run the program without GUI (must enter file [-f] name that exist on data folder and generations [-g] to run)", 
					default=False, action="store_true")
parser.add_argument("-f", "--file", help="File name")
parser.add_argument("-g", "--gen", help="Generations to run", type=int)


args = parser.parse_args()
#if args.verbose:
#    print("verbosity turned on")
#    print(args.echo)

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


#import pyqtgraph as pg
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
    
    #Output files for data checking
    f = open("out.txt",'w')
    f.close()
    f = open("flex.txt",'w')
    f.close()

    for t in range(1, args.gen + 1):

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

            ACF.node_agrupation(Especies_Nicho, i, Muertes, Data_Especies)
                    
            ACF.node_asociation(Especies_Nicho, i, Muertes, Data_Especies)

        print("FIN DE ASO/AGR", file = f)
        print(Especies_Nicho, file = f)

        [Egoismo, Egoismo_Relativo, Egoismo_Especies] = ACF.greed_calc(Especies_Nicho, N_Nichos, N_Especies, Data_Especies)

        #Resets deaths for this generation
        Muertes = numpy.zeros((N_Nichos,N_Especies,2))

        #Order by direct fitness/indirect fitness proportion
        order_if = numpy.argsort(Data_Especies[:,0]/Data_Especies[:,4])
        order = numpy.argsort(Data_Especies[:,0])

        print(order_if, file = f)    
        print(order, file = f)
        
        order_if = ACF.reorder(order_if, 1, Data_Especies)

        order = ACF.reorder(order, 0, Data_Especies)
        
        print("reordenado: 1->DF/IF; 2->DF", file = f)
        print(order_if, file = f)    
        print(order, file = f) 

        for i in range(0,N_Nichos):
            [Especies_Nicho, Muertes] = ACF.node_GS(order, order_if, i, Especies_Nicho, Muertes, Deaths, Data_Especies)
        
        print("FIN DE SG", file = f)
        print(Especies_Nicho, file = f)

        """
        Individual selection
        """
        if Reproduction != 0:
            for i in range(0,N_Nichos):

                Especies_Nicho = ACF.node_consumption(Especies_Nicho, i, Resources, Data_Especies, N_Especies, Muertes, Reproduction)
            
        print("FIN DE SI", file = f)
        print(Especies_Nicho, file = f)



        


















        
    
    
    