import sys

def input_format():
    constraints = []
    # Constraints and board are taken
    with open(sys.argv[1], 'r') as file:
        for _ in range(4):
            numbers = [int(number) for number in file.readline().split()]
            constraints.append(numbers)

        board = file.readlines()
        for i in range(len(board)):
            board[i] = board[i].split()
    return constraints, board



def solve(board,constraints):

    coordinates = find(board)

    if coordinates == None:           #If all of the board is tracked, checks all constraints
        return check_cons_last(board, constraints)
    else:
        row, col = coordinates

    original_board = [row[:] for row in board]

    values = ["H", "B", "N"]
    co_values = ["B", "H", "N"]
    for i in range(len(values)):

        #Finds the first element of the grid
        #Tries all valid possibilities for the grid in order

        if board[row][col] == 'L':
            if (valid(board, values[i], (row, col)) and
                    valid(board, co_values[i], (row, col + 1))):

                board[row][col] = values[i]
                board[row][col + 1] = co_values[i]

                #If the pattern suits the constraint too, move to the next step
                if check_cons(board, constraints, row, col) and solve(board,constraints):
                    return True

        if board[row][col] == 'U':
            if (valid(board, values[i], (row, col)) and
                    valid(board, co_values[i], (row + 1, col))):

                board[row][col] = values[i]
                board[row + 1][col] = co_values[i]

                #If the pattern suits the constraint too, move to the next step
                if check_cons(board, constraints, row, col) and solve(board,constraints):
                    return True

        #After the cut off, restore the last tile

        for y in range(len(original_board)):
            for x in range(len(original_board[y])):
                board[y][x] = original_board[y][x]

    return False


def check_cons_last(board, constraints):
    #At the end, it checks if all of the constraints are satisfied

    highs_row, bases_row, highs_col, bases_col = constraints

    for i in range(len(highs_row)):     #Top constraints
        if not (highs_row[i] == board[i].count('H') or highs_row[i] == -1):
            return False

    for i in range(len(bases_row)):     #Bottom constraints
        if not (bases_row[i] == board[i].count('B') or bases_row[i] == -1):
            return False

    for i in range(len(highs_col)):     #Left constraints
        if highs_col[i] == -1:
            continue

        col_H_counter = 0
        for j in range(len(board)):
            if board[j][i] == 'H':
                col_H_counter += 1

        if highs_col[i] != col_H_counter:
            return False


    for i in range(len(bases_col)):     #Right constraints
        if bases_col[i] == -1:
            continue

        col_B_counter = 0
        for j in range(len(board)):
            if board[j][i] == 'B':
                col_B_counter += 1

        if bases_col[i] != col_B_counter:
            return False

    return True


def check_cons(board, constraints, r, c):
    #Checks for the taken element if it breaches the constraints or not

    highs_row, bases_row, highs_col, bases_col = constraints

    if not (highs_row[r] >= board[r].count('H') or highs_row[r] == -1):        #Top constraint
        return False

    if not (bases_row[r] >= board[r].count('B') or bases_row[r] == -1):        #Bottom constraint
        return False

    if highs_col[c] != -1:                                                     #Left constraint
        col_H_counter = 0
        for i in range(len(board)):
            if board[i][c] == 'H':
                col_H_counter += 1

        if not (highs_col[c] >= col_H_counter):
            return False

    if bases_col[c] != -1:                                                     #Right constraint
        col_B_counter = 0
        for i in range(len(board)):
            if board[i][c] == 'B':
                col_B_counter += 1

        if not (bases_col[c] >= col_B_counter):
            return False

    return True


def valid(board, val, pos):
    # Checks all neighbors

    r, c = pos
    if val == 'N':
        return True

    if r > 0 and board[r - 1][c] == val:
        return False

    if c > 0 and board[r][c - 1] == val:
        return False

    if r + 1 < len(board) and board[r + 1][c] == val:
        return False

    if c + 1 < len(board[r]) and board[r][c + 1] == val:
        return False

    return True


def print_format(board, output_file):
    for i in board:
        board_output = ' '.join(i)
        output_file.write(board_output + "\n")


def find(board):
    # Find L or U to apply changes
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'L' or board[i][j] == 'U':
                return (i, j)
    return None


def main():
    constraints, board = input_format()
    output_file = open(sys.argv[2], "w")

    if solve(board,constraints):
        print_format(board, output_file)
    else:
        output_file.write("No solution!")


if __name__ == "__main__":
    main()