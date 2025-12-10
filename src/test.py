import time
import numpy as np
from node import Node
from seq import *
from setup import *
from mc import *

# TESTING

# HPHPPHPPHH folding sequence for -epsilon = [1,12]
folding = [0,1,0,1,1,0,1,1,0,0]
nonfolding = [1,1,1,1,1,0,0,0,0,0]

x = [x for x in range(0,30)]
y1 = []
y2 = []
y3 = []
y4 = []

# g_mc = main(10, 100, folding, 2)
# setEnsembleSequence(g_mc, nonfolding)

for e in x:
    g_mc = main(10, 1000, folding,e)
    g_ld = generateConformations(10, folding)
    y1.append(calcAvgP(g_mc, e))
    y2.append(calcAvgP(g_ld,e))
    setEnsembleSequence(g_mc, nonfolding)
    setEnsembleSequence(g_ld, nonfolding)
    y3.append(calcAvgP(g_mc, e))
    y4.append(calcAvgP(g_ld,e))

# plt.plot(x, y1, marker='o')
# plt.plot(x, y2, marker='o')
# plt.plot(x, y3, marker='o')
# plt.plot(x, y4, marker='o')
# plt.show()
# Line fitting

# itr = 100000
# # m, b = np.polyfit(iter_int, t,1)
# # plt.text(3, 8, "y = " + str(round(m, 8)) + "n + " + str(round(b, 3)), style='italic')
# plt.ylabel('Average Runtime (s)')
# plt.xlabel('Number of iterations')