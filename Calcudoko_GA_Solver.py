import random
import numpy
import time
import math
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import Calcudoku


# This class represents a Calcudoku solver using GA"
class Calcudoku_GA_Solver:

    # The constructor of the class
    def __init__(self, board_size, constraints):
        self.board_size = board_size
        self.constraints = constraints

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        self.toolbox = base.Toolbox()
        self.toolbox.register("Initialization", self.initiate_first_generation)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.Initialization)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.evaluate_board)
        self.toolbox.register("mate", self.crossover)
        self.toolbox.register("mutate", self.mut_shuffle)
        self.toolbox.register("select", tools.selTournament, tournsize=10)

    # This function will solve the calcudoku with the given parameters:
    # population - The size of the population
    # generations - The number of generations until we stop the algorithm
    # mutation_p - The probability for a mutation in an individual
    # crossover_p - The probability for a crossover between two individuals
    def solve(self, population, generations, mutation_p, crossover_p):

        pop = self.toolbox.population(n=population)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("Avg", numpy.mean)
        stats.register("Median", numpy.median)
        stats.register("Best", numpy.min)
        stats.register("Worst", numpy.max)
        start_time = time.time();

        algorithms.eaSimple(pop, self.toolbox, cxpb=crossover_p, mutpb=mutation_p, ngen=generations,
                            stats=stats, halloffame=hof, verbose=True)

        elapsed_time = time.time() - start_time
        print('%.2f  seconds' % elapsed_time)

        return pop, stats, hof

    # The initialization operator - This function will create a board with the following features:
    # Each row contains each number once
    # Each column contains each number once
    def initiate_first_generation(self):
        board = self.random_creation(self.board_size)
        return Calcudoku.convert_to_array(board)

    # This function will create a board where each row and col are permutation
    def random_creation(self, n):
        # todo dont try to solve soduko
        b = [None] * n
        b[0] = random.sample(range(1, n+1), n)
        for i in range(1, n):
            b[i] = random.sample(range(1, n+1), n)
            while not self.valid_insertion(b, i):
                b[i] = random.sample(range(1, n+1), n)

        return b


    # This function will check if in each column in the board there are only unique values.
    # We will scan the column from row 0 to row "row_index"
    def valid_insertion(self, board, row_index):
        for i in range(len(board[0])):
            col_values = []
            for j in range(row_index + 1):
                col_values.append(board[j][i])
            if len(set(col_values)) != len(col_values):
                return False
        return True

    # This function represents the mutation operator.
    def mut_shuffle(self, individual):
        board = Calcudoku.convert_to_table(individual)
        board = self.change_cells(board)
        array = Calcudoku.convert_to_array(board)
        for index in range(len(array)):
            individual[index] = array[index]
        return individual,

    def change_row_column(self, board):
        first_index = random.randrange(len(board))
        second_index = self.get_random(len(board), first_index)
        if random.random() < 0.5:
            board = self.change_two_columns(board, first_index, second_index)
        else:
            board = self.change_two_rows(board, first_index, second_index)
        return board


    def change_two_rows(self, board, first_index, second_index):
        tmp = board[second_index]
        board[second_index] = board[first_index]
        board[first_index] = tmp
        return board

    def change_two_columns(self, board, first_index, second_index):
        for index in range(len(board)):
            tmp = board[index][second_index]
            board[index][second_index] = board[index][first_index]
            board[index][first_index] = tmp
        return board

    def change_cells(self, board):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if random.random() < 0.05 :
                    board[i][j] = random.randrange(1, self.board_size + 1)
        return board

    def get_random(self, num_range, first_index):
        random_index = random.randrange(num_range)
        while random_index == first_index:
            random_index = random.randrange(num_range)
        return random_index

    def constraints_crossover(self, first_individual, second_individual):
        random_index = random.randrange(1, len(self.constraints) - 1)
        for i in range(random_index, len(self.constraints)):
            for index in self.constraints[i][2]:
                tmp = first_individual[index]
                first_individual[index] = second_individual[index]
                second_individual[index] = tmp
        return first_individual, second_individual

    def rows_columns_crossover(self, first_individual, second_individual):
        random_index = random.randrange(1, self.board_size - 1)
        index = random_index * self.board_size
        if random.random() < 0.5:
            first_board = Calcudoku.convert_to_table(first_individual)
            second_board = Calcudoku.convert_to_table(second_individual)
            for row_index in range(self.board_size):
                for col_index in range(random_index, self.board_size):
                    tmp = first_board[row_index][col_index]
                    first_board[row_index][col_index] = second_board[row_index][col_index]
                    second_board[row_index][col_index] = tmp
            first_board = Calcudoku.convert_to_array(first_board)
            second_board = Calcudoku.convert_to_array(second_board)
            for i in range(len(first_board)):
                first_individual[i] = first_board[i]
                second_individual[i] = second_board[i]
        else:
            first_individual[index:], second_individual[index:] = second_individual[index:], first_individual[index:]
        return first_individual, second_individual

    # This function represents the crossover operator.
    def crossover(self, first_individual, second_individual):
        first_individual, second_individual = self.constraints_crossover(first_individual, second_individual)
        return first_individual, second_individual

    # This function represents the fitness function
    def evaluate_board(self, individual):
        return Calcudoku.count_all_duplicates(individual)[1] + Calcudoku.check_fault_constraints(individual, self.constraints),


# The main
def main():
    board_size = 6
    true_solution, constraints = Calcudoku.generate_board_in_size(board_size)
    solver = Calcudoku_GA_Solver(board_size, constraints)
    pop, stats, hof = solver.solve(100, 1000, 1, 0.7)
    print("Our Solution:")
    Calcudoku.print_board(Calcudoku.convert_to_table(hof[0]))
    print()
    Calcudoku.print_board(true_solution)
    print()
    print(constraints)


if __name__ == "__main__":
    main()
