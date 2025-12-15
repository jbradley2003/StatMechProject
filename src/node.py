# Node class designed to represent the constituent residues of a protein.
class Node:
    def __init__(self, loc, pol, neigh):
        """
        Create a Node object.
        
        :param self: Initialized Node object
        :param loc: Node position (tuple)
        :param pol: Node polarity (string)
        :param neigh: Connected Node objects (set)
        """
        self.position = loc
        self.polarity = pol
        self.neighbors = neigh

    def connect(self, node):
        """
        Forms an edge with another input Node.
        
        :param self: Node object from which edge is being formed.
        :param node: Other Node object.
        """
        self.neighbors.add(node)
        node.neighbors.add(self)

    def isConnected(self, node):
        """
        Returns True if input Node is in the adjacency set of given Node.
        
        :param self: Node object (its adjacency set is searched) 
        :param node: Other Node object
        """
        return node in self.neighbors
    
    def samePolarity(self, node):
        """
        Checks if input Node object has same polarity as given Node.
        
        :param self: Node object (primary polarity label)
        :param node: Other Node object
        """
        return self.polarity == node.polarity 