import pandas as pd
import queue as Q
import matplotlib.pyplot as plt
import numpy as np
from gurobipy import *
import gurobipy
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
        sol = brute_force(inputfile)
        curr_dir = os.cwd() + "/"
        np.savetxt(curr_dir + "BF_NDP_6.txt", sol, delimiter='\t', newline='\n')
        summary = np.asarray(BFtime(inputfile), len(sol))
        np.savetxt(curr_dir + "summary.txt", summary, delimiter='\t', newline ='\n')

        #save other outputs

    elif method ==2:

        sol1, count = Rectangle_Division(inputfile)
        sol = np.array(sol1)
        sol.sort()
        curr_dir = os.cwd() + "/"
        np.savetxt(curr_dir + "BB_NDP_6.txt", sol, delimiter='\t', newline='\n')

        summary = np.asarray(RBtime(inputfile), len(sol), count)
        np.savetxt(curr_dir + "BB_SUMMARY_6.txt", summary, delimiter='\t', newline ='\n')
        #save to curr_dir
        #save other outputs

    elif method ==3:

        sol1, count = supernal_method(inputfile)
        sol = np.array(sol1)
        sol.sort()
        curr_dir = os.cwd() + "/"
        np.savetxt(curr_dir + "SP_NDP_6.txt", sol, delimiter='\t', newline='\n')

        summary = np.asarray(supernal_time(inputfile), len(sol), count)
        np.savetxt(curr_dir + "SP_SUMMARY_6.txt", summary, delimiter='\t', newline ='\n')


    elif method == 4:
        sol1, count = supernal_method(inputfile)
        sol = np.array(sol1)
        sol.sort()
        curr_dir = os.cwd() + "/"
        np.savetxt(curr_dir + "COMPETITION_2D_NDP_6.txt", sol, delimiter='\t', newline='\n')
        summary = np.asarray(supernal_time(inputfile), len(sol), count)
        np.savetxt(curr_dir + "COMPETITION_2D_SUMMARY_06.txt", summary ,delimiter='\t', newline='\n')


    elif method ==5:

        sol1, count = supernal_method(inputfile)
        sol = np.array(sol1)
        sol.sort()
        curr_dir = os.cwd() + "/"
        np.savetxt(curr_dir + "Supernal.txt", sol, delimiter='\t', newline='\n')
        summary = np.asarray(supernal_time(inputfile), len(sol), count)
        np.savetxt(curr_dir + "COMPETITION_3D_SUMMARY_06.txt", summary, delimiter='\t', newline='\n')

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
        s2 = s2.strip()
        file.write(s2) #check that it's negative 1
        file.write('\n')

    for i in range(m):
        s = str(np.array(a)[:,i])
        st = s.replace("  ", " ")
        s1 = st.replace("[", "")
        s2 = s1.replace("]", "")
        s2 = s2.strip()
        file.write(s2)
        file.write('\n')

    file.close()


def to_float(array):
    n = 0
    while n<len(array):
        array[n] = float(array[n])
        n+=1
    return array

def read_instance(file):
    ## assumes file is in SAME directory

    cwd = os.getcwd()
    path = cwd+"/"+file + ".txt"

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

def LexMin_Helper(file, axis, z1, z2, constraint):
    #Max Z1, min Z2


    n, b, c, a = read_instance(file)
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

            constraint_1 = m.addConstr(quicksum([c[0][j] * x[j] for j in range(n)]) <= z1[1]) #z1 SE
            constraint_2 = m.addConstr(quicksum([c[0][j] * x[j] for j in range(n)]) >= z1[0]) # z1 NW
            constraint_3 = m.addConstr(quicksum([c[1][j] * x[j] for j in range(n)]) >= z2[1]) # z2 NW
            constraint_3 = m.addConstr(quicksum([c[1][j] * x[j] for j in range(n)]) <= z2[0]) # z2 SE

        if (constraint is not None):

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


def Rectangle_Division(file):
    n, b, c, a = read_instance(file)
    eps = 0.01

    FoundNDPs = []

    z_nw = LexMin("input", 0, None, None)
    z_se = LexMin("input", 1, None, None)

    FoundNDPs.append(z_nw)
    FoundNDPs.append(z_se)

    Rectangles = [[z_nw, z_se]]


    while len(Rectangles) != 0:
        R = Rectangles[0]
        print(R)

        Rectangles.remove(R)

        #lower rectangle
        R_2 = [[R[0][0], (R[0][1] + R[1][1])/2], R[1]]

        z_hat = LexMin(file, 0, R_2[0], R_2[1])
        print(z_hat)
        if z_hat[0] == -1 or z_hat[1] == -1: #non-feasible solution
            continue
        if z_hat[0] != R[1] and z_hat not in FoundNDPs:
            FoundNDPs.append(z_hat)
            Rectangles.append([z_hat, R[1]])

        #top Rectangle

        R_3 = [R[1], (z_hat[0] - eps, (R[0][1] + R[1][1]) / 2)]

        print(R_3)

        z_hat = LexMin(file, 1, R_3[0], R_3[1])

        print(z_hat)
        if z_hat[0] == -1 or z_hat[1] == -1: #non-feasible solution
            continue
        if z_hat != R[0] and z_hat not in FoundNDPs:
            FoundNDPs.append(z_hat)
            Rectangles.append([R[0], z_hat])

    return FoundNDPs

def weighted_sum_single_OOP(file, z_bound):
    np.random.seed(77973 * 2)
    n, b, c, a = read_instance(file)
    J = len(c)
    M = len(a)

    # Finding supernal point of MP
    m = gp.Model("MOP")
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    temp = []
    # Generate lambda
    if (J == 2):
        _lambda = [1, 1]
    if (J == 3):
        _lambda = [1, 1, 1]
    elif (J > 3):
        _lambda = np.random.randint(1, 3, size=J)
    # Set Objective Function
    for k in range(J):
        temp.append(LinExpr(quicksum([c[k][i] * x[i] for i in range(n)])))
    Obj = LinExpr(quicksum([_lambda[k] * temp[k] for k in range(J)]))

    m.setObjective(Obj, GRB.MINIMIZE)
    # Constraints
    for dim in range(M):
        constraint_0 = m.addConstr(quicksum([a[dim][i] * x[i] for i in range(n)]) <= b[dim])
    for k in range(J):
        consraint_1 = m.addConstr(quicksum([c[k][i] * x[i] for i in range(n)]) <= z_bound[k])

    m.update()
    m.optimize()

    if (m.status == 2):
        z_op = [sum((x[i].x) * c[j][i] for i in range(n)) for j in range(J)]
        return z_op
    else:
        return []


def supernal_method(file):
    feasible = []
    n, b, c, a = read_instance(file)
    J = len(c)
    M = len(a)
    temp = []
    region = []

    # create an arbitrary supernal point like (-1,-1 . . .) of length J
    for k in range(J):
        temp = np.random.randint(-1, 1, size=J)
        region.append(temp)

    regions = 0
    while (len(region) >= 1):  # Regions are not empty
        regions +=1
        processing = region.pop(0)
        _zMinimize = weighted_sum_single_OOP(file, processing)

        if (len(_zMinimize) != 0):  # If feasible
            feasible.append(_zMinimize)
            # remove that region you got an optimal solution with from the list
            region.remove(region[0])
            # break it down into J regions following supernal pseudo code
            newRegions = []
            for i in range(len(_zMinimize)):
                r = [1] * (len(_zMinimize))  # make a temporary array to hold the new region coordinates
                for j in range(len(_zMinimize)):
                    if (j != i):
                        # DEBUG: it should be processing since this is the region we are working with
                        r[j] = processing[j]  # keep the original region's dimension for j!=i
                    else:
                        r[j] = _zMinimize[j] - 1  # use the optimal solution's ith dimension to narrow the region down
                newRegions.append(r)  # add one of the new regions to newRegions list

            # add those new regions to the list
            for r in newRegions:
                region.append(r)
            # if J >= 3, remove dominated regions
            if (J >= 3):
                region = remove_dominated(region)
        else:
            continue

    return feasible, regions

supernal_method("input")


def supernal_time(file):
    start_time = time.perf_counter()
    sol = supernal_method(file)
    total_time = time.perf_counter() - start_time
    return total_time

def BFtime(file):
    start_time = time.perf_counter()
    sol = brute_force(file)
    total_time = time.perf_counter() - start_time
    return total_time

def RBtime(file):
    start_time = time.perf_counter()
    sol = Rectangle_Division(file)
    total_time = time.perf_counter() - start_time
    return total_time







