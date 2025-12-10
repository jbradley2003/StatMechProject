import random
import copy
import numpy as np
from node import Node
from setup import *

def main(n, iterations, seq, energy):
    total = []
    g = generateRandCon(n)
    count = 2
    start = len(g)
    while start < n:
        print("Attempt #" + str(count))
        g = generateRandCon(n)
        start = len(g)
        count += 1
    setGraphSequence(g, seq)
    total.append(g)
    current = g
    for i in range(iterations):
        rand = random.randrange(n)
        if rand == 0 or rand == n - 1:
            new = endRotation(current, rand)
        else:
            new = cornerFlip(current, rand)
        if accept(current, new, energy) and not graphEquals(new, current):
            total.append(new)
            current = new
    return total

def generateRandCon(n):
    pos = [(0,0)]
    visited = set()
    for i in range(n-1):
        moves = []
        for d in DIRECTIONS:
            temp = add(pos[-1], d)
            if temp not in visited:
                moves.append(temp)
        if len(moves) > 0:
            rand = random.randrange(len(moves))
            nxt = moves[rand]
            visited.add(nxt)
            pos.append(nxt)
        else:
            return [(0,0)]
    return sawToGraph(pos)

def endRotation(graph,n):
    node_pos = {b.position for b in graph}
    moves = []
    g = copy.deepcopy(graph)
    bead = g[n]
    neigh = next(iter(bead.neighbors)).position
    for d in DIRECTIONS:
        nxt = add(neigh,d)
        if nxt not in node_pos:
            moves.append(nxt)
    if len(moves) < 1:
        return g
    else:
        rand = random.randrange(len(moves))
        g[n].position = moves[rand]
        return g
    
def cornerFlip(graph, n):
    node_pos = {b.position for b in graph}
    g = copy.deepcopy(graph)
    bead = g[n]
    if len(bead.neighbors) < 2:
        return g
    node = bead.neighbors.copy()
    a = node.pop().position
    b = node.pop().position
    a_vec = (a[0]-bead.position[0], a[1]-bead.position[1])
    b_vec = (b[0]-bead.position[0], b[1]-bead.position[1])
    new_pos = add(bead.position, add(a_vec, b_vec))
    if dot(a_vec, b_vec) == 0 and new_pos not in node_pos:
        bead.position = new_pos
    return g

# def calcZ()

# Metropolis criteria using U(i) = -e(s-m_i), where e > 0
def accept(i, j, energy):
    """Metropolis acceptance based on H–H contacts.""" 
    m = findTopolHHNeighbors(j)
    n = findTopolHHNeighbors(i)
    if m >= n:
        return True
    else:
        r = random.random()
        try:
            return np.exp(-energy *(n-m)) > r
        except OverflowError: # not sure if this is needed.
            return False



