import time
import numpy as np
from node import Node
from seq import *
from setup import *
from mc import *

# At low iteration counts, there can be divide by zero errors, this is likely due to overflow issues.

def generateContour(n, itr, energy, seq, lvls=10, log=True, color='viridis'):
    print("Start")
    start = time.perf_counter()
    X, Y = np.meshgrid(itr, energy)
    w, h = len(itr), len(energy)
    print(len(itr))
    m_error = [[0 for x in range(w)] for y in range(h)] 
    for i in range(w):
        for j in range(h):
            m1 = calcAvgM(generateConformations(n, seq), energy[j]) # Deterministic model
            m2 = 0
            for k in range(5): # Average over 5 MC ensembles 
                m2 += calcAvgM(main(n, itr[i], seq, energy[j]), energy[j])
            m_error[j][i] = m2/5 - m1
    end = time.perf_counter()
    print("End: ", (end-start)/60)
    cp = plt.contourf(X, Y, m_error, levels=lvls, cmap=color) 
    plt.colorbar(cp, label=r'$<m>_{MC} - <m>_{LD}$')
    plt.title("Folding Sequence (HPHPPHPPHH)")
    plt.xlabel('Number of iterations')
    plt.ylabel(r'$-\epsilon \; (\frac{E}{kT})$')
    plt.contour(X, Y, m_error, colors='black', linestyles='dashed', linewidths=0.8)
    if log is True:
        plt.xscale('log')
    plt.show()

# Contour plots

folding = [0,1,0,1,1,0,1,1,0,0]
nonfolding = [1,1,1,1,1,0,0,0,0,0]
iterate = [10, 100, 1000, 10000, 100000]
energy = [x for x in range(1, 13)]

generateContour(10, iterate, energy, folding)
generateContour(10, iterate, energy, nonfolding)




