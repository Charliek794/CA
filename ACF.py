# -*- coding: utf-8 -*-
"""
Automata Celular Functions
v0.5.1
@author: Carlos Villagrasa Guerrero
"""

"""
# libraries
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# create data
x = np.random.rand(15)
y = x+np.random.rand(15)
z = x+np.random.rand(15)
z=z*z

# Change color with c and alpha. I map the color to the X axis value.
plt.scatter(x, y, s=z*2000, c=x, cmap="Blues", alpha=0.4, edgecolors="grey", linewidth=2)

# Add titles (main and on axis)
plt.xlabel("the X axis")
plt.ylabel("the Y axis")
plt.title("A colored bubble plot")

plt.show()
"""

import numpy, math
from random import randint, shuffle

def random_order(ESPECIES):
    """
    random_order(ESPECIE)
    Description:
        -This function receives every specie on a node and returns and array with every individual shuffled
    Input:
        -ESPECIES: 2D array
    Output:
        -ORDER: 1D array
    """
    ORDER = []
    X = 0
    Y = 0

    for j in ESPECIES:

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
    return Especies_Nicho
    
def resize_matrix_3d(matrix, new_x, new_y):
    """
    resize_matrix_3d(matrix, original_x, original_y, new_x, new_y)
    Description:
        -This function changes the size of a 3D matrix keeping the z axis size the same
    Input:
        -matrix: 3D array to be resized
        -new_x: new axis x size
        -new_y: new axis y size
    """
    matrix_temp = numpy.zeros((new_x, new_y, numpy.size(matrix,2)), dtype=numpy.int)
    matrix_temp[0:numpy.size(matrix,0), 0:numpy.size(matrix,1), :] = matrix[:, :, :]
    matrix = numpy.zeros((new_x, new_y, numpy.size(matrix,2)), dtype=numpy.int)
    return matrix_temp

def convert_data(Names, Datos):
    """
    convert_data(Names, Datos, N_Especies)
    Description:
        -This function wraps data from the file to the data that the program needs
    Input:
        -Names: list of the names of the species
        -Datos: 2D list with the data from the species
    Output:
        -Data_Especies: 2D array prepared for the program with the data from the species
    """

    #Set matrix for data of the species
    Data_Especies = numpy.zeros((len(Names), 9))
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

    for i in range(0,len(Names)):
        Data_Especies[i,8] = -1
        Data_Especies[i,6] = -1

    for i in range(0,len(Names)):

        #Direct fitness
        Data_Especies[i,0] = Datos[1][i]
        #Initial quantity
        Data_Especies[i,1] = Datos[0][i]
        #Indirect fitness
        Data_Especies[i,4] = Datos[2][i]

        if not Datos[3][i]:
            Data_Especies[i,2] = -1
        else:
            #Asociation partner
            Data_Especies[i,2] = Names.index(Datos[3][i])

        if not Datos[4][i]:
            Data_Especies[i,3] = -1
            Data_Especies[i,7] = -1
        else:
            #Agrupation partner
            Data_Especies[i,3] = Names.index(Datos[4][i])
            #Agrupation result
            Data_Especies[i,7] = Names.index(Names[i] + "(" + Datos[4][i] + ")")
            #Agrupation origen
            Data_Especies[int(Data_Especies[i,7]),8] = i
        
        #Flexibility
        Data_Especies[i,5] = Datos[5][i]

    return Data_Especies

def node_agrupation(Especies_Nicho, i, Muertes, Data_Especies):
    order1 = random_order(Especies_Nicho[i,:,:])
    temp_sin_asociar = Especies_Nicho[i,:,0].copy()
    k = 0
    
    if len(order1) > 0:
        while k < len(order1):
            j = int(order1[k] / 10)
            #print(j)
            #if randint(0, 100) * Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]) <= Data_Especies[j,5]:
            if Data_Especies[j,3] != -1 and temp_sin_asociar[j] > 0:
                R = randint(0, 100)
                
                if Muertes[i,j,1] == 0 and Muertes[i,j,0] == 0:
                    #print(R)
                    if R <= Data_Especies[j,5]:
                        if int(Data_Especies[j,3]) != j:
                            if temp_sin_asociar[int(Data_Especies[j,3])] > 0:
                                Especies_Nicho[i,int(Data_Especies[j,7]),0] = Especies_Nicho[i,int(Data_Especies[j,7]),0] + 1
                                
                                Especies_Nicho[i,int(Data_Especies[j,3]),0] = Especies_Nicho[i,int(Data_Especies[j,3]),0] - 1
                                temp_sin_asociar[int(Data_Especies[j,3])] = temp_sin_asociar[int(Data_Especies[j,3])] - 1
                                
                                Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - 1
                                temp_sin_asociar[j] = temp_sin_asociar[j] - 1
                        else:
                            if temp_sin_asociar[j] > 1:
                                Especies_Nicho[i,int(Data_Especies[j,7]),0] = Especies_Nicho[i,int(Data_Especies[j,7]),0] + 1
                                Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - 2
                                temp_sin_asociar[j] = temp_sin_asociar[j] - 2  
                else:
                    
                    #print('NICHO {0} and ESPECIE{1}'.format(i, j), file = g)
                    R = randint(-10, 10)
                    #print(R + (Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]))*100, file = g)
                    #print(R + (Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]))*100)
                    if R + (Muertes[i,j,1]/(Muertes[i,j,0] + Muertes[i,j,1]))*100 <= Data_Especies[j,5]: #Agrupación 
                        if int(Data_Especies[j,3]) != j:
                            if temp_sin_asociar[int(Data_Especies[j,3])] > 0:
                                Especies_Nicho[i,int(Data_Especies[j,7]),0] = Especies_Nicho[i,int(Data_Especies[j,7]),0] + 1
                                
                                Especies_Nicho[i,int(Data_Especies[j,3]),0] = Especies_Nicho[i,int(Data_Especies[j,3]),0] - 1
                                temp_sin_asociar[int(Data_Especies[j,3])] = temp_sin_asociar[int(Data_Especies[j,3])] - 1
                                
                                Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - 1
                                temp_sin_asociar[j] = temp_sin_asociar[j] - 1
                        else:
                            if temp_sin_asociar[j] > 1:
                                Especies_Nicho[i,int(Data_Especies[j,7]),0] = Especies_Nicho[i,int(Data_Especies[j,7]),0] + 1
                                Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] - 2
                                temp_sin_asociar[j] = temp_sin_asociar[j] - 2    
            
                
                
            """
            else:
                #REVISAR
                Especies_Nicho[i,j,0] = Especies_Nicho[i,j,0] + Especies_Nicho[i,j,2]
                Especies_Nicho[i,int(Data_Especies[j,3]),0] = Especies_Nicho[i,int(Data_Especies[j,3]),0] + Especies_Nicho[i,j,2]
                Especies_Nicho[i,j,2] = 0
            """
            k = k +1

def node_asociation(Especies_Nicho, i, Muertes, Data_Especies):
    order2 = random_order(Especies_Nicho[i,:,:])
    temp_sin_asociar = Especies_Nicho[i,:,0].copy()
    
    k = 0
    if len(order2) > 0:
        while k < len(order2):
            j = int(order2[k] / 10)
            
            if Data_Especies[j,2] != -1 and temp_sin_asociar[j] > 0: #Asociación
                if temp_sin_asociar[int(Data_Especies[j,2])] > 0:
                    if int(Data_Especies[int(Data_Especies[j,2]),2]) != j:
                        Especies_Nicho[i,j,1] += 1
                        temp_sin_asociar[j] -= 1
                        Especies_Nicho[i,int(Data_Especies[j,2]),2] += 1 
                        Especies_Nicho[i,int(Data_Especies[j,2]),0] -= 1
                        temp_sin_asociar[int(Data_Especies[j,2])] -= 1
                        Especies_Nicho[i,j,0] -= 1 
                    else:              
                        if temp_sin_asociar[j] != 1 or int(Data_Especies[j,2]) != j:
                            Especies_Nicho[i,j,3] += 1
                            temp_sin_asociar[j] -= 1
                            Especies_Nicho[i,int(Data_Especies[j,2]),3] += 1 
                            Especies_Nicho[i,int(Data_Especies[j,2]),0] -= 1
                            temp_sin_asociar[int(Data_Especies[j,2])] -= 1
                            Especies_Nicho[i,j,0] -= 1 
            
            k = k +1

def reorder(order, inclusive, Data_Especies):
    T_min = 0
    T_max = 0
    for i in range(1,len(order)): 
        if inclusive == 1:
            if (Data_Especies[int(order[i]), 0]/Data_Especies[int(order[i]), 4]) > (Data_Especies[int(order[i - 1]), 0]/Data_Especies[int(order[i - 1]), 4]):               
                shuffle(order[T_min:(T_max+1)])
                T_min = i
                T_max = i
            else:
                T_max = i
        else:
            if (Data_Especies[int(order[i]), 0]) > Data_Especies[int(order[i - 1]), 0]:   
                shuffle(order[T_min:(T_max+1)])
                T_min = i
                T_max = i
            else:
                T_max = i
  
    shuffle(order[T_min:(len(order)+1)])
    return order

def node_GS(order, order_if, i, Especies_Nicho, Muertes, Deaths, Data_Especies):
    o = len(order) - 1
    k = Deaths/100 * Especies_Nicho[i,:,:].sum(axis = 0).sum()
    k = math.ceil(k)
    
    while o >= 0 and k > 0: #individuos y recipientes
        if Data_Especies[order[o],8] != -2:
            no_zero = numpy.nonzero(Especies_Nicho[i,order[o],:2])
            while len(no_zero[0]) != 0 and k > 0:
                Random = randint(0, len(no_zero[0])-1)
                
                if Especies_Nicho[i,order[o],no_zero[0][Random]] >= k:
                    Especies_Nicho[i,order[o],no_zero[0][Random]] = Especies_Nicho[i,order[o],no_zero[0][Random]] - k
                    Muertes[i,order[o],0] += k
                    k = 0
                else:
                    k = k - Especies_Nicho[i,order[o],no_zero[0][Random]]
                    Muertes[i,order[o],0] += Especies_Nicho[i,order[o],no_zero[0][Random]]
                    Especies_Nicho[i,order[o],no_zero[0][Random]] = 0
                no_zero = numpy.nonzero(Especies_Nicho[i,order[o],:2])
                
        if k > 0:
            o = o - 1
    o = len(order_if) - 1
    while o >= 0 and k > 0: # actores y reciprocos
        if Data_Especies[order_if[o],8] != -2:
            no_zero = numpy.nonzero(Especies_Nicho[i,order_if[o],2:])
            while len(no_zero[0]) != 0 and k > 0:
                Random = randint(0, len(no_zero[0])-1)
                if Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] >= k:
                    Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] = Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] - k
                    Muertes[i,order_if[o],0] += k
                    k = 0
                else:
                    k = k - Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2]
                    Muertes[i,order_if[o],0] += Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2]
                    Especies_Nicho[i,order_if[o],no_zero[0][Random] + 2] = 0
                no_zero = numpy.nonzero(Especies_Nicho[i,order_if[o],2:])
        if k > 0:
            o = o - 1
    return [Especies_Nicho, Muertes]

def node_consumption(Especies_Nicho, i, Resources, Data_Especies, N_Especies, Muertes, Reproduction):
    temp_rec = Resources
    Feeded = numpy.zeros((N_Especies,4))
    
    ORDER = random_order(Especies_Nicho[i,:,:])

    j = 0
    if len(ORDER) > 0:
        while temp_rec > 0 and j < len(ORDER):

            if Especies_Nicho[i, int(ORDER[j] / 10), int(ORDER[j] % 10)] > 0:

                if ORDER[j] % 10 == 0: #individual
                    temp_rec = temp_rec - (Data_Especies[int(ORDER[j] / 10),0] * int(Reproduction)/100)
                if ORDER[j] % 10 == 1: #asociación recipiente
                    temp_rec = temp_rec - (Data_Especies[int(ORDER[j] / 10),0] * int(Reproduction)/100)
                if ORDER[j] % 10 == 2 or ORDER[j] % 10 == 3: #asociación actor o reciproca
                    temp_rec = temp_rec - ((Data_Especies[int(ORDER[j] / 10),4] + Data_Especies[ORDER[j] // 10,0]) * int(Reproduction)/100)
                if temp_rec >= 0:
                    Feeded[ORDER[j] // 10,ORDER[j] % 10] = Feeded[ORDER[j] // 10,ORDER[j] % 10] + 1
                    
            j = j +1
        
        Muertes[i,:,1] = Especies_Nicho[i,:,:].sum(axis = 1) - Feeded.sum(axis = 1)
        
        Especies_Nicho[i,:,:] = Feeded
    return Especies_Nicho

def greed_calc(Especies_Nicho, N_Nichos, N_Especies, Data_Especies):
    Egoismo = numpy.zeros((N_Nichos,N_Especies,4))
    Egoismo_Relativo = numpy.zeros((N_Nichos,N_Especies,4))
    Egoismo_Especies = Especies_Nicho
    E_Total = 0

    for i in range(0,N_Nichos):
        E_Total = 0
        for j in range(0,N_Especies):
            Egoismo[i,j,0] = 1
            Egoismo[i,j,1] = 1
            Egoismo[i,j,2] = Data_Especies[j,0] / (Data_Especies[j,0] + Data_Especies[j,4])
            Egoismo[i,j,3] = Data_Especies[j,0] / (Data_Especies[j,0] + Data_Especies[j,4])
            
            E_Total += (Egoismo[i,j,0] * Especies_Nicho[i,j,0] +
                        Egoismo[i,j,1] * Especies_Nicho[i,j,1] +
                        Egoismo[i,j,2] * Especies_Nicho[i,j,2] +
                        Egoismo[i,j,3] * Especies_Nicho[i,j,3])
            """
            E_Total += (Egoismo[i,j,0] +
                        Egoismo[i,j,1] +
                        Egoismo[i,j,2] +
                        Egoismo[i,j,3])
            """ 
        for j in range(0,N_Especies):    
            Egoismo_Relativo[i,j,0] = Egoismo[i,j,0] / E_Total
            Egoismo_Relativo[i,j,1] = Egoismo[i,j,1] / E_Total
            Egoismo_Relativo[i,j,2] = Egoismo[i,j,2] / E_Total
            Egoismo_Relativo[i,j,3] = Egoismo[i,j,3] / E_Total

    return [Egoismo, Egoismo_Relativo, Egoismo_Especies]