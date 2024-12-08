import sys


def file_to_list(board):
    # Get the input. Then convert it to list in a suitable form.

    board = [row.strip() for row in board]
    board = [[int(num) for num in row.split()] for row in board]
    return board


def validity(output_file, board, step_number):
    # Checks the validity of the cells to put a number

    is_board_changed = False

    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                continue

            # If the number of the cell is 0, check the possible numbers to put
            possible_numbers = []
            for i in range(1, 10):
                if possibility(board, i, r, c) == True:
                    possible_numbers.append(i)

            # If you have only one option, plug it instead of zero
            if len(possible_numbers) == 1:
                board[r][c] = possible_numbers[0]

                # Since 1 step is completed, break the nested loops
                is_board_changed = True
                break
        if is_board_changed:
            break

    # Print out the step and start from the beginning
    if is_board_changed:
        step_number += 1
        print_format(output_file, board, step_number, r, c)
        validity(output_file, board, step_number)


def print_format(output_file, board, step_number, r, c):
    # Writes in the desired format

    output_file.write(f"------------------\n")
    line = (f"Step {step_number} - {board[r][c]} @ R{str(r + 1)}C{str(c + 1)}\n")
    output_file.write(str(line))
    output_file.write(f"------------------\n")

    # Seperate the numbers with spaces
    for r in board:
        board_output = ' '.join(map(str, r))
        output_file.write(f"{board_output}\n")


def possibility(board, n, r, c):
    # Checks if it is possible to plug a number

    not_in_row = n not in board[r]
    not_in_column = False

    # Check the numbers with the same index in all rows
    for k in range(9):
        if n == board[k][c]:
            not_in_column = False
            break
        else:
            not_in_column = True

    in_square = False
    square_row = r // 3 * 3
    square_column = c // 3 * 3

    # Check all the numbers in the same 3x3 cell
    for i in range(3):
        for j in range(3):
            if board[square_row + i][square_column + j] == n:
                in_square = True

    if not_in_row and not_in_column and not in_square:
        return True
    return False


def main():
    input_file = open(sys.argv[1], "r")
    output_file = open(sys.argv[2], "w")
    board = file_to_list(input_file.readlines())
    step_number = 0

    validity(output_file, board, step_number)

    output_file.write(f"------------------")

    input_file.close()
    output_file.flush()
    output_file.close()


if __name__ == "__main__":
    main()