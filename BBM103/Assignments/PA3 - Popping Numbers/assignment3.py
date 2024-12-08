import sys

def board_to_list(board):
    # Converts input_file to a list into a lists of integers
    board = [row.strip() for row in board]
    board = [[int(num) for num in row.split()] for row in board]
    return board

def print_format(board,score):
    #Prints out the current board
    board_output = "\n".join(" ".join(map(str, row)) for row in board)
    print("\n" + board_output + "\n")
    print("Your score is:", score , "\n")

def game_over(board):
    # Checks if there are any cells with neighbors having the same number
    for i in range(len(board)):
        for j in range(len(board[0])):
            if has_neighbor(board, i, j):
                return False
    return True

def has_neighbor(board,r,c):
    # Checks above, below, left and right neighbors if they have the same number
    number = board[r][c]
    neighbors = [(r+1,c), (r-1,c), (r,c-1), (r,c+1)]
    for r, c in neighbors:
        if -1 < r < len(board) and -1 < c < len(board[0]):
            if number != " " and board[r][c] == number:
                return True
    return False

def change_output(board,r,c):                                                                                           ###HARDEST PART
    # Main purpose is updating the score, Secondly it updates the board by calling functions
    number = board[r][c]
    remove_these = [(r, c)]                                                                                             ##Assignmentta en sevdiğim mantık
    will_be_deleted(board, r, c, number, remove_these)
    # Update the board by removing destroyed cells
    for i, j in remove_these:
        board[i][j] = " "
    # Shift numbers down and remove empty columns
    scroll_down(board)
    board = delete_empty_line(board)
    return board, len(remove_these) * number
def will_be_deleted(board,r,c,number,remove_these):
    # In addition to "has_neighbor" function, it checks the neighbors of the required neighbors and appends to a list
    neighbors = [(r-1,c), (r+1,c), (r,c+1), (r,c-1)]
    for i, j in neighbors:
        if 0 <= i < len(board) and 0 <= j < len(board[0]):
            if board[i][j] == number and (i, j) not in remove_these:
                remove_these.append((i, j))
                will_be_deleted(board, i, j, number, remove_these)
def scroll_down(board):
    # To scroll the numbers down, it moves blank cells up                                                               #Baya baya baya iyi mantık

    num_of_rows = len(board)
    for c in range(len(board[0])):
        filled_cells = []
        for r in board:
            if r[c] != " ":
                filled_cells.append(r[c])
        num_of_emp_cells = num_of_rows - len(filled_cells)

        #At the same column, firstly, add blank cells as many as the num_of_emp_cell, then add the rest
        for i in range(num_of_rows):
            if i < num_of_emp_cells:
                board[i][c] = " "
            else:
                board[i][c] = filled_cells[i - num_of_emp_cells]
        #Since lists are mutable, the function doesn't need to return anything
def delete_empty_line(board):
    #If there are no numbers left, the game is over                                                                     #En zor kısmı olabilirdi ama aynı mantık tekrarladı
    all_empty = True
    for r in board:
        row_empty = True
        for c in r:
            if c != " ":
                row_empty = False
                break

        if row_empty == False:
            all_empty = False
            break

    if all_empty:
        print("Game over")
        return board

    #Deletes empty rows
    remove_rows = []
    for r in range(len(board)):
        row_empty = True
        for number in board[r]:
            if number!= " ":
                row_empty = False
                break
        if row_empty:
            remove_rows.append(board[r])

    refresh_board = []
    for r in board:
        if r not in remove_rows:
            refresh_board.append(r)
    board = refresh_board

    #Delete empty columns
    remove_cols = []
    for c in range(len(board[0])):
        col_empty = True
        for r in board:
            if r[c] != " ":
                col_empty = False
                break
        if col_empty:
            remove_cols.append(c)

    refresh_board = []
    for r in board:
        new_rows = []
        for i in range(len(board[0])):
            if i not in remove_cols:
                new_rows.append(r[i])
        refresh_board.append(new_rows)
    board = refresh_board

    return board
def main():
    input_file = open(sys.argv[1], "r")
    board = board_to_list(input_file)
    score = 0
    print_format(board, score)
    while game_over(board) == False:

        place = input("Please enter a row and a column number: ").split()
        r, c = int(place[0]) - 1, int(place[1]) - 1

        #Print out different outputs for exceptional cases
        if not (-1<r<len(board) and -1<c<len(board[0])):
            print("\nPlease enter a correct size!\n")
            continue

        if has_neighbor(board, r, c) == False:
            print("\nNo movement happened try again.")
            print_format(board, score)
            continue

        # While everything is appropriate, update the board and score
        board, turn_score = change_output(board, r, c)
        score += turn_score
        print_format(board, score)
    print("Game over")


if __name__ == "__main__":
    main()