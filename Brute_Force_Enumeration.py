import numpy as np
import Read_file

def brute_force(file,m,j):
    n, b, c, a = Read_file.read_instance(file, 2, 2)
    #ennumerate all binary solutions and check which ones satisfy knapsack constraints

    #option - randomly generate binary x vector and check if solution is feasible

    #Ennumerate all points

    feasible = []
    N = 10000
    #check if satisfies X, if yes then append to f
    check = False
    for i in range(N):
        x = np.random.randint(2, size=int(n))

        for k in range(len(b)):

            if np.dot(c[k], x) >= b[k]:
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

    return Z

brute_force("instance6",2,2)





