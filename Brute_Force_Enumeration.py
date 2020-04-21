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
    #check if satisfies X, if yes then append to f
    check = False
    x_list = list(itertools.product([0, 1], repeat=int(n)))

    for x in x_list:
        # print("start")
        # print(x)
        count = 0
        for k in range(len(b)): #loop through all knapsacks
            # print(np.dot(a[k], x))
            # print(b[k])

            if np.dot(a[k], x) > b[k]:
                check =False
                break #if doesn't meet one of the constraints, then move to next x
            count +=1
        if count == len(b):
            feasible.append(x)

    Z = []
    for val in feasible:
        Z.append(np.dot(c[k], val))
    Z_temp = np.unique(np.array(Z))

    Z = RemoveNonDominated.BFM_NDP(Z_temp)

    return Z

print(brute_force("ExampleData"))





