import random
import math
from numpy import *
from node import Node
from setup import *

DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]

def endRotation(graph):
    node_pos = [n.position for n in graph]
    moves = []
    n = len(graph)
    ran1 = random.randrange(n)
    if ran1 == 0 or ran1 == n:
        bead = graph[n]
        for d in DIRECTIONS:
            nxt = add(bead.position,d)
            if nxt not in node_pos:
                moves.append(nxt)
    if len(moves) < 1:
        return graph
    else:
        ran2 = random.randrange(len(moves))
        copy = graph.copy()
        copy[ran1] = moves[ran2]
        return copy

def generateConformations(n):
    g = []
    for w in enumerate_saws(n):
        g.append(sawToGraph(w))
    return g

def findEnergy():
    

def accept(i, j):
    