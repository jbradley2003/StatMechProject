 
# BEAD CLASS

class Node:
    def __init__(self, loc, pol, neigh):
        self.position = loc
        self.polarity = pol
        self.neighbors = neigh

    def connect(self, node):
        self.neighbors.add(node)

    def isConnected(self, node):
        return node in self.neighbors
    
    def samePolarity(self, node):
        return self.polarity == node.polarity    
    
# TESTING CLASS
a = Node((0,0), 'H', set())
b = Node((0,0), 'H', {a})
a.connect(b)
print(b.samePolarity(a))


# CHAIN GENERATION

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
            yield list(walk)  # return a copy
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



