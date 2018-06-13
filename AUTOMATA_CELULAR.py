# -*- coding: utf-8 -*-
"""
Automata Celular Main
v0.4.1
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
parser.parse_args()



from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from sip import SIP_VERSION_STR 

print("Qt version:", QT_VERSION_STR)
print("SIP version:", SIP_VERSION_STR)
print("PyQt version:", PYQT_VERSION_STR)

import sys

from PyQt5 import uic, QtWidgets


#import pyqtgraph as pg
import numpy
import ACF, ACF_QT, ACF_FILE


numpy.set_printoptions(threshold=numpy.inf)

if __name__ == '__main__':     
    app = QtWidgets.QApplication(sys.argv)
    window = ACF_QT.MyApp()
    window.show()
    app.exec_()
    
    