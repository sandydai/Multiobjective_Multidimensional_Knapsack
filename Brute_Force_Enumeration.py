import numpy as np
import Read_file
import itertools
import RemoveNonDominated

def brute_force(file):
    n, b, c, a = Read_file.read_instance(file)

    ### is C negative??
    ##taking in C as negative values will mean we want to minimize (in order to maximize)

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
    Z = RemoveNonDominated.BFM_NDP(Z_temp)

    return Z

print(brute_force("input"))





