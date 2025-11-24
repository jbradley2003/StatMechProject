import numpy as np
import scipy
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from node import Node

DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

# Chain Generation

def enumerate_saws(n):
    """
    Generate all self-avoiding walks of length n on a 2D square lattice
    using depth-first search.
    """
    start = (0, 0)
    walk = [start]
    occupied = {start}


    def dfs():
        # If we've reached the desired chain length, yield the walk
        if len(walk) == n:
            yield walk   # return a copy
            return

        # Try extending in all directions
        for d in DIRECTIONS:
            nxt = add(walk[-1], d)

            # Self-avoidance check
            if nxt in occupied:
                continue

            # Extend the walk
            walk.append(nxt)
            occupied.add(nxt)

            # Recurse
            yield from dfs()

            # Backtrack
            walk.pop()
            occupied.remove(nxt)

    yield from dfs()

# Turn SAW into graph

def sawToGraph(saw):
    g = []
    i = 0
    for b in saw:
        if i == 0:
            g.append(Node(b, 'H', set()))
        else:
            g.append(Node(b, 'H', set()))
            g[i].connect(g[i-1])
        i += 1
    return g

# Generate all conformations of length n

def generateConformations(n, seq):
    g = []
    for w in enumerate_saws(n):
        h = sawToGraph(w)
        setSequence(h, seq)
        g.append(h)
    return g

# Represent residue sequence as list of bits

def setSequence(graph, seq):
    if len(graph) == len(seq):
        for i in range(len(graph)):
            if seq[i] == 0:
                graph[i].polarity = 'H'
            else:
                graph[i].polarity = 'P'
    else:
        print("Length mismatch")


def findTopolHHNeighbors(graph):
    h_nodes = [node for node in graph if node.polarity == 'H']
    h_positions = [node.position for node in graph if node.polarity == 'H']
    visited = set()
    m = 0
    for n in h_nodes:
        neigh_positions = [node.position for node in n.neighbors]
        for d in DIRECTIONS:  
            nxt = add(n.position, d)
            if nxt in h_positions and nxt not in neigh_positions:
                pair = tuple(sorted([n.position, nxt]))
                if pair not in visited:
                    visited.add(pair)
                    m += 1
    return m

def getGraphSequence(graph):
    seq = []
    for n in graph:
        if n.polarity == 'H':
            seq.append(0)
        else:
            seq.append(1)
    return seq

def findAllTopolNeighbors(graph):
    return

def displayConformation(graph):
    n = len(graph)
    x_l = []
    y_l = []
    plt.figure()
    for n in graph: 
            x_l.append(n.position[0])
            y_l.append(n.position[1])
    plt.plot(x_l,y_l, marker='.',ms=10)
    plt.show()

def printPositions(graph):
    for i in range(len(graph)):
        print("Node " + str(i) + " position: " + str(graph[i].position))

def calcZ(ensemble, e):
    max = 0
    z = 0
    freq = {}
    for i in ensemble:
        m = findTopolHHNeighbors(i)
        if m in freq:
            freq[m] += 1
        else:
            freq[m] = 1
        if m > max:
            max = m
    for i in range(max+1):
        if i in freq:
            z += freq[i] * np.exp((max-i)*(-e))
    return [z, freq, max]

def calcAvgM(ensemble, e):
    z, freq, max = calcZ(ensemble, e)
    avg_m = 0
    for i in range(max+1):
        if i in freq:
            avg_m += i * freq[i] * np.exp((max-i)*(-e))
    avg_m /= z
    return avg_m

x = [x for x in range(0,13)]
seq = [0,1,0,1,1,0,1,1,0,0] # HPHPPHPPHH

g = generateConformations(10,seq)
y = [calcZ(g, e)[0] for e in x]
# plt.plot(x,y, marker='o')
# plt.yscale('log')
# plt.show()

