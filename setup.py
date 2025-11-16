 
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

    
# Testing
# a = Node((0,0), 'H', set(),0)
# b = Node((0,0), 'H', {a},1)
# a.connect(b)
# print(b.samePolarity(a))


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
            # Node(loc, polarity, neighbors_set, start_flag)
            g.append(Node(b, 'H', set(), 1))
        else:
            g.append(Node(b, 'H', set(), 0))
            g[i].connect(g[i-1])
        i += 1
    return g

g = []
for w in enumerate_saws(3):
    g.append(sawToGraph(w))

for gr in g:
    print('new graph')
    for n in gr:
        print(n.position)
        print()
        print(n.isStart())