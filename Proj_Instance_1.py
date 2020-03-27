# Create two m-KP-MOP problem instances with n = 5, J ∈ {2, 3}, m = 1, U = 40
# usingAlgorithm4(oneforJ=2andoneforJ=3).
# Youneedtosetseed=last five digits of a group member’s student number
# in the generation algorithm. You can use numpy.random.seed(seed) function to do that.
import numpy as np
import math

def m_KP_MOP(n, m, J, U):
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
    instance_num = input("What is the instance number:   ")
    instance = "instance" + instance_num

    file = open(instance + ".txt","w+")
    file.write(str(n) +  "\n")
    for i in range(len(b)):
        file.write(str(b[i]))
        file.write('\n')

    for j in range(J):
        file.write(str(np.array(c)[:,j]*-1)) #check that it's negative 1
        file.write('\n')

    for i in range(m):
        file.write(str(np.array(a)[:,i]))
        file.write('\n')

    file.close()

m_KP_MOP(5, 1, 1, 40)
#m_KP_MOP(5, 1, 2, 40)










