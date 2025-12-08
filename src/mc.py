import random
import math
import copy
import numpy as np
from node import Node
from setup import *

def main(n, iterations, seq, energy):
    total = []
    g = generateRandCon(n)
    setSequence(g, seq)
    for i in range(iterations):
        rand = random.randrange(n)
        if rand == 0 or rand == n - 1:
            new = endRotation(current, rand)
        else:
            new = cornerFlip(current, rand)
        if accept(current, new, energy) and not graphEquals(new, current):
            total.append(new)
            current = new
            # displayConformation(current)
            # print(findTopolHHNeighbors(current))
    # displayConformation(current)
    print(len(total))
    return total

def generateRandCon(n):
    graph = []
    visited = set()
    for i in range(n):
        if i == 0:
            graph.append(Node((0,0),'H',set()))
            visited.add((0,0))
        else:
            moves = []
            for d in DIRECTIONS:
                temp = add(graph[-1].position, d)
                if temp not in visited:
                    moves.append(temp)
            if len(moves) > 0:
                rand = random.randrange(len(moves))
                nxt = moves[rand]
                visited.add(nxt)
                graph.append(Node(nxt, 'H',set()))
                graph[i].connect(graph[-1])
            else:
                continue
    return graph

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

# Metropolis criteria using U(i) = (s-m_i)*e, where e < 0
def accept(i, j, energy):
    """Metropolis acceptance based on H–H contacts.""" 
    m = findTopolHHNeighbors(j)
    n = findTopolHHNeighbors(i)
    if m >= n:
        return True
    else:
        r = random.random()
        try:
            return np.exp(energy *(n-m)) > r
        except OverflowError: # not sure if this is needed.
            return False
        
# n = 13
# for i in range(10): 
#     displayConformation(generateRandCon(n))


# itr = 300
# seq = [0,1,0,1,1,0,1,1,0,0]
# # main(n, itr, [0]*n)
# g = generateConformations(n, seq)
# # t = np.linspace()
# x = [x for x in range(0,13)]
# y = [calcAvgP(main(n, itr, seq, e), e) for e in x]
# y1 = [calcAvgP(g, e) for e in x]
# plt.plot(x,y, marker='o')
# plt.plot(x,y1, marker='o')
# # plt.yscale('log')
# plt.show()
    
# HPPHPPHPHH
