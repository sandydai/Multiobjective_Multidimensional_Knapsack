
import os
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

    n = float(lines[0])
    temp = lines[1]
    b.append(float(temp))
    m = 1

    while len(lines[1+m].split(" ")) < 2:
        temp = lines[1+m]
        b.append(float(temp))
        m+=1

    j = len(lines) - (2*m + 1) #number of C vectors


    for i in range(j): #C vectors start from index = 1+m

        temp = lines[i + 1+m].split(" ")

        c.append(to_float(temp))

    for i in range(m): #a vectors start from index 1+m+j

        temp = lines[i + 1 + m+j].split(" ")
        a.append(to_float(temp))

    return n, b, c, a


# n,b,c,a = read_instance("instance6")
# print(n,b,c,a)







