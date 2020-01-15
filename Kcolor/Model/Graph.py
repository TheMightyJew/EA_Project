from Kcolor.Model.Node import Node


class Graph:

    def __init__(self, partition, size):
        self.size = size
        self.id_to_node = {}
        for i in range(len(partition)):
            id = partition[i][0] * size + partition[i][1]
            self.id_to_node[id] = Node(id)
        connected = []
        for i in range(len(partition)):
            id = partition[i][0] * size + partition[i][1]
            to_connect = self.id_to_node.get(id)
            for j in range(i):
                connected_with = connected[j]
                if self.to_connect(to_connect, connected_with):
                    to_connect.add_neighbor(connected_with)
                    connected_with.add_neighbor(to_connect)
            connected.append(to_connect)

    def to_connect(self, node1, node2):
        x1 = int(node1.get_id() / self.size)
        y1 = int(node1.get_id() % self.size)
        x2 = int(node2.get_id() / self.size)
        y2 = int(node2.get_id() % self.size)
        return x1 == x2 or y1 == y2

    def get_nodes(self):
        return list(self.id_to_node.values())
