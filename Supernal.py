import numpy as np
import Read_file
from gurobipy import *
import gurobipy as gp
import RemoveNonDominated


def weighted_sum_single_OOP(file,
                            z_bound):  # add another parameter for the region; should be a list of the RHS of area constraints
    np.random.seed(77973 * 2)
    n, b, c, a = Read_file.read_instance(file)
    J = len(c)
    M = len(a)
    print(J)
    print(M)
    # Finding supernal point of MP
    m = gp.Model("MOP")
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    temp = []
    # Generate lambda
    if (J == 2):
        _lambda = np.random.randint(1, 2, size=J)
    elif (J >= 3):
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
        consraint_1 = m.addConstr(quicksum([c[k][i] * x[i] for i in range(n)]) <= temp[k])
        # Add Area constraints (e.g z1 < -1 ; z2 < <-3 ; z3 < -1)

    m.update()
    m.optimize()

    # TODO Add area constraints

    if (m.status == 2):
        z_op = [sum((x[i].x) * c[j][i] for i in range(n)) for j in range(J)]
        return z_op
    else:
        return []


def supernal_method(file):
    feasible = []
    n, b, c, a = Read_file.read_instance(file)
    J = len(b)
    M = len(a)

    region = []  # create an arbitrary supernal point like (-1,-1 . . .)) of length J
    while (len(region) >= 1):  # Regions are not empty
        processing = region[0]
        _zMinimize = weighted_sum_single_OOP(file, processing)
        if (len(_zMinimize) != 0):  # If feasible
            feasible.append(_zMinimize)
            # remove that region you got an optimal solution with from the list
            region.remove(region[0])
            newRegions = [0] * n
            # break it down into J regions following supernal pseudo code
            for i in range(len(processing)):
                for j in range(len(processing)):
                    if (j != i):
                        newRegions[j] = processing[j] - 1
                        newRegions[i] = processing[i]
            # add those new regions to the list
            for r in newRegions:
                region.append(r)
            # if J >= 3, remove dominated regions
            if (J >= 3):
                region = RemoveNonDominated.BFM_NDP(region)
        else:
            continue

    return feasible

print(supernal_method("input"))