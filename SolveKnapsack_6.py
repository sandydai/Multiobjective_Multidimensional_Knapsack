import pandas as pd
import numpy as np
import Read_file
import scipy as sp
import queue as Q
from gurobipy import *
import gurobipy
import itertools
import matplotlib . pyplot as plt
import copy
import time
import collections
import os
import itertools
from datetime import datetime

## SOLVE KNAPSACK

def SolveKnapsack(inputfile, method):

    if method ==1:

        sol = Brute_Force_Enumeration(inputfile)
        curr_dir = os.cwd() + "/"
        #save to curr_dir
        #save other outputs

    if method ==2:

        sol = Rectangle_Division(inputfile)
        curr_dir = os.cwd() + "/"
        #save to curr_dir
        #save other outputs

    if method ==3:

        sol = Supernal(inputfile)
        curr_dir = os.cwd() + "/"
        #save to curr_dir
        #save other outputs

    return

## RANDOM INSTANCE

def m_KP_MOP(n, m, J, U):
    #n number of items
    #m number of dimensions in knapsack
    #J number of knapsacks

    if U < 40:
        return "Error, U must be greater than 40"

    np.random.seed(77973)

    c = np.random.randint(1, high=U, size = (n, J))
    a = np.random.randint(1, high=U, size = (n, m))

    b = []

    for k in range(m):
        a_np = np.array(a)
        sum = 0
        for i in range(n):
            sum += a[i][k]
        temp = a_np[:,k]
        np.append(temp, math.ceil(0.5*sum))
        b.append(max(temp))  #b is capacity in k


    # Writing to txt
    instance_num = input("What is the instance number:   ") #for text file name
    instance = "instance" + str(instance_num)

    file = open(instance + ".txt","w+")
    file.write(str(n) + "\n")
    for i in range(len(b)):
        file.write(str(b[i]))
        file.write('\n')

    for j in range(J):
        s = str(np.array(c)[:,j]*-1)
        st = s.replace("  ", " ")
        s1 = st.replace("[", "")
        s2 = s1.replace("]", "")
        file.write(s2) #check that it's negative 1
        file.write('\n')

    for i in range(m):
        s = str(np.array(a)[:,i])
        st = s.replace("  ", " ")
        s1 = st.replace("[", "")
        s2 = s1.replace("]", "")
        file.write(s2)
        file.write('\n')

    file.close()
    return

def to_float(array):
    n = 0
    while n<len(array):
        array[n] = float(array[n])
        n+=1
    return array

def read_instance(file):

    path = file

    b = []
    c = []
    a = []

    with open(path) as f:
        lines = [line.rstrip() for line in f]

    n = int(lines[0])
    temp = lines[1]
    b.append(int(temp))
    m = 1

    while len(lines[1+m].split(" ")) < 2:
        temp = lines[1+m]
        b.append(int(temp))
        m+=1

    j = len(lines) - (2*m + 1) #number of C vectors


    for i in range(j): #C vectors start from index = 1+m

        temp = lines[i + 1+m].split(" ")

        c.append(to_float(temp))

    for i in range(m): #a vectors start from index 1+m+j

        temp = lines[i + 1 + m+j].split(" ")
        a.append(to_float(temp))

    return n, b, c, a

def remove_dominated(Z):
    NDP = []
    pareto_front = np.ones(len(Z), dtype=bool) #initialize all feasible values as True

    #loop through Z and compare scores - if score is lower than NDP
    #j dominates/same as all i AND one of j is better than one of i

    for i in range(len(Z)):
        for j in range(len(Z)):

            if np.all(Z[j] <= Z[i]) and np.any(Z[j] < Z[i]):
                pareto_front[i] = False
                break

    for i in range(len(Z)):
        if pareto_front[i]:
            NDP.append(Z[i])
    return np.array(NDP)


def brute_force(file):
    n, b, c, a = read_instance(file)

    #ennumerate all binary solutions and check which ones satisfy knapsack constraints

    #Ennumerate all points

    feasible = []
    Z = []
    #check if satisfies X, if yes then append to f

    x_list = list(itertools.product([0, 1], repeat=int(n)))


    for x in x_list:

        count = 0
        for k in range(len(b)): #loop through all knapsacks

            if np.dot(a[k], x) > b[k]:
                break #if doesn't meet one of the constraints, then move to next x
            count +=1
        if count == len(b):
            feasible.append(x)

    for val in feasible:
        temp = []
        for k in range(len(c)):
            temp.append(np.dot(c[k], val))
        Z.append(temp)

    # print(Z)
    Z_temp = np.unique(Z, axis = 0)
    # print(Z_temp)
    Z = remove_dominated(Z_temp)

    return Z
