import random
import numpy
import time
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import Calcudoku
from Kcolor.Model.Graph import Graph
from Kcolor.Algorithms.GreedyColoring import GreedyColoring


"""
 This class represents a Calcudoku solver using GA"
"""
class Calcudoku_GA_Solver:

    """
    The constructor of the class
    """
    def __init__(self, board_size=6):
        self.board_size = board_size
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        self.toolbox = base.Toolbox()
        self.toolbox.register("Initialization", self.initiate_first_generation)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.Initialization)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.evaluate_board)
        self.toolbox.register("mate", self.crossover)
        self.toolbox.register("mutate", self.mut_shuffle)
        self.toolbox.register("select", tools.selTournament, tournsize=5)

    """
    This function constraints and generates the possible assignments for cages
    """
    def set_constraints(self, constraints):
        self.constraints = constraints
        self.possible_assignments = self.possible_assignment_partitions()


    """
    This function returns all the possible assignments for the cages in the puzzle
    """
    def possible_assignment_partitions(self):
        list_partition_to_possible_assignment_value = []
        list_partition_to_possible_assignment_structure = []
        for i in range(len(self.constraints)):
            vals, structure = self.possible_assignment_for_partition(self.constraints[i])
            list_partition_to_possible_assignment_value.append(vals)
            list_partition_to_possible_assignment_structure.append(structure)
        return self.build_complete_possible_assignments(list_partition_to_possible_assignment_structure,
                                                        list_partition_to_possible_assignment_value)

    """
    This function recieves the possible structures and values for the cages and returns the complete assignments
    """
    def build_complete_possible_assignments(self, possible_assignment_structure,
                                            possible_assignment_vals):
        complete_possible_assignments = []
        for i in range(len(self.constraints)):
            complete_assignment_for_structure_list = []
            for assignment_structure_index in range(len(possible_assignment_structure[i])):
                for assignment in possible_assignment_vals[i][assignment_structure_index]:
                    if len(assignment) > 0:
                        complete_assignment = []
                        for index in possible_assignment_structure[i][assignment_structure_index]:
                            complete_assignment.append(assignment[index])
                        complete_assignment_for_structure_list.append(complete_assignment)
            complete_possible_assignments.append(complete_assignment_for_structure_list)
        return self.fix(complete_possible_assignments)

    """
    This function receives a partition and returns all the possible assignments for it
    """
    def possible_assignment_for_partition(self, partition):

        partition_list = []
        for i in range(len(partition[2])):
            x = int(partition[2][i] / self.board_size)
            y = int(partition[2][i] % self.board_size)
            partition_list.append((x, y))

        graph = Graph(partition_list, self.board_size)
        greedyColoring = GreedyColoring()
        nodes_in_graph, solutions = greedyColoring.color_graph(graph, self.board_size)
        possible = []
        for solution in solutions:
            dictionary_color_to_location = {}
            for i in range(len(solution)):
                node = nodes_in_graph[i]
                x = int(node.get_id() / self.board_size)
                y = int(node.get_id() % self.board_size)
                if not solution[i] in dictionary_color_to_location:
                    dictionary_color_to_location[solution[i]] = []
                locations = dictionary_color_to_location[solution[i]]
                locations.append((x, y))
            possible.append(list(dictionary_color_to_location.values()))
        possible_vals = Calcudoku.partition_possible_values(len(partition[2]), partition[1], partition[0],
                                                            self.board_size, possible)
        return possible_vals, solutions

    """
    This function will solve the calcudoku with the given parameters:
    population - The size of the population
    generations - The number of generations until we stop the algorithm
    mutation_p - The probability for a mutation in an individual
    crossover_p - The probability for a crossover between two individuals
    """
    def solve(self, population_size, generations, crossover_p, mutation_p, change_constraint_p, max_without_improvment,
              max_time_per_run):
        self.change_constraint_p = change_constraint_p
        start_time = time.time();
        while True:
            if time.time() - start_time > max_time_per_run:
                break
            pop = self.toolbox.population(n=population_size)
            hof = tools.HallOfFame(1)
            stats = tools.Statistics(lambda ind: ind.fitness.values)
            stats.register("Avg", numpy.mean)
            stats.register("Median", numpy.median)
            stats.register("Best", numpy.min)
            stats.register("Worst", numpy.max)
            population, logbook = algorithms.eaSimple(pop, self.toolbox, cxpb=crossover_p, mutpb=mutation_p,
                                                      ngen=generations, max_without_improvment=max_without_improvment,
                                                      stats=stats, halloffame=hof, verbose=False)
            if logbook[len(logbook) - 1]['Best'] == 0:
                break

        elapsed_time = time.time() - start_time
        print('Total %.2f  seconds' % elapsed_time)
        print()
        return pop, stats, hof, elapsed_time
    """
     The initialization operator - This function will create a board with the following features:
     Each row contains each number once
     Each column contains each number once
    """
    def initiate_first_generation(self):
        board = [0] * pow(self.board_size, 2)
        board = self.change_constraints_assignments(board, 1)
        return board
    """
    This function assigns a possible value for all partitions in the board
    in the given probability
    """
    def change_constraints_assignments(self, board, probability):
        for constraint_index in range(len(self.constraints)):
            if random.random() < probability:
                constraint = self.constraints[constraint_index]
                chosen_assignment = self.possible_assignments[constraint_index][
                    random.randrange(len(self.possible_assignments[constraint_index]))]
                for location_index in range(len(constraint[2])):
                    board[constraint[2][location_index]] = chosen_assignment[location_index]
        return board
    """
    This function represents the mutation operator.
    """
    def mut_shuffle(self, individual):
        self.change_constraints_assignments(individual, self.change_constraint_p)
        return individual,

    """
    This function will preform crossover between two partitions in two individuals
    """
    def constraints_crossover(self, first_individual, second_individual):
        random_index = random.randrange(1, len(self.constraints) - 1)
        for i in range(random_index, len(self.constraints)):
            for index in self.constraints[i][2]:
                tmp = first_individual[index]
                first_individual[index] = second_individual[index]
                second_individual[index] = tmp
        return first_individual, second_individual


    """
    This function represents the crossover operator.
    """
    def crossover(self, first_individual, second_individual):
        first_individual, second_individual = self.constraints_crossover(first_individual, second_individual)
        return first_individual, second_individual


    """
    This function represents the fitness function
    """
    def evaluate_board(self, individual):
        return Calcudoku.count_all_duplicates(individual)[1],

    """
    Remove assignment that are conflicted with "must have pairs" values until there are no more
    """
    def fix(self, complete_possible_assignments):
        removed = -1
        new_complete_possible_assignments = complete_possible_assignments
        while removed != 0:
            must_pairs = self.find_must_pairs(new_complete_possible_assignments)
            new_complete_possible_assignments, removed = self.remove_violating_assignments(
                new_complete_possible_assignments, must_pairs)
        return new_complete_possible_assignments

    """
      Remove assignment that are conflicted with "must have pairs" values
    """
    def remove_violating_assignments(self, old_complete_possible_assignments, must_pairs):
        removed = 0
        new_complete_possible_assignments = []
        for constraint_index in range(len(self.constraints)):
            new_constraint_assignments = []
            for assignment in old_complete_possible_assignments[constraint_index]:
                violates = False
                for index in range(len(self.constraints[constraint_index][2])):
                    location = self.constraints[constraint_index][2][index]
                    for pair_location, pair_value in must_pairs.items():
                        if (pair_location % self.board_size == location % self.board_size or int(
                                pair_location / self.board_size) == int(
                            location / self.board_size)) and pair_location != location:
                            if pair_value == assignment[index]:
                                violates = True
                                removed += 1
                                break
                    if violates:
                        break
                if not violates:
                    new_constraint_assignments.append(assignment)
            new_complete_possible_assignments.append(new_constraint_assignments)
        return new_complete_possible_assignments, removed

    """
    This function finds all "must have pairs"
    """
    def find_must_pairs(self, complete_possible_assignments):
        must_pairs = {}
        for constraint_index in range(len(self.constraints)):
            list = complete_possible_assignments[constraint_index]
            for index in range(len(self.constraints[constraint_index][2])):
                last = None
                constant = True
                for assignment in list:
                    if assignment[index] != last:
                        if last is None:
                            last = assignment[index]
                        else:
                            constant = False
                            break
                if constant:
                    must_pairs[self.constraints[constraint_index][2][index]] = last
        return must_pairs

"""
This function tests the GA model with the given parameterss
"""
def test(board_size=7, max_time_per_run=60 * 10, number_of_runs=10):
    solver = Calcudoku_GA_Solver(board_size)
    total_time = 0
    counter = 0
    timestamp = time.strftime('%b_%d_%Y_%H%M%S', time.localtime())
    file = open("Results_" + str(timestamp) + ".txt", 'a')
    file.write("Results on Calcudokus of size:" + str(board_size) + "\n")
    file.write("Time limit per run: 10 minutes\n\n")
    for i in range(number_of_runs):
        true_solution, constraints = Calcudoku.generate_board_in_size(board_size)
        file.write("\n")
        file.write("Test " + str(i) + ":\n")
        file.write("Constraints: " + str(constraints) + "\n")
        print()
        print("Run number " + str(i))
        solver.set_constraints(constraints)
        print(constraints)
        print()
        pop, stats, hof, elapsed_time = solver.solve(100, 500, 0.8, 1, 0.1, 30, max_time_per_run)
        print(hof[0])
        Calcudoku.print_board(Calcudoku.convert_to_table(hof[0]))
        if elapsed_time < max_time_per_run:
            counter += 1
            total_time += elapsed_time
            file.write("Success: " + str(round(elapsed_time, 2)) + " seconds\n")
        else:
            file.write("Failed\n")
    if counter > 0:
        average_time = round(total_time / counter, 2)
    else:
        average_time = 0
    file.write("\n")
    file.write("Successes: " + str(counter) + "\n")
    file.write("Fails: " + str(number_of_runs - counter) + "\n")
    file.write("Average success run time : " + str(average_time) + "\n")
    file.close()


"""
The main
"""
def main():
    test()


if __name__ == "__main__":
    main()
