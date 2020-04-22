


import numpy as np
import Read_file
from gurobipy import *
import gurobipy as gp
import RemoveNonDominated
import time


def weighted_sum_single_OOP(file, z_bound):
    np.random.seed(77973 * 2)
    n, b, c, a = Read_file.read_instance(file)
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
    n, b, c, a = Read_file.read_instance(file)
    J = len(c)
    M = len(a)
    temp = []
    region = []

    # create an arbitrary supernal point like (-1,-1 . . .) of length J
    for k in range(J):
        temp = np.random.randint(-1, 1, size=J)
        region.append(temp)

    region = 0
    while (len(region) >= 1):  # Regions are not empty
        region +=1
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
                region = RemoveNonDominated.remove_dominated(region)
        else:
            continue

    return feasible, region

supernal_method("input")


def supernal_time(file):
    start_time = time.perf_counter()
    NDP = supernal_method(file)
    total_time = time.perf_counter() - start_time
    return total_time