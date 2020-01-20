from calcudoku.game import Calcudoku
import math

"""
This function will generate a board in the given size
The function will return the solved board and its constraints
"""
def generate_board_in_size(board_size):
    game = Calcudoku.generate(board_size)
    for partition in game.partitions:
        partition.sort()
    board = convert_to_table(game.board)
    constraints = get_constraints(game.operations, game.partitions)
    return board, constraints

"""
This function will convert a given array to a table (2D array)
"""
def convert_to_table(array):
    table = []
    n = int((len(array)) ** 0.5)
    for i in range(0, n):
        line = []
        for j in range(0, n):
            line.append(array[i * n + j])
        table.append(line)
    return table

"""
This function will convert the array to a 2D table
"""
def convert_to_array(table):
    n = int((len(table)) ** 2)
    table_length = len(table)
    array = []
    for i in range(0, n):
        array.append(table[int(i / table_length)][i % table_length])
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
    for i in range(0, len(operations)):
        constraints.append((operations[i][0], operations[i][1], partitions[i]))
    return constraints

"""
This function represents the sum operator
"""
def operator_sum(board, indexes_list, answer):
    total_sum = 0
    for index in indexes_list:
        if answer - board[index] < len(indexes_list) - 1:
            return -1
        total_sum += board[index]
    return total_sum

"""
This function represents the multiplication operator
"""
def operator_multiply(board, indexes_list, answer):
    multiplication = 1
    for index in indexes_list:
        if answer % board[index] != 0:
            return -1
        multiplication *= board[index]
    return multiplication

"""
This function returns the minimum and maximum numbers in a given list
"""
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

"""
This function represents the subtraction operator
"""
def operator_sub(board, indexes_list, answer):
    min_num, max_num = get_min_max_by_indexes(board, indexes_list)
    if max_num <= answer or min_num + answer > pow(len(board), 0.5):
        return -1
    return max_num - min_num

"""
This function represents the division operator
"""
def operator_divide(board, indexes_list, answer):
    min_num, max_num = get_min_max_by_indexes(board, indexes_list)
    if max_num % answer != 0 or answer * min_num > pow(len(board), 0.5):
        return -1
    return max_num / min_num

"""
This function represents a "none" operator. This happens when there is only one cell in the constraint
"""
def operator_none(board, indexes_list, answer):
    if board[indexes_list[0]] != answer:
        return -1
    return answer

"""
This function will count the number of duplicates in a given list of numbers
"""
def count_duplicates(numbers_list):
    duplicates_count = 0
    num_set = []
    for num in numbers_list:
        if num in num_set:
            duplicates_count += 1
        else:
            num_set.append(num)
    return duplicates_count

"""
This function will receive a board and will return the number of duplicates
In each row and in each column in the board
"""
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

"""
This function returns th possible values for a given partition
"""
def partition_possible_values(partition_length, answer, operator, board_size, possible_locations):
    operators_to_sign_dict = {'subtract': '-', 'multiply': '*', 'add': '+',
                              'divide': '/', 'none': '0'}
    op = operators_to_sign_dict[operator]
    if op == '+':
        arr = partition_possible_values_sum(partition_length, answer, board_size, possible_locations)
    elif op == '-':
        arr = partition_values_sub(answer, board_size)
    elif op == '/':
        arr = partition_values_div(answer, board_size)
    elif op == '*':  # *
        arr = partition_possible_values_multi(partition_length, answer, board_size, possible_locations)
    else:  # None operator
        arr = ["%s" % answer]

    true_arr = {}
    for i in range(len(arr)):
        instance = arr[i]
        true_sol = []
        for solution in instance:
            split = solution.split(",")
            val_arr = []
            for val in split:
                val_arr.append(int(val))
            true_sol.append(val_arr)
        true_arr[i] = true_sol
    return true_arr

"""
This function returns th possible values for a given partition with the 'sub' operator
"""
def partition_values_sub(answer, board_size):
    array = []
    for i in range(1, board_size - answer + 1):
        array.append("%s,%s" % (i, answer + i))
        array.append("%s,%s" % (answer + i, i))
    return [array]

"""
This function returns th possible values for a given partition with the 'div' operator
"""
def partition_values_div(answer, board_size):
    array = []
    for i in range(1, int(board_size / answer) + 1):
        array.append("%s,%s" % (i, answer * i))
        array.append("%s,%s" % (answer * i, i))
    return [array]

"""
This function returns th possible values for a given partition with the 'sum' operator
"""
def partition_possible_values_sum(partition_length, answer, board_size, possible_locations):
    dictionary_assignment = []
    for i in range(len(possible_locations)):
        possible = possible_locations[i]
        dictionary_assignment.append(
            partition_possible_values_sum_rec(partition_length, answer, [], board_size, '', possible, 0))
    return dictionary_assignment

"""
This function returns th possible values for a given partition with the 'sum' operator recursively 
"""
def partition_possible_values_sum_rec(partition_length, answer, array, board_size, so_far_string, possible,
                                      index_possible):
    if partition_length == 0 and answer == 0 and index_possible == len(possible):  # success
        toAppend = '%s' % so_far_string[:-1]
        split = toAppend.split(",")
        if len(set(split)) == len(split):
            array.append(toAppend)
        return array
    if partition_length == 0 or answer <= 0 or index_possible == len(possible):  # fail
        return array
    num_of_times = len(possible[index_possible])
    min_val = min(board_size, int(answer / num_of_times))
    for i in range(1, min_val + 1):
        partition_possible_values_sum_rec(partition_length - num_of_times, answer - num_of_times * i, array, board_size,
                                          '%s%s,' % (so_far_string, i), possible, index_possible + 1)
    return array

"""
This function returns th possible values for a given partition with the 'multi' operator
"""
def partition_possible_values_multi(partition_length, answer, board_size, possible_locations):
    dictionary_assignment = []
    for i in range(len(possible_locations)):
        possible = possible_locations[i]
        dictionary_assignment.append(
            partition_possible_values_multi_rec(partition_length, answer, [], board_size, '', possible, 0, False))
    return dictionary_assignment

"""
This function returns th possible values for a given partition with the 'multi' operator recursively 
"""
def partition_possible_values_multi_rec(partition_length, answer, array, board_size, so_far_string, possible,
                                        index_possible, used_one):
    if partition_length == 0 and answer == 1 and index_possible == len(possible):  # success
        toAppend = '%s' % so_far_string[:-1]
        split = toAppend.split(",")
        if len(set(split)) == len(split):
            array.append(toAppend)
        return array
    if partition_length == 0 or index_possible == len(possible):  # fail
        return array
    if answer == 1 and used_one:
        return array
    num_of_times = len(possible[index_possible])
    min_val = min(board_size, int(answer ** (1 / num_of_times)))
    for i in range(1, min_val + 1):
        multi = i ** num_of_times
        if answer % multi == 0:
            partition_possible_values_multi_rec(partition_length - num_of_times, answer / (i ** num_of_times), array,
                                                board_size, '%s%s,' % (so_far_string, i), possible, index_possible + 1,
                                                used_one or i == 1)
    return array

"""
The operator dictionary
"""
operators_dict = {'subtract': operator_sub, 'multiply': operator_multiply, 'add': operator_sum,
                  'divide': operator_divide, 'none': operator_none}

"""
This function will return the number of fault constraints (constraints that are fulfilled)
"""
def check_fault_constraints(board, constraints):
    faults = 0
    for constraint in constraints:
        calculation = operators_dict[constraint[0]](board, constraint[2], constraint[1])
        if calculation == -1:
            faults += len(constraints)
        else:
            faults += min(1, abs(constraint[1] - calculation))
    return faults
