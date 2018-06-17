#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import scipy.spatial
import time
start = time.clock()

def limited_hamming_distance(matrix, m, n, contain):
    sequence = []
    count = 0#iteration stop condition
    dis_matrix = scipy.spatial.distance.pdist(matrix, 'hamming') * n#calculate hamming distance into a adjacent matrix
    dis_matrix_squareform = scipy.spatial.distance.squareform(dis_matrix)#square the matrix
    for i in range(m):# find lines hammming distance less than 3
        for j in range(i, m):
            if 0<dis_matrix_squareform[i][j]<3:
                sequence.append([i,j])
    if (len(sequence) == 0):
        mordified_dis_matrix = scipy.spatial.distance.pdist(matrix, 'hamming') * n
        mordified_dis_matrix_squareform = scipy.spatial.distance.squareform(mordified_dis_matrix)
        return matrix, mordified_dis_matrix_squareform, contain, count
    else:
        for k in range(len(sequence)):# transform the second line large base into a small one, and small base into a larger one
            for i in range(n):
                if (matrix[sequence[k][0]][i] == matrix[sequence[k][1]][i]) and (matrix[sequence[k][0]][i] <= 2):
                    if [sequence[k][0], i] not in contain:
                        count += 1
                        matrix[sequence[k][0]][i] = matrix[sequence[k][0]][i] + 1
                        contain.append([sequence[k][0], i])
                    else:
                        continue
                elif (matrix[sequence[k][0]][i] == matrix[sequence[k][1]][i]) and (matrix[sequence[k][0]][i] > 2):
                    if [sequence[k][0], i] not in contain:
                        count +=1
                        matrix[sequence[k][0]][i] = matrix[sequence[k][0]][i] - 1
                        contain.append([sequence[k][0], i])
                    else:
                        continue
        mordified_dis_matrix = scipy.spatial.distance.pdist(matrix, 'hamming') * n
        mordified_dis_matrix_squareform = scipy.spatial.distance.squareform(mordified_dis_matrix)
        return matrix, mordified_dis_matrix_squareform, contain, count
     

def limit_base_ratio(matrix, m, n, mordified_contain_1):
    k = int(m/16)#16 lines a group
    count = 0#iteration stop condition
    base_ratios = []
    for i in range(k):#in every group
        for g in range(n):#in every column
            distribution = {}
            base_len = []
            base_ratio = []
            
            for j in range(i * 16, (i + 1) * 16):# in every row in group
                distribution.setdefault(matrix[j][g], []).append([j, g])#record the address of every base
            for h in range(1,5):
                if h in distribution.keys():
                    base_len.append(len(distribution[h]))#count base number, meanwhile the base order is fixed
                else:
                    base_len.append(0)
            for p in range(4):
                base_ratio.append(base_len[p]/16)
            base_ratios.append(base_ratio)
            #only two situation meet the request(4,4,4,4; 3,3,5,5; 5,4,4,3/(ignore 3,3,3,7;3,3,4,6))
            for l in range(len(base_len) - 1):
                for o in range(l + 1, len(base_len)):
                    if(abs(base_len[l] - base_len[o]) > 2):#base is represented by l+1 and o+1
                        count +=1
                        if((base_len[l] - base_len[o]) > 2):
                            #replace the higher occupy ratio one to the lower one
                            if [distribution[l+1][0][0], distribution[l+1][0][1]] not in mordified_contain_1:
                                matrix[distribution[l+1][0][0], distribution[l+1][0][1]] = o+1
                                mordified_contain_1.append([distribution[l+1][0][0], distribution[l+1][0][1]])
                            else:
                                continue
                        elif((base_len[l] - base_len[o]) < -2):
                            if [distribution[o+1][0][0], distribution[o+1][0][1]] not in mordified_contain_1:
                                matrix[distribution[o+1][0][0], distribution[o+1][0][1]] = l+1
                                mordified_contain_1.append([distribution[o+1][0][0], distribution[o+1][0][1]])
                            else:
                                continue
            continue
    return matrix, base_ratios, mordified_contain_1, count


def Barcode(m, n):
    Barcode_ini = np.random.randint(1, 5, size = [m, n])
    matrix = Barcode_ini
    number_1 = number_2 = number_3 = 1
    iteration_time = 0
    while(number_3 != 0):
        contain = []
        number_3 = 0
        while (number_1 != 0 or number_2 != 0):
            hammming_distance_matrix, mordified_dis_matrix_squareform, mordified_contain_1, number_1 = limited_hamming_distance(matrix, m, n, contain)
            base_ratio_matrix, base_ratios, mordified_contain_2, number_2 = limit_base_ratio(hammming_distance_matrix, m, n, mordified_contain_1)
            matrix = base_ratio_matrix
            if (len(mordified_contain_2) < 150):
                contain = mordified_contain_2
            else:
                matrix = np.random.randint(1, 5, size = [m, n])
                contain = []
                number_1 = number_2 = 1
        else:
            '''change the second base of 3 continuitious bases'''
            for i in range(m):
                for j in range(n-2):
                    if (matrix[i][j] == matrix[i][j + 1] == matrix[i][j + 2]) and (matrix[i][j + 1] <= 2):
                        number_3 += 1
                        matrix[i][j + 1] = matrix[i][j + 1] + 1
                    elif(matrix[i][j] == matrix[i][j + 1] == matrix[i][j + 2]) and (matrix[i][j + 1] > 2):
                        number_3 += 1
                        matrix[i][j + 1] = matrix[i][j + 1] - 1
            
    else:        
        return matrix, mordified_dis_matrix_squareform, base_ratios

    


if __name__ == "__main__":
    m = 80
    n = 10
    #m = int(input("(interger times of 16)barcode number: "))
    #n = int(input("barcode length: "))
    designed_barcode, mordified_dis_matrix_squareform, base_ratios = Barcode(m, n)
    for i in range(len(designed_barcode)):
        for j in range(len(designed_barcode[0])):
            if designed_barcode[i][j] == 1:
                print('A', end = ' ')
            if designed_barcode[i][j] == 2:
                print('T', end = ' ')
            if designed_barcode[i][j] == 3:
                print('C', end = ' ')
            if designed_barcode[i][j] == 4:
                print('G', end = ' ')
        print('\n')
    for k in range(len(mordified_dis_matrix_squareform)):
        for l in range(len(mordified_dis_matrix_squareform)):
            print(mordified_dis_matrix_squareform[k][l], end = '\t')
        print(end = '\n')
    print(base_ratios)
    elapsed = (time.clock() - start)
    print("Time used:", elapsed)
            

