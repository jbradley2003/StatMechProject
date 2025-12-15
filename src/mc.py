import random
import copy
import numpy as np
from setup import *

def main(n, iterations, seq, neg_epsilon):
    """
    Produces ensemble of conformations through Monte Carlo importance sampling over the 
    input number of iterations where each conformation is set to have the input sequence
    and H-H contacts correspond to the input stabilization energy (neg_epsilon).
    
    :param n: Residue count (integer)
    :param iterations: Number of attempted moves from random starting conformation (integer)
    :param seq: Sequence list (list of integers)
    :param neg_epsilon: Stabilization energy (float)
    """
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
            new = endMove(rand, current)
        else:
            new = cornerMove(rand, current)
        if accept(current, new, neg_epsilon) and not graphEquals(new, current):
            total.append(new)
            current = new
            displayConformation(current)
    return total

def accept(i, j, neg_epsilon):
    """
    Returns True if Metropolis acceptance criteria is satisfied (energy is minimized between moves 
    or random number is greater than energetically uphill move probability), otherwise False is returned.
    
    :param i: Graph before attempted move (list of Node objects)
    :param j: Graph after attempted move (list of Node objects)
    :param neg_epsilon: Stabilization energy (float)
    """
    m = findTopolHHNeighbors(j)
    n = findTopolHHNeighbors(i)
    if m >= n:
        return True
    else:
        r = random.random()
        return np.exp(-neg_epsilon*(n-m)) > r

def generateRandCon(n):
    """
    Generates a random starting conformation with input residue count.
    
    :param n: Residue count (integer)
    """
    pos = [(0,0)]
    visited = {(0,0)}
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

def boundsCheck(n, position):
    """
    Returns True if Node position exists within an n x n grid, 
    False otherwise.
    
    :param n: Grid parameter (integer)
    :param position: Node position (tuple) 
    """
    x, y = position
    if x > n or x < -n:
        return False
    if y > n or y < -n:
        return False
    return True

def endRotation(n, graph):
    """
    Attempts to perform a rotation move on a random leaf Node (adjacency set has a length of 1) in the graph.
    
    :param n: Chosen bead index (integer)
    :param graph: Graph (list of Node objects)
    """
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

def cornerFlip(n, graph):
    """
    Attempts to perform a corner flip move on a random non-leaf Node in the graph.
    
    :param n: Chosen bead index (integer)
    :param graph: Graph (list of Node objects)
    """
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

#----------------------------------------------------------------------------------#
# These versions restrict the moves to a n x n grid.

def endMove(n, graph): 
    node_pos = {b.position for b in graph}
    moves = []
    g = copy.deepcopy(graph)
    bead = g[n]
    neigh = next(iter(bead.neighbors)).position
    for d in DIRECTIONS:
        nxt = add(neigh,d)
        if nxt not in node_pos and boundsCheck(len(graph),nxt) is True:
            moves.append(nxt)
    if len(moves) < 1:
        return g
    else:
        rand = random.randrange(len(moves))
        g[n].position = moves[rand]
        return g
    
def cornerMove(n, graph):
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
    if dot(a_vec, b_vec) == 0 and new_pos not in node_pos and boundsCheck(len(graph),new_pos) is True:
        bead.position = new_pos
    return g
#----------------------------------------------------------------------------------#
