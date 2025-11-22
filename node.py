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