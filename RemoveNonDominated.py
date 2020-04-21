import numpy as np

def BFM_NDP(Z):
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


    #loop through entire array of solutions, if
def weightedsum(array):
    NDP = []


    return NDP

# print(BFM_NDP(np.array([[7,1],[4,2], [-1,3]])))