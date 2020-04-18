import numpy as np
import Read_file
def brute_force(file):
    n, b, c, a = Read_file.read_instance(file)
    #ennumerate all binary solutions and check which ones satisfy knapsack constraints

    #option - randomly generate binary x vector and check if solution is feasible

    #Ennumerate all points

    feasible = []
    N = 10000
    #check if satisfies X, if yes then append to f
    check = False
    for i in range(N):
        x = np.random.randint(2, size=n)

    for k in len(b):
        if c[k]*x >= b[k]:
            check =False
            break
        if k == len(b)-1:
            feasible.append(x)

    #Find feasible Images

    ### Check MEANING!!


    #Remove duplicates
    temp = [tuple(row) for row in feasible]
    Z = np.unique(temp)

    #Remove Dominated


    return 0





