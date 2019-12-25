from calcudoku.game import Calcudoku


"""
This function will convert the array to a 2D table
"""
def convert_to_table(array):
    table = []
    n = int((len(array))** 0.5)
    for i in range(0,n):
        line = []
        for j in range(0,n):
            line.append(array[i*n+j])
        table.append(line)
    return table
"""
This function will convert the array to a 2D table
"""
def convert_to_array(table):
    n = int((len(table))** 2)
    table_length = len(table)
    array = []
    for i in range(0,n):
        array.append(table[int(i/table_length)][i%table_length])
    return array

"""
This function will print the board
"""
def print_board(board):

    for line in board:
        print(line)

"""
This function extracts the constraints from the operations and partitions
"""
def get_constraints(operations, partitions):
    constraints = []
    for i in range(0,len(operations)):
        constraints.append((operations[i][0],operations[i][1],partitions[i]))
    return constraints


"""
This function represents the sum operator
"""


def operator_sum(board, indexes_list):
    sum = 0
    for index in indexes_list:
        sum += board[index]
    return sum

"""
This function represents the multiplication operator
"""
def operator_mult(board, indexes_list):
    multiplication = 1
    for index in indexes_list:
        multiplication *= board[index]
    return multiplication

"""
This function returns the minimum and maximum numbers in a given list
"""
def get_min_max_by_indexes(board, indexes_list):
    maxNum = None
    minNum = None
    for index in indexes_list:
        value = board[index]
        if maxNum == None or minNum == None:
            minNum = value
            maxNum = value
        else:
            minNum = min(minNum, value)
            maxNum = max(maxNum, value)
    return minNum, maxNum

"""
This function represents the subtraction operator
"""
def operator_sub(board, indexes_list):
    minNum, maxNum = get_min_max_by_indexes(board, indexes_list)
    return maxNum - minNum

"""
This function represents the division operator 
"""
def operator_divide(board, indexes_list):
    minNum, maxNum = get_min_max_by_indexes(board, indexes_list)
    return maxNum / minNum

def operator_none(board, indexes_list):
    return board[indexes_list[0]]

operators_dict = {'subtract': operator_sub, 'multiply': operator_mult, 'add': operator_sum, 'divide': operator_divide,'none':operator_none}


def count_duplicates(numbers_list):
    duplicates_count = 0
    num_set = []
    for num in numbers_list:
        if num in num_set:
            duplicates_count += 1
        else:
            num_set.append(num)
    return duplicates_count


def count_all_duplicates(board):
    size = int(len(board) ** 0.5)
    duplicates_count = 0
    bad_rows = 0
    bad_columns = 0
    for index in range(size):
        boardRow = board[size * index:size * (index + 1)]
        duplicates = count_duplicates(boardRow)
        duplicates_count += duplicates
        bad_rows += min(1, duplicates)
        boardColumn = []
        for secondIndex in range(size):
            boardColumn.append(board[index + size * secondIndex])
        duplicates = count_duplicates(boardColumn)
        duplicates_count += duplicates
        bad_columns += min(1, duplicates)
    return duplicates_count, bad_rows + bad_columns

"""
This function will generate a board in the given size
The function will return the solved board and its constraints
"""
def generate_board_in_size(board_size):
    game = Calcudoku.generate(board_size)
    board = convert_to_table(game.board)
    print_board(board)
    constraints = get_constraints(game.operations, game.partitions)
    return board, constraints

board_sol, constraints = generate_board_in_size(6)
print(constraints)

def check_fault_constraints(board):
    print(constraints)
    faults_num = 0
    for constraint in constraints:
        if constraint[1] != operators_dict[constraint[0]](board, constraint[2]):
            print(constraint)
            faults_num += 1
    return faults_num
"""
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("Initialization", initiate_first_generation)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.Initialization)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", eval_path)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", mut_shuffle)
toolbox.register("select", tools.selTournament, tournsize=3)
"""

def main():
    """
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", numpy.mean)
    stats.register("Median", numpy.median)
    stats.register("Best", numpy.min)
    stats.register("Worst", numpy.max)

    start_time = time.time();

    algorithms.eaSimple(pop, toolbox, cxpb = 0.7, mutpb = 0.01, ngen=500, stats=stats, halloffame=hof, verbose=True)

    elapsed_time = time.time() - start_time
    print('%.2f  seconds' % elapsed_time)
    #print_solution(hof[0])

    return pop, stats, hof

    """

    board_as_array = convert_to_array(board_sol)
    board_as_array[2] = 4
    #board_as_array[4] = 4
    print()
    print_board(convert_to_table(board_as_array))
    print()
    print(count_all_duplicates(board_as_array))
    print()
    print(check_fault_constraints(board_as_array))

    #check_fault_constraints([])
if __name__ == "__main__":
    main()