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
from datetime import datetime



def LexMin_Helper(file, axis, z1, z2, constraint):
    #Max Z1, min Z2
    print(z1)
    print(z2)

    n, b, c, a = Read_file.read_instance(file)
    z_i = -1

    #set opposite axis
    if axis == 0:
        opp = 1
    else:
        opp = 0

    try:
        m = gurobipy.Model("Binary_Knapsack")
        x = m.addVars(n, vtype=GRB.BINARY, name="x")
        m.Params.outputFlag = 0

        obj = LinExpr(quicksum([x[j] * c[axis][j] for j in range(n)]))
        m.setObjective(obj, GRB.MINIMIZE)
        for i in range(len(a)): #m number of constraints
            constraint_0 = m.addConstr(quicksum([a[i][j] * x[j] for j in range(n)]) <= b[i])


        if (z1 is not None and z2 is not None): #constraints of 2 lex problems for m as 0,1
            # print("here")
            # print(z1[0])
            # print(z1[1])
            # print(z2[0])
            # print(z2[1])

            constraint_1 = m.addConstr(quicksum([c[0][j] * x[j] for j in range(n)]) <= z1[1]) #z1 SE
            constraint_2 = m.addConstr(quicksum([c[0][j] * x[j] for j in range(n)]) >= z1[0]) # z1 NW
            constraint_3 = m.addConstr(quicksum([c[1][j] * x[j] for j in range(n)]) >= z2[1]) # z2 NW
            constraint_3 = m.addConstr(quicksum([c[1][j] * x[j] for j in range(n)]) <= z2[0]) # z2 SE

        if (constraint is not None):
            # print("here2")
            # print(constraint)
            # print(opp)
            constraint_4 = m.addConstr(quicksum([c[opp][j] * x[j] for j in range(n)]) <= constraint) #other corner must also be NDP



        m.update()
        m.optimize()

        if (m.status == 2): # there exists an optimal solution
            z_i = m.objVal


    except ValueError:
        z_i = -1

    return z_i


def LexMin(file, axis, z1, z2): #axis = 0 for NW and 1 for SE
    #minimize z1, then minimize z2
    if axis == 0: #solving z1 first
        z_1 = round(LexMin_Helper(file, 0, z1, z2, None))
        z_2 = round(LexMin_Helper(file, 1, z1, z2, z_1))

    if axis == 1: #solving z2 first
        z_2 = round(LexMin_Helper(file, 1, z1, z2, None))
        z_1 = round(LexMin_Helper(file, 0, z1, z2, z_2))

    return [z_1,z_2]

def Bisect(R):
    new_R = []
    temp = [R[0][0], (R[0][1] + R[1][1])/2]
    new_R.append(temp)
    new_R.append(R[1])
    return new_R

def Rectangle_Division(file):
    n, b, c, a = Read_file.read_instance(file)
    eps = 0.1

    FoundNDPs = []

    z_nw = LexMin("input", 0, None, None)
    z_se = LexMin("input", 1, None, None)

    FoundNDPs.append(z_nw)
    FoundNDPs.append(z_se)

    Rectangles = [[z_nw, z_se]]

    print(Rectangles)

    while len(Rectangles) != 0:
        R = Rectangles[0]
        print(R)
        Rectangles.remove(R)
        R_2 = Bisect(R)
        print(R_2[0], R_2[1])

        z_hat = LexMin(file, 0, R_2[0], R_2[1])
        print(z_hat)
        if z_hat[0] == -1 or z_hat[1] == -1: #non-feasible solution
            continue
        if z_hat[0] != R[1] and z_hat not in FoundNDPs:
            FoundNDPs.append(z_hat)
            Rectangles.append([R[0], z_hat])
            print(1)
        R_3 = [R[0], [z_hat[0] - eps, Bisect(R)]]
        z_hat = LexMin(file, 1, R_3[1], R_3[0])
        if z_hat[0] == -1 or z_hat[1] == -1: #non-feasible solution
            continue
        if z_hat!= R[0] and z_hat not in FoundNDPs:
            FoundNDPs.append(z_hat)
            Rectangles.append([R[0], z_hat])
            print(1)



    return FoundNDPs

z_nw = LexMin("input", 0, None, None)
z_se = LexMin("input", 1, None, None)
print(Rectangle_Division("input"))
#print(LexMin("input", 0, z_nw,z_se))





