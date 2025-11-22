import numpy
import scipy
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from node import Node

# sequences are bit strings
def setSequence(graph, seq):
    if len(graph) == len(seq):
        for i in range(len(graph)):
            if seq[i] == 0:
                graph[i].polarity = 'H'
            else:
                graph[i].polarity = 'P'
    else:
        print("Length mismatch")

# def findTopologicalNeighbors(graph):
#     # positions = {n.position for n in graph}
#     h_nodes = [n for n in graph if n.polarity == 'H']
#     h_pos = [n.position for n in h_nodes]
#     visited = set()
#     m = 0
#     for node in h_nodes:
#         visited.add(node)
#         neigh_pos = [n.position for n in node.neighbors]
#         for d in DIRECTIONS:  
#             nxt = add(tuple(node.position), d) # Directions and node.neighbors has upper bound
#             if nxt in h_pos and nxt not in neigh_pos:
#                 if nxt not in visited:
#                     visited.add(nxt)
#                     m += 1

#     return [m,visited]

#Fix later, this looks terrible

def findTopologicalNeighbors(graph):
    visited = set()
    m = 0
    for i in range(len(graph)):
        visited.add(graph[i]) 
        for j in range(len(graph)):
            if graph[j] not in graph[i].neighbors:
                for d in DIRECTIONS:  
                    nxt = add(tuple(graph[i].position), d)
                    if graph[j].position == nxt and graph[j] not in visited:
                        if graph[j].polarity == graph[j].polarity:
                            if graph[i].polarity == 'H':
                                m += 1
    return m

                        

# Chain Generation

# Chain length
# Directions for a 2D square lattice

DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


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

     
g = []
for w in enumerate_saws(10):
    g.append(sawToGraph(w))

b = g[20]
print(findTopologicalNeighbors(b))
# print(len(g))
# Testing neighbor counter

# ma = 0
# for i in g:
#     count = 1
#     print("neighbors: " + str(findTopologicalNeighbors(i)))
#     ma = max(ma, findTopologicalNeighbors(i))
#     for j in i:
#         print("node " + str(count) + " position: " + str(j.position))

# print(ma)

# PLOTTING
x_l = []
y_l = []
plt.figure()
plt.xlim(-10,10)
plt.ylim(-10,10)
for n in b:
        x = list(n.position)[0]
        y = list(n.position)[1]
        x_l.append(x)
        y_l.append(y)
plt.plot(x_l,y_l, marker='.',ms=10)
plt.show()
    # ax = plt.gca()

    # Set major ticks every 1 unit
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(1.0))
    # plt.grid(True)
    # plt.xlim(-3,3)
    # plt.ylim(-3,3)
    # plt.show()


# phi = 0.5

l = {}

# setSequence(b, [0,1,0,1,0,1,0,1,0,1])

# for i in range(len(g)):
#     setSequence(g[i], [0,1,0,1,0,1,0,1,0,1])
#     energy = findTopologicalNeighbors(g[i])
#     if energy not in l:
#         l[energy] = [g[i]]
#     else:
#         temp = l[energy]
#         temp.append(g[i])
#         l[energy] = temp

# x = []
# y = []
# for key in l:
#     y.append(len(l[key])/len(g))
#     x.append(key)

# plt.plot(x,y)
# plt.show()