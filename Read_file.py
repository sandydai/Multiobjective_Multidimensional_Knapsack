
import os
def to_int(array):
    n = 0
    while n<len(array):
        array[n] = int(array[n])
        n+=1
    return array

def read_instance(file, m, j):
    ## assumes file is in SAME directory
    cwd = os.getcwd()
    path = cwd+"/"+file + ".txt"

    b = []
    c = []
    a = []

    with open(path) as f:
        lines = [line.rstrip() for line in f]

    n = int(lines[0])

    for i in range(m):
        temp = lines[i+1].split(" ")
        b.append(to_int(temp))
    for i in range(j):
        temp = lines[i + 1+m].split(" ")
        c.append(to_int(temp))
    for j in range(m):
        temp = lines[i + 1 + m+j].split(" ")
        a.append(to_int(temp))

    return n, b, c,a




