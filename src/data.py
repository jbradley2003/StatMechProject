import time
import numpy as np
from node import Node
from seq import *
from setup import *

x = []
y = []

n = 10
b = generateOrderedSeqs(n)
g = generateConformations(n, [0]*n)
j = 0

start_time = time.perf_counter()
for phi in list(b.keys()):
    p = 0
    x.append(phi)
    for s in b.get(phi):
        # j += 1
        # print(j)
        setEnsembleSequence(g, s)
        p = max(p, calcZ(g, 200)[0]) 
    y.append(p)
end_time = time.perf_counter()
print("time: ", (end_time - start_time))
plt.plot(x,y,marker='o')
plt.show()