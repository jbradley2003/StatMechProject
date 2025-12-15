import numpy as np
import matplotlib.pyplot as plt
from node import Node
from setup import *

F = [0,1,0,1,1,0,1,1,0,0]
NF = [1,1,1,1,1,0,0,0,0,0]
DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]

def add(a, b):
    """
    Enables vector addition for tuples.
    
    :param a: Tuple
    :param b: Tuple
    """
    return (a[0] + b[0], a[1] + b[1])

def dot(a, b):
    """
    Enables use of dot product operator for tuples.
    
    :param a: Tuple
    :param b: Tuple
    """
    return a[0]*b[0] + a[1]*b[1]

def dist(a, b):
    """
    Computes distance between input positions (a and b)
    
    :param a: Tuple
    :param b: Tuple
    """
    x1, y1 = a
    x2, y2 = b
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

def enumerate_saws(n):
    """
    Generate all self-avoiding walks of length n on a 2D square lattice
    using depth-first search (DFS).
    
    :param n: Residue count
    """
    start = (0, 0)
    walk = [start]
    occupied = {start}


    def dfs():
        if len(walk) == n:
            yield walk 
            return

        for d in DIRECTIONS:
            nxt = add(walk[-1], d)

            if nxt in occupied:
                continue

            walk.append(nxt)
            occupied.add(nxt)
            yield from dfs()

            walk.pop()
            occupied.remove(nxt)

    yield from dfs()

def sawToGraph(saw):
    """
    Converts a list of positions (tuples) to list of Node objects.
    
    :param saw: List of positions (tuples)
    """
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

def generateCons(n, seq):
    """
    Generate all self-avoiding walks with n residues starting from the origin, (0,0), as graphs.
    
    :param n: Residue count (integer)
    :param seq: Sequence list (list of integers)
    """
    g = []
    for w in enumerate_saws(n):
        h = sawToGraph(w)
        setGraphSequence(h, seq)
        g.append(h)
    return g

def graphEquals(a, b):
    """
    Checks if input graphs are identical.
    
    :param a: Graph (list of Node objects)
    :param b: Graph (list of Node objects)
    """
    for i in range(len(a)):
        if a[i].position != b[i].position:
            return False
    return True

def setGraphSequence(graph, seq):
    """
    Sets polarity labels of all Node objects in a graph according to input sequence.
    
    :param graph: Graph (lists of Node objects)
    :param seq: Sequence list (list of integers)
    """
    if type(graph[0]) is Node:
        if len(graph) == len(seq):
            for i in range(len(graph)):
                if seq[i] == 0:
                    graph[i].polarity = 'H'
                else:
                    graph[i].polarity = 'P'
        else:
            print("Length mismatch")

def setEnsembleSequence(ensemble, seq):
    """
    Sets polarity labels of all Node objects in each graph in the ensemble according to input sequence.
    
    :param ensemble: List of graphs (lists of Node objects)
    :param seq: Sequence list (list of integers)
    """
    if len(ensemble[0]) == len(seq):
        for g in ensemble:
            setGraphSequence(g, seq)
    else:
        print("Length mismatch")

def seqToString(seq):
    """
    Converts a sequence list to a string of corresponding polarity labels.
    
    :param seq: Sequence list (list of integers)
    """
    string = ''
    for n in seq:
        if n == 0:
            string += 'H'
        else:
            string += 'P'
    return string

def getGraphSequence(graph):
    """
    Finds sequence list of an input graph.
    
    :param graph: Graph (list of Node objects)
    """
    seq = []
    for n in graph:
        if n.polarity == 'H':
            seq.append(0)
        else:
            seq.append(1)
    return seq

def findTopolPPNeighbors(graph):
    """
    Finds number of topological P-P contacts in a graph.
    
    :param graph: Graph (list of Node objects)
    """
    p_nodes = [node for node in graph if node.polarity == 'P']
    p_positions = [node.position for node in graph if node.polarity == 'P']
    visited = set()
    m = 0
    for n in p_nodes:
        neigh_positions = [node.position for node in n.neighbors]
        for d in DIRECTIONS:  
            nxt = add(n.position, d)
            if nxt in p_positions and nxt not in neigh_positions:
                pair = frozenset({n.position, nxt})
                if pair not in visited:
                    visited.add(pair)
                    m += 1
    return m

def findTopolHPNeighbors(graph):
    """
    Finds number of topological H-P contacts in a graph.
    
    :param graph: Graph (list of Node objects)
    """
    p_nodes = [node for node in graph if node.polarity == 'P']
    h_positions = [node.position for node in graph if node.polarity == 'H']
    visited = set()
    m = 0
    for n in p_nodes:
        neigh_positions = [node.position for node in n.neighbors]
        for d in DIRECTIONS:  
            nxt = add(n.position, d)
            if nxt in h_positions and nxt not in neigh_positions:
                pair = frozenset({n.position, nxt})
                if pair not in visited:
                    visited.add(pair)
                    m += 1
    return m

def findTopolHHNeighbors(graph):
    """
    Finds number of topological H-H contacts in a graph.
    
    :param graph: Graph (list of Node objects)
    """
    h_nodes = [node for node in graph if node.polarity == 'H']
    h_positions = [node.position for node in graph if node.polarity == 'H']
    visited = set()
    m = 0
    for n in h_nodes:
        neigh_positions = [node.position for node in n.neighbors]
        for d in DIRECTIONS:  
            nxt = add(n.position, d)
            if nxt in h_positions and nxt not in neigh_positions:
                pair = frozenset({n.position, nxt})
                if pair not in visited:
                    visited.add(pair)
                    m += 1
    return m

def findAllTopolNeighbors(graph):
    """
    Returns list containing topological H-H contacts (m) in addition to the sum of H-P and P-P contacts (u).
    
    :param graph: Graph (list of Node objects)
    """
    m = findTopolHHNeighbors(graph)
    u = findTopolHPNeighbors(graph) + findTopolPPNeighbors(graph)
    return [m, u]

def findMinPerim(graph):
    """
    Finds perimeter of maximally compact conformation of input graph.
    
    :param graph: Graph (list of Node objects)
    """
    n = len(graph)
    m = int(np.floor(np.sqrt(n)))

    if m*m == n:
        return 4*m
    elif m*(m+1) >= n:
        return 4*m + 2
    else:
        return 4*(m+1)

def findMaxNeighbors(graph):
    """
    Finds the maximum possible topological neighbors for given graph.
    
    :param graph: Graph (list of Node objects)
    """
    n = len(graph)
    return n + 1 - findMinPerim(graph)/2

def displayConformation(graph):
    """
    Displays input graph on a scatterplot.
    
    :param graph: Graph (list of Node objects)
    """
    x_l = []
    y_l = []
    l = len(graph)

    plt.figure()

    for n in graph:
        x, y = n.position
        x_l.append(x)
        y_l.append(y)

    x_mid = min(x_l) + int((max(x_l)-min(x_l))/2)
    y_mid = min(y_l) + int((max(y_l)-min(y_l))/2)

    # These are useful if the graph is not restricted to a n x n grid.
    # plt.xlim(x_mid - l,x_mid + l)
    # plt.ylim(y_mid - l,y_mid + l)
    plt.xlim(-l, l)
    plt.ylim(-l,l)
    plt.plot(x_l,y_l, marker='.',ms=10)
    plt.grid()
    plt.show()

def printPositions(graph):
    """
    Prints positions of each residue (Node) in a conformation (graph)
    
    :param graph: Graph (list of Node objects)
    """
    for i in range(len(graph)):
        print("Node " + str(i) + ", position: " + str(graph[i].position))

def calcZ(ensemble, neg_espilon=2):
    """
    Calculates the partition function of an input ensemble with an input stabilization energy.
    
    :param ensemble: List of graphs (list of lists of Node objects)
    :param neg_epsilon: Stabilization energy (float)
    """
    max_m = 0
    z = 0
    freq = {}
    for i in ensemble:
        m = findTopolHHNeighbors(i)
        if m in freq:
            freq[m] += 1
        else:
            freq[m] = 1
        max_m = max(m, max_m)
    for i in range(max_m+1):
        if i in freq:
            z += freq[i] * np.exp((max_m-i)*(-neg_espilon))
    return [z, freq, max_m]

def calcAvgP(ensemble, neg_espilon=2):
    """
    Calculates expectation value of compactness for an input ensemble with an input stabilization energy.
    
    :param ensemble: List of graphs (list of lists of Node objects)
    :param neg_espilon: Stabilization energy (float)
    """
    max_m = 0
    avg_p = 0
    max_n = findMaxNeighbors(ensemble[0])
    freq = {}
    
    for i in ensemble:
        m, u = findAllTopolNeighbors(i)
        if (m, u) in freq:
            freq[(m, u)] += 1
        else:
            freq[(m, u)] = 1
        max_m = max(m, max_m)
    for i in range(max_m+1):
        for j in range(max_n+1 - i):
            if (i, j) in freq:
                avg_p += ((i + j)/max_n)*freq[(i, j)] * np.exp((max_m - i)*(-neg_espilon))
            
    return avg_p/calcZ(ensemble, neg_espilon)[0]

def calcNativeP(ensemble):
    """
    Calculates compactness of native conformations in an input ensemble.
    
    :param ensemble: List of graphs (list of lists of Node objects)
    """
    max_m = 0
    p_ns = 0
    z_inf = 0
    max_n = int(findMaxNeighbors(ensemble[0]))
    freq = {}
    for i in ensemble:
        m, u = findAllTopolNeighbors(i)
        if (m, u) in freq:
            freq[(m, u)] += 1
        else:
            freq[(m, u)] = 1
        max_m = max(m, max_m)
    
    for i in range(max_n+1 - max_m):
        if (max_m, i) in freq:
            z_inf += freq[(max_m, i)]
            p_ns += freq[(max_m, i)]*(i + max_m)/max_n
    return p_ns/z_inf

def calcAvgM(ensemble, neg_epsilon=2):
    """
    Calculates expectation value of H-H topological neighbors in an input ensemble.
    
    :param ensemble: List of graphs (list of lists of Node objects)
    :param neg_espilon: Stabilization energy (float)
    """
    [z, freq, max] = calcZ(ensemble, neg_epsilon)
    avg_m = 0
    for i in range(max+1):
        if i in freq:
            avg_m += i * freq[i] * np.exp((max-i)*(-neg_epsilon))
    return avg_m/z