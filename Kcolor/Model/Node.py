"""
This class represents a node
"""
class Node:
    """
    The constructor of the class
    """
    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.color = None
    """
    This function returns the id of the node
    """
    def get_id(self):
        return self.id

    """
    This function returns the color of the node
    """
    def get_color(self):
        return self.color

    """
    This function will color the node
    """
    def color_node(self, color):
        self.color = color

    """
    This function will uncolor the node
    """
    def uncolor_node(self):
        self.color = None

    """
    This function will return all the neighbors of the node
    """
    def get_neighbors(self):
        return self.neighbors

    """
    This function will add a given node as this node's neighbors
    """
    def add_neighbor(self, node):
        self.neighbors.append(node)
