class Node:

    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.color = None

    def get_id(self):
        return self.id

    def get_color(self):
        return self.color

    def color_node(self, color):
        self.color = color

    def uncolor_node(self):
        self.color = None

    def get_neighbors(self):
        return self.neighbors

    def add_neighbor(self, node):
        self.neighbors.append(node)
