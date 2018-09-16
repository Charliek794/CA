# -*- coding: utf-8 -*-
"""
Automata Celular Functions
v0.7.2
@author: Carlos Villagrasa Guerrero
"""

import numpy, math
from random import randint, shuffle

def random_order(ESPECIES):
    """
    random_order(ESPECIES)
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

def node_agrupation_percentage(Especies_Nicho, Muertes, Data_Especies, N_Especies):
    """
    node_agrupation(Especies_Nicho, i, Muertes, Data_Especies)
    Description:
        -This function agruppate the especies of a node
    Input:
        -Especies_Nicho: Array with all the individuals and its positions on the nodes
        -i: Node to agruppate
        -Muertes: Array with the deaths for the species 
        -Data_Especies: Array with data for the species       
    """
    order1 = random_order(Especies_Nicho[:,:])
    temp_sin_asociar = Especies_Nicho[:,0].copy()
    k = 0
    
    temp_to_agr = numpy.zeros((N_Especies), dtype=int)
    for i in range(0, N_Especies):
        if Data_Especies[i,3] != -1:
            if Especies_Nicho[i,0] > Especies_Nicho[int(Data_Especies[i,3]),0]:
                temp_to_agr[i] = int(Especies_Nicho[i,0] * Data_Especies[i,5] / 100)
            else:
                temp_to_agr[i] = int(Especies_Nicho[int(Data_Especies[i,3]),0] * Data_Especies[i,5] / 100)
        else:
            temp_to_agr[i] = Especies_Nicho[i,0]

    if len(order1) > 0:
        while k < len(order1):
            j = int(order1[k] / 10)

            if Data_Especies[j,3] != -1 and temp_sin_asociar[j] > 0 and temp_to_agr[j] > 0:
                if int(Data_Especies[j,3]) != j:
                    if temp_sin_asociar[int(Data_Especies[j,3])] > 0 and temp_to_agr[int(Data_Especies[j,3])] > 0:
                        Especies_Nicho[int(Data_Especies[j,7]),0] = Especies_Nicho[int(Data_Especies[j,7]),0] + 1
                        
                        Especies_Nicho[int(Data_Especies[j,3]),0] = Especies_Nicho[int(Data_Especies[j,3]),0] - 1
                        temp_sin_asociar[int(Data_Especies[j,3])] = temp_sin_asociar[int(Data_Especies[j,3])] - 1
                        
                        Especies_Nicho[j,0] = Especies_Nicho[j,0] - 1
                        temp_sin_asociar[j] = temp_sin_asociar[j] - 1
                        temp_to_agr[j] = temp_to_agr[j] - 1
                        temp_to_agr[int(Data_Especies[j,3])] = temp_to_agr[int(Data_Especies[j,3])] - 1
                else:
                    if temp_sin_asociar[j] > 1 and temp_to_agr[j] > 1:
                        Especies_Nicho[int(Data_Especies[j,7]),0] = Especies_Nicho[int(Data_Especies[j,7]),0] + 1
                        Especies_Nicho[j,0] = Especies_Nicho[j,0] - 2
                        temp_sin_asociar[j] = temp_sin_asociar[j] - 2
                        temp_to_agr[j] = temp_to_agr[j] - 2      

            k = k +1
    return Especies_Nicho

def node_agrupation(Especies_Nicho, Data_Especies, N_Especies):
    """
    node_agrupation(Especies_Nicho, i, Muertes, Data_Especies)
    Description:
        -This function agruppate the especies of a node
    Input:
        -Especies_Nicho: Array with all the individuals and its positions on the nodes
        -i: Node to agruppate
        -Muertes: Array with the deaths for the species 
        -Data_Especies: Array with data for the species       
    """
    temp_sin_asociar = Especies_Nicho[:,:].copy()  

    SUM_E = numpy.sum(Especies_Nicho)

    for i in range(0, N_Especies):
        if Data_Especies[i,3] != -1:
            if temp_sin_asociar[i,0] > 0:
                if Data_Especies[i,5] > 0:
                    if Data_Especies[i,5] > temp_sin_asociar[i,0]/SUM_E:
                        if int(Data_Especies[i,5]*SUM_E/100) < temp_sin_asociar[i,0]:
                            if int(Data_Especies[i,5]*SUM_E/100) < temp_sin_asociar[int(Data_Especies[i,3]),0]:
                                Especies_Nicho[int(Data_Especies[i,7]),0] += int(Data_Especies[i,5]*SUM_E/100)
                                Especies_Nicho[i,0] -= int(Data_Especies[i,5]*SUM_E/100)
                                Especies_Nicho[int(Data_Especies[i,3]),0] -= int(Data_Especies[i,5]*SUM_E/100)
                                temp_sin_asociar[int(Data_Especies[i,3]),0] -= int(Data_Especies[i,5]*SUM_E/100)
                                temp_sin_asociar[i,0] -= int(Data_Especies[i,5]*SUM_E/100)
                            else:
                                Especies_Nicho[int(Data_Especies[i,7]),0] += temp_sin_asociar[int(Data_Especies[i,3]),0]
                                Especies_Nicho[i,0] -= temp_sin_asociar[int(Data_Especies[i,3]),0]
                                Especies_Nicho[int(Data_Especies[i,3]),0] = 0 
                                temp_sin_asociar[int(Data_Especies[i,3]),0] = 0
                                temp_sin_asociar[i,0] -= temp_sin_asociar[int(Data_Especies[i,3]),0]
                        else: 
                            if temp_sin_asociar[i,0] < temp_sin_asociar[int(Data_Especies[i,3]),0]:
                                Especies_Nicho[int(Data_Especies[i,7]),0] += temp_sin_asociar[i,0]
                                Especies_Nicho[i,0] = 0
                                Especies_Nicho[int(Data_Especies[i,3]),0] -= temp_sin_asociar[i,0]
                                temp_sin_asociar[int(Data_Especies[i,3]),0] -= temp_sin_asociar[i,0]
                                temp_sin_asociar[i,0] = 0
                            else:
                                Especies_Nicho[int(Data_Especies[i,7]),0] += temp_sin_asociar[int(Data_Especies[i,3]),0]
                                Especies_Nicho[i,0] -= temp_sin_asociar[int(Data_Especies[i,3]),0]
                                Especies_Nicho[int(Data_Especies[i,3]),0] = 0 
                                temp_sin_asociar[int(Data_Especies[i,3]),0] = 0
                                temp_sin_asociar[i,0] -= temp_sin_asociar[int(Data_Especies[i,3]),0]

                elif Data_Especies[i,5] < 0:
                    if abs(Data_Especies[i,5]) < temp_sin_asociar[i,0]/SUM_E:
                        if int((1 - abs(Data_Especies[i,5]))*SUM_E/100) < temp_sin_asociar[i,0]:
                            if int((1 - abs(Data_Especies[i,5]))*SUM_E/100) < temp_sin_asociar[int(Data_Especies[i,3]),0]:
                                Especies_Nicho[int(Data_Especies[i,7]),0] += int((1 - abs(Data_Especies[i,5]))*SUM_E/100)
                                Especies_Nicho[i,0] -= int(Data_Especies[i,5]*SUM_E/100)
                                Especies_Nicho[int(Data_Especies[i,3]),0] -= int((1 - abs(Data_Especies[i,5]))*SUM_E/100)
                                temp_sin_asociar[int(Data_Especies[i,3]),0] -= int((1 - abs(Data_Especies[i,5]))*SUM_E/100)
                                temp_sin_asociar[i,0] -= int(Data_Especies[i,5]*SUM_E/100)
                            else:
                                Especies_Nicho[int(Data_Especies[i,7]),0] += temp_sin_asociar[int(Data_Especies[i,3]),0]
                                Especies_Nicho[i,0] -= temp_sin_asociar[int(Data_Especies[i,3]),0]
                                Especies_Nicho[int(Data_Especies[i,3]),0] = 0 
                                temp_sin_asociar[int(Data_Especies[i,3]),0] = 0
                                temp_sin_asociar[i,0] -= temp_sin_asociar[int(Data_Especies[i,3]),0]
                        else: 
                            if temp_sin_asociar[i,0] < temp_sin_asociar[int(Data_Especies[i,3]),0]:
                                Especies_Nicho[int(Data_Especies[i,7]),0] += temp_sin_asociar[i,0]
                                Especies_Nicho[i,0] = 0
                                Especies_Nicho[int(Data_Especies[i,3]),0] -= temp_sin_asociar[i,0]
                                temp_sin_asociar[int(Data_Especies[i,3]),0] -= temp_sin_asociar[i,0]
                                temp_sin_asociar[i,0] = 0
                            else:
                                Especies_Nicho[int(Data_Especies[i,7]),0] += temp_sin_asociar[int(Data_Especies[i,3]),0]
                                Especies_Nicho[i,0] -= temp_sin_asociar[int(Data_Especies[i,3]),0]
                                Especies_Nicho[int(Data_Especies[i,3]),0] = 0 
                                temp_sin_asociar[int(Data_Especies[i,3]),0] = 0
                                temp_sin_asociar[i,0] -= temp_sin_asociar[int(Data_Especies[i,3]),0]

    return Especies_Nicho

def node_asociation(Especies_Nicho, Muertes, Data_Especies):
    """
    node_agrupation(Especies_Nicho, i, Muertes, Data_Especies)
    Description:
        -This function associate the especies of a node
    Input:
        -Especies_Nicho: Array with all the individuals and its positions on the nodes
        -i: Node to associate
        -Muertes: Array with the deaths for the species 
        -Data_Especies: Array with data for the species       
    """
    order2 = random_order(Especies_Nicho[:,:])
    temp_sin_asociar = Especies_Nicho[:,0].copy()
    
    k = 0
    if len(order2) > 0:
        while k < len(order2):
            j = int(order2[k] / 10)
            
            if Data_Especies[j,2] != -1 and temp_sin_asociar[j] > 0: #Asociación
                if temp_sin_asociar[int(Data_Especies[j,2])] > 0:
                    if int(Data_Especies[int(Data_Especies[j,2]),2]) != j:
                        Especies_Nicho[j,1] += 1
                        temp_sin_asociar[j] -= 1
                        Especies_Nicho[int(Data_Especies[j,2]),2] += 1 
                        Especies_Nicho[int(Data_Especies[j,2]),0] -= 1
                        temp_sin_asociar[int(Data_Especies[j,2])] -= 1
                        Especies_Nicho[j,0] -= 1 
                    else:              
                        if temp_sin_asociar[j] != 1 or int(Data_Especies[j,2]) != j:
                            Especies_Nicho[j,3] += 1
                            temp_sin_asociar[j] -= 1
                            Especies_Nicho[int(Data_Especies[j,2]),3] += 1 
                            Especies_Nicho[int(Data_Especies[j,2]),0] -= 1
                            temp_sin_asociar[int(Data_Especies[j,2])] -= 1
                            Especies_Nicho[j,0] -= 1 
            
            k = k +1
    return Especies_Nicho

def node_GS(Especies_Nicho, Muertes, Deaths, Egoismo_Relativo, Lambda, N_Especies):
    """
    node_GS(order, i, Especies_Nicho, Muertes, Deaths)
    Description:
        -This function does the group selection on a node 
    Input:
        -order: Array order to be reordered
        -inclusive: flag for using DF or DF/IF
        -Data_Especies: Array with data for the species       
    """
    k = Deaths/100 * Especies_Nicho[:,:].sum(axis = 0).sum()
    k = math.ceil(k)
    
    Distr = numpy.zeros((N_Especies,4))

    for i in range(0,N_Especies):
        for j in range(0,4):
            if Especies_Nicho[i,j] == 0:
                Distr[i,j] = 0
            else:
                Distr[i,j] = math.exp(Lambda * Egoismo_Relativo[i,j])

    SUM_D = numpy.sum(Distr)

    for i in range(0,N_Especies):
        for j in range(0,4):
            if Especies_Nicho[i,j] > 0:
                temp = math.ceil(Distr[i,j] * k / SUM_D)
                if temp < Especies_Nicho[i,j]:
                    Muertes[i,0] += temp
                    Especies_Nicho[i,j] -= temp
                else:
                    Muertes[i,0] += Especies_Nicho[i,j]

                    Especies_Nicho[i,j] = 0

    return [Especies_Nicho, Muertes]

def node_consumption(Especies_Nicho, Resources, Data_Especies, N_Especies, Muertes, Reproduction):
    temp_rec = Resources
    Feeded = numpy.zeros((N_Especies,4))
    
    ORDER = random_order(Especies_Nicho[:,:])

    j = 0
    if len(ORDER) > 0:
        while temp_rec > 0 and j < len(ORDER):

            if Especies_Nicho[int(ORDER[j] / 10), int(ORDER[j] % 10)] > 0:

                if ORDER[j] % 10 == 0: #individual
                    temp_rec = temp_rec - (Data_Especies[int(ORDER[j] / 10),0] * int(Reproduction)/100)
                if ORDER[j] % 10 == 1: #asociación recipiente
                    temp_rec = temp_rec - (Data_Especies[int(ORDER[j] / 10),0] * int(Reproduction)/100)
                if ORDER[j] % 10 == 2 or ORDER[j] % 10 == 3: #asociación actor o reciproca
                    temp_rec = temp_rec - ((Data_Especies[int(ORDER[j] / 10),4] + Data_Especies[ORDER[j] // 10,0]) * int(Reproduction)/100)
                if temp_rec >= 0:
                    Feeded[ORDER[j] // 10,ORDER[j] % 10] = Feeded[ORDER[j] // 10,ORDER[j] % 10] + 1
                    
            j = j +1
        
        Muertes[:,1] = Especies_Nicho[:,:].sum(axis = 1) - Feeded.sum(axis = 1)
        
        Especies_Nicho[:,:] = Feeded
    return [Especies_Nicho, Muertes]

def greed_calc(Especies_Nicho, Data_Especies, N_Nichos, N_Especies):

    Egoismo = numpy.zeros((N_Nichos,N_Especies,4))
    Egoismo_Relativo = numpy.zeros((N_Nichos,N_Especies,4))
    E_Total = 0
    
    for i in range(0,N_Nichos):
        
        for j in range(0,N_Especies):
            if Especies_Nicho[i,j,0] == 0: #Individual
                Egoismo[i,j,0] = 0
            else:    
                Egoismo[i,j,0] = Data_Especies[j,0]

            if Especies_Nicho[i,j,1] == 0: #Recipiente
                Egoismo[i,j,1] = 0
            else:
                Egoismo[i,j,1] = Data_Especies[j,0] + Data_Especies[int(Data_Especies[j,2]),4]

            if Especies_Nicho[i,j,2] == 0: #Actor
                Egoismo[i,j,2] = 0
            else:
                Egoismo[i,j,2] = Data_Especies[j,0] - Data_Especies[j,4]

            if Especies_Nicho[i,j,3] == 0: #Reciproco
                Egoismo[i,j,3] = 0
            else: 
                Egoismo[i,j,3] = Data_Especies[j,0] + Data_Especies[int(Data_Especies[j,2]),4] - Data_Especies[j,4]

        MIN = numpy.amin(Egoismo[i,:,:])
        for j in range(0,N_Especies): 
            if Especies_Nicho[i,j,0] == 0: #Individual
                Egoismo[i,j,0] = 0
            else:    
                Egoismo[i,j,0] = Egoismo[i,j,0] - MIN + 1

            if Especies_Nicho[i,j,1] == 0: #Recipiente
                Egoismo[i,j,1] = 0
            else:
                Egoismo[i,j,1] = Egoismo[i,j,1] - MIN + 1

            if Especies_Nicho[i,j,2] == 0: #Actor
                Egoismo[i,j,2] = 0
            else:
                Egoismo[i,j,2] = Egoismo[i,j,2] - MIN + 1

            if Especies_Nicho[i,j,3] == 0: #Reciproco
                Egoismo[i,j,3] = 0
            else: 
                Egoismo[i,j,3] = Egoismo[i,j,3] - MIN + 1   

        MAX = numpy.amax(Egoismo[i,:,:])
        if MAX == 0:
            MAX = 1
        for j in range(0,N_Especies):    
            Egoismo_Relativo[i,j,0] = Egoismo[i,j,0] / MAX
            Egoismo_Relativo[i,j,1] = Egoismo[i,j,1] / MAX
            Egoismo_Relativo[i,j,2] = Egoismo[i,j,2] / MAX
            Egoismo_Relativo[i,j,3] = Egoismo[i,j,3] / MAX

    return Egoismo_Relativo

def node_reproduction(Especies_Nicho, Data_Especies, N_Especies):

    temp_Especies = numpy.zeros((N_Especies,4), dtype=int)
    
    for j in range(0, N_Especies):
        for k in range(0, 4):
            if k == 0:
                temp_Especies[j,0] += Especies_Nicho[j,k] * Data_Especies[j,0]

            if (k == 1 or k==3) and Data_Especies[j,2] != -1:
                temp_Especies[j,0] += Especies_Nicho[j,k] * (Data_Especies[j,0] + Data_Especies[int(Data_Especies[j,2]),4])

            if k == 2:
                temp_Especies[j,0] += Especies_Nicho[j,k] * Data_Especies[j,0]
    return temp_Especies



def node_flexibility(Especies_Nicho, Data_Especies, N_Especies):

    temp_sin_asociar = Especies_Nicho[:,:].copy()  

    SUM_E = numpy.sum(Especies_Nicho)

    for i in range(0, N_Especies):
        if Data_Especies[i,8] != -1:
            if temp_sin_asociar[i,0] > 0:
                if Data_Especies[i,5] > 0:
                    if Data_Especies[i,5] > temp_sin_asociar[i,0]/SUM_E:
                        if int(Data_Especies[i,5]*SUM_E/100) < temp_sin_asociar[i,0]:
                            Especies_Nicho[int(Data_Especies[i,8]),0] += temp_sin_asociar[i,0] - int(Data_Especies[i,5]*SUM_E/100)
                            Especies_Nicho[int(Data_Especies[int(Data_Especies[i,8]),3]),0] += temp_sin_asociar[i,0] - int(Data_Especies[i,5]*SUM_E/100)
                            Especies_Nicho[i,0] = int(Data_Especies[i,5]*SUM_E/100)

                        else: 
                            Especies_Nicho[int(Data_Especies[i,8]),0] += 0
                            Especies_Nicho[int(Data_Especies[int(Data_Especies[i,8]),3]),0] += 0
                            Especies_Nicho[i,0] = temp_sin_asociar[i,0]

                elif Data_Especies[i,5] < 0:
                    if abs(Data_Especies[i,5]) < temp_sin_asociar[i,0]/SUM_E:
                        if int((1 - abs(Data_Especies[i,5]))*SUM_E/100) < temp_sin_asociar[i,0]:

                            Especies_Nicho[int(Data_Especies[i,8]),0] += temp_sin_asociar[i,0] - int((1 - abs(Data_Especies[i,5]))*SUM_E/100)
                            Especies_Nicho[int(Data_Especies[int(Data_Especies[i,8]),3]),0] += temp_sin_asociar[i,0] - int((1 - abs(Data_Especies[i,5]))*SUM_E/100)
                            Especies_Nicho[i,0] = int((1 - abs(Data_Especies[i,5]))*SUM_E/100)
                           
                        else: 

                            Especies_Nicho[int(Data_Especies[i,8]),0] += 0
                            Especies_Nicho[int(Data_Especies[int(Data_Especies[i,8]),3]),0] += 0
                            Especies_Nicho[i,0] = temp_sin_asociar[i,0]
                            
    return Especies_Nicho


def distribution(Especies_Nicho, N_Nichos,N_Especies):

    temp_Especies = numpy.zeros((N_Nichos,N_Especies,4), dtype=int)
    for i in range(0, N_Nichos):
        for j in range(0, N_Especies):
            for I in range(0,int(Especies_Nicho[i,j,0])):
                if N_Nichos > 4:
                    l = randint(-2, 2)
                    if i + l >= N_Nichos:    
                        temp_Especies[i + l - N_Nichos,j,0] += 1
                    elif i + l < 0:
                        temp_Especies[i + l + N_Nichos,j,0] += 1
                    else:
                        temp_Especies[i + l,j,0] += 1
                else:
                    l = randint(0, N_Nichos - 1)
                    temp_Especies[l,j,0] += 1
    return temp_Especies


def IS_pressure(Especies_Nicho, Muertes, N_Especies, N_Nichos):
    P = numpy.zeros(N_Nichos)

    for i in range(0,N_Nichos):
        
        not_count = 0
        for j in range(0,N_Especies):
            if ((Especies_Nicho[i,j,:].sum()) != 0):
                if ((Muertes[i,j,0] + Muertes[i,j,1]) != 0):
                    P[i] += Muertes[i,j,1] / (Muertes[i,j,0] + Muertes[i,j,1])
                else:
                    P[i] += 0.5
            else:
                not_count += 1
        if (N_Especies - not_count) == 0:
            P[i] = 0.5
        else:
            P[i] = P[i] / (N_Especies - not_count)

    return P
