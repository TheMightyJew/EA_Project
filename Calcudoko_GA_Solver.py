import random
import numpy
import time

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import Calcudoku


class Calcudoku_GA_Solver:

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
        self.toolbox.register("select", tools.selTournament, tournsize=3)


    """
    This function will convert the array to a 2D table
    """

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

    def initiate_first_generation(self):
        board = self.random_creation(self.board_size)
        return Calcudoku.convert_to_array(board)

    def random_creation(self, n):
        b = [None] * n
        b[0] = random.sample(range(1, n+1), n)
        for i in range(1, n):
            b[i] = random.sample(range(1, n+1), n)
            while not self.valid_insertion(b, i):
                b[i] = random.sample(range(1, n+1), n)
        return b

    def valid_insertion(self, board, row_index):
        for i in range(len(board[0])):
            col_values = []
            for j in range(row_index + 1):
                col_values.append(board[j][i])
            if len(set(col_values)) != len(col_values):
                return False
        return True

    def mut_shuffle(self, individual):
        board = Calcudoku.convert_to_table(individual)
        row_index = random.randrange(len(board))
        first_col_index = random.randrange(len(board[row_index]))
        second_col_index = random.randrange(len(board[row_index]))
        while first_col_index == second_col_index:
            second_col_index = random.randrange(len(board[row_index]))
        tmp = board[row_index][second_col_index]
        board[row_index][second_col_index] = board[row_index][first_col_index]
        board[row_index][first_col_index] = tmp
        array = Calcudoku.convert_to_array(board)
        for index in range(len(array)):
            individual[index] = array[index]
        return individual,

    def crossover(self, first_individual, second_individual):
        random_row_index = random.randrange(1, self.board_size - 1)
        index = random_row_index * self.board_size
        tmp = first_individual
        first_individual[index:], second_individual[index:] = second_individual[index:], first_individual[index:]
        return first_individual, second_individual

    def evaluate_board(self, individual):
        return Calcudoku.count_all_duplicates(individual)[1]*self.board_size + Calcudoku.check_fault_constraints(individual, self.constraints),


def main():
    board_size = 4
    true_solution, constraints = Calcudoku.generate_board_in_size(board_size)
    solver = Calcudoku_GA_Solver(board_size, constraints)
    pop, stats, hof = solver.solve(100, 500, 0.01, 0.7)
    Calcudoku.print_board(Calcudoku.convert_to_table(hof[0]))
    print()
    Calcudoku.print_board(true_solution)
    print()
    print(constraints)

if __name__ == "__main__":
    main()