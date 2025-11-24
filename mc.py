import random
import math
import copy
# from numpy import *
from node import Node
from setup import *

DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]

def main(size, iterations, seq):
    # l = [n for n in range(1,size-1)]
    g = generateConformations(size)
    ensemble = set()
    total = []
    current = g[0]
    setSequence(current, seq)
    displayConformation(current)
    for i in range(iterations):
        rand = random.randrange(size)
        # rand = random.choice(l)
        if rand == 0 or rand == size - 1:
            new = endRotation(current, rand)
            pass
        else:
            new = cornerFlip(current, rand)
        if accept(current, new):
            total.append(new) # how does allowing duplicates influence average values?
            current = new
            print(findTopolHHNeighbors(current))
    displayConformation(current)
    print(seq)
    return total


def endRotation(graph, n):
    # n is an endpoint: degree = 1
    g = copy.deepcopy(graph)
    bead = g[n]
    node_pos = {b.position for b in g}

    # get the only neighbor
    nbr = next(iter(bead.neighbors))
    nx, ny = nbr.position

    # potential new positions: all 4 directions around the neighbor
    candidates = [(nx+dx, ny+dy) for dx,dy in DIRECTIONS]

    # cannot stay on top of neighbor or collide with any bead
    valid = [p for p in candidates if p != bead.position and p not in node_pos]

    # If no valid moves, return unchanged
    if not valid:
        return g

    bead.position = random.choice(valid)
    return g

# def endRotation(graph,n):
#     node_pos = [b.position for b in graph]
#     moves = []
#     bead = graph[n]
#     for d in DIRECTIONS:
#         nxt = add(next(iter(bead.neighbors)).position,d)
#         if nxt not in node_pos:
#             moves.append(nxt)
#     if len(moves) < 1:
#         return graph
#     else:
#         rand = random.randrange(len(moves))
#         graph[n].position = moves[rand]
#         return graph
    
def cornerFlip(graph, n):
    g = copy.deepcopy(graph)
    bead = g[n]
    node_pos = {b.position for b in g}

    # must have 2 neighbors
    if len(bead.neighbors) != 2:
        return g

    a, b = list(bead.neighbors)

    ax, ay = a.position
    bx, by = b.position
    nx, ny = bead.position

    # must be orthogonal: (a-n) and (b-n) must not be colinear
    if (ax == nx and bx == nx) or (ay == ny and by == ny):
        # neighbors are colinear → no corner → no flip
        return g

    # geometry of corner flip:
    new_pos = (ax + bx - nx, ay + by - ny)

    # new position must be empty
    if new_pos in node_pos:
        return g

    bead.position = new_pos
    return g

# def cornerFlip(graph, n):
#     node_pos = [b.position for b in graph]
#     bead = graph[n]
#     x = 0
#     y = 0
#     if len(bead.neighbors) < 2:
#         return graph
#     g = bead.neighbors.copy()
#     a = g.pop()
#     b = g.pop()
#     if a.position[0] != b.position[0] and a.position[1] != b.position[1]:   
#         if add(bead.position, (1,0)) in node_pos:
#             x = bead.position[0] + 1
#         if add(bead.position, (-1,0)) in node_pos:
#             x = bead.position[0] - 1
#         if add(bead.position, (0,1)) in node_pos:
#             y = bead.position[1] + 1
#         if add(bead.position, (0,-1)) in node_pos:
#             y = bead.position[1] - 1
#         graph[n].position = (x,y)
#     return graph



# Metropolis criteria using U(i) = (s-m_i)*e, where e < 0
def accept(i, j, energy=-20):
    """Metropolis acceptance based on H–H contacts.""" 
    m = findTopolHHNeighbors(j)
    n = findTopolHHNeighbors(i)
    if m >= n:
        return True
    else:
        r = random.random()
        try:
            return math.exp(energy *(n-m)) > r
        except OverflowError: # not sure if this is needed.
            return False
        

    
# HPPHPPHPHH
