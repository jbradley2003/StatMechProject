import numpy
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scipy

# Protein Monomer Class

class Node:
    def __init__(self, loc, pol, neigh, start):
        self.position = loc
        self.polarity = pol
        self.neighbors = neigh
        self.first = start

    def connect(self, node):
        self.neighbors.add(node)
        node.neighbors.add(self)

    def isConnected(self, node):
        return node in self.neighbors
    
    def samePolarity(self, node):
        return self.polarity == node.polarity

    def isStart(self):
        return self.first == 1

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

# def findTopolNeighbors(graph):
#     visited = set()
#     m = 0
#     for i in range(len(graph)):
#         visited.add(graph[i])
#         for d in DIRECTIONS:  
#             nxt = add(tuple(graph[i].position), d)
#             for 

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
            g.append(Node(b, 'H', set(), 1))
        else:
            g.append(Node(b, 'H', set(), 0))
            g[i].connect(g[i-1])
        i += 1
    return g

     
g = []
for w in enumerate_saws(4):
    g.append(sawToGraph(w))

# ma = 0
# for i in g:
#     count = 1
#     print("neighbors: " + str(findTopologicalNeighbors(i)))
#     ma = max(ma, findTopologicalNeighbors(i))
#     for j in i:
#         print("node " + str(count) + " position: " + str(j.position))

# print(ma)

plt.figure()
for w in g:
    x_l = []
    y_l = []
    for n in w:
        x = list(n.position)[0]
        y = list(n.position)[1]
        x_l.append(x)
        y_l.append(y)
    plt.plot(x_l,y_l, marker='.',ms=10)
    ax = plt.gca()

    # Set major ticks every 1 unit
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(1.0))
    # plt.grid(True)
    plt.xlim(-3,3)
    plt.ylim(-3,3)
    plt.show()

