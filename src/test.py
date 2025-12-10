import time
import numpy as np
from node import Node
from seq import *
from setup import *
from mc import *

# TESTING

# HPHPPHPPHH folding sequence for -epsilon = [1,12]

# seq = [1,1,1,1,1,0,0,0,0,0] 
# x = [x for x in range(0,13)]
# g = generateConformations(10,seq)
# y = [calcAvgZ(g, e)[0] for e in x]
# plt.plot(x,y, marker='o')
# # plt.yscale('log')
# plt.show()

# Line fitting

# itr = 100000
# # m, b = np.polyfit(iter_int, t,1)
# # plt.text(3, 8, "y = " + str(round(m, 8)) + "n + " + str(round(b, 3)), style='italic')
# plt.ylabel('Average Runtime (s)')
# plt.xlabel('Number of iterations')