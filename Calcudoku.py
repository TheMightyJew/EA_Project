from calcudoku.game import Calcudoku


# This function will generate a board in the given size
# The function will return the solved board and its constraints
def generate_board_in_size(board_size):
    game = Calcudoku.generate(board_size)
    for partition in game.partitions:
        partition.sort()
    board = convert_to_table(game.board)
    constraints = get_constraints(game.operations, game.partitions)
    #constraints = [('multiply', 32, [0, 1, 5, 9]), ('add', 5, [2, 6]), ('add', 9, [4, 8, 12, 13]), ('subtract', 1, [10, 14]), ('multiply', 24, [3, 7, 11, 15])]
    return board, constraints


# This function will convert a given array to a table (2D array)
def convert_to_table(array):
    table = []
    n = int((len(array)) ** 0.5)
    for i in range(0, n):
        line = []
        for j in range(0, n):
            line.append(array[i * n + j])
        table.append(line)
    return table


# This function will convert the array to a 2D table
def convert_to_array(table):
    n = int((len(table)) ** 2)
    table_length = len(table)
    array = []
    for i in range(0, n):
        array.append(table[int(i / table_length)][i % table_length])
    return array


# This function will print the board
def print_board(board):
    for line in board:
        print(line)


# This function extracts the constraints from the operations and partitions
def get_constraints(operations, partitions):
    constraints = []
    for i in range(0, len(operations)):
        constraints.append((operations[i][0], operations[i][1], partitions[i]))
    return constraints


# This function represents the sum operator
def operator_sum(board, indexes_list):
    total_sum = 0
    for index in indexes_list:
        total_sum += board[index]
    return total_sum


# This function represents the multiplication operator
def operator_multiply(board, indexes_list):
    multiplication = 1
    for index in indexes_list:
        multiplication *= board[index]
    return multiplication


# This function returns the minimum and maximum numbers in a given list
def get_min_max_by_indexes(board, indexes_list):
    max_num = None
    min_num = None
    for index in indexes_list:
        value = board[index]
        if max_num is None or min_num is None:
            min_num = value
            max_num = value
        else:
            min_num = min(min_num, value)
            max_num = max(max_num, value)
    return min_num, max_num


# This function represents the subtraction operator
def operator_sub(board, indexes_list):
    min_num, max_num = get_min_max_by_indexes(board, indexes_list)
    return max_num - min_num


# This function represents the division operator
def operator_divide(board, indexes_list):
    min_num, max_num = get_min_max_by_indexes(board, indexes_list)
    return max_num / min_num


# This function represents a "none" operator. This happens when there is only one cell in the constraint
def operator_none(board, indexes_list):
    return board[indexes_list[0]]


# This function will count the number of duplicates in a given list of numbers
def count_duplicates(numbers_list):
    duplicates_count = 0
    num_set = []
    for num in numbers_list:
        if num in num_set:
            duplicates_count += 1
        else:
            num_set.append(num)
    return duplicates_count


# This function will receive a board and will return the number of duplicates
# In each row and in each column in the board
def count_all_duplicates(board):
    size = int(len(board) ** 0.5)
    duplicates_count = 0
    bad_rows = 0
    bad_columns = 0
    for index in range(size):
        board_row = board[size * index:size * (index + 1)]
        duplicates = count_duplicates(board_row)
        duplicates_count += duplicates
        bad_rows += min(1, duplicates)
        board_column = []
        for secondIndex in range(size):
            board_column.append(board[index + size * secondIndex])
        duplicates = count_duplicates(board_column)
        duplicates_count += duplicates
        bad_columns += min(1, duplicates)
    return duplicates_count, bad_rows + bad_columns


operators_dict = {'subtract': operator_sub, 'multiply': operator_multiply, 'add': operator_sum,
                  'divide': operator_divide, 'none': operator_none}


# This function will return the number of fault constraints (constraints that are fulfilled)
def check_fault_constraints(board, constraints):
    """
    board = [4, 1, 2, 3, 3, 2, 1, 4, 2, 4, 3, 1, 1, 3, 4, 2]
    print_board(convert_to_table(board))
    """
    faults_num = 0
    for constraint in constraints:
        if constraint[1] != operators_dict[constraint[0]](board, constraint[2]):
            #faults_num += len(constraint[2])
            faults_num += 1
    return faults_num
