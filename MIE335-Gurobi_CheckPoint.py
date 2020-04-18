from gurobipy import *


m = Model("m1")

b = 36
c = [[19, 16],
 [5,  6],
 [39, 29],
 [36, 36],
 [22,  6]]
a = [29,36,36,33,6]

x = []

for i in range(len(c)):
    x.append(m.addVar(vtype = GRB.BINARY, name = str(i)))
m.update()

m.addConstr(quicksum(a[i] * x[i] for i in range(len(c))) <=b, "c1")

m.setObjective(quicksum(c[i]*x[i] for i in range(len(c))), GRB.MAXIMIZE)
m.optimize()

b = 36*1.5
c = [x / 2 for x in c]
a = [29,36,36,22,6]

m.update()
m.optimize()





