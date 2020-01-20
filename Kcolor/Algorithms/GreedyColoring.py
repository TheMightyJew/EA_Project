class GreedyColoring:

    def is_valid(self, toColor, color):
        neighbors = toColor.get_neighbors()
        for neigh in neighbors:
            if neigh.get_color() != None and neigh.get_color() == color:
                return False
        return True

    def color_graph_rec(self, node_in_graph, k, index, solutions):

        if index == len(node_in_graph):
            sol = []
            num_to_locations = {}
            count = 0
            for i in range(len(node_in_graph)):
                color = node_in_graph[i].get_color()
                if not color in num_to_locations:
                    num_to_locations[color] = count
                    count = count + 1
                color = num_to_locations[color]
                sol.append(color)
            for solution in solutions:
                if solution == sol:
                    return
            solutions.append(sol)
            return

        for i in range(k):
            toColor = node_in_graph[index]
            if self.is_valid(toColor, i):
                toColor.color_node(i)
                self.color_graph_rec(node_in_graph, k, index + 1, solutions)
                toColor.uncolor_node()
        return

    def color_graph(self, graph, k):
        nodes_in_graph = graph.get_nodes()
        solutions = []
        self.color_graph_rec(nodes_in_graph, k, 0, solutions)
        return nodes_in_graph, solutions
