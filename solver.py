# Sudoku Solver


#test_board
medium_board = [
    [0, 0, 0, 5, 3, 0, 0, 8, 0],
    [0, 0, 2, 6, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 4, 1, 7, 0, 6],
    [2, 0, 0, 0, 0, 7, 3, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 5, 2, 0, 0, 0, 0, 4],
    [5, 0, 9, 3, 2, 0, 0, 0, 1],
    [3, 0, 0, 0, 0, 4, 6, 0, 0],
    [0, 4, 0, 0, 1, 5, 0, 0, 0]
]
medium_board_solution = [
    [4, 6, 7, 5, 3, 2, 1, 8, 9],
    [9, 1, 2, 6, 7, 8, 4, 3, 5],
    [8, 5, 3, 9, 4, 1, 7, 2, 6],
    [2, 9, 4, 1, 5, 7, 3, 6, 8],
    [1, 3, 6, 4, 8, 9, 5, 7, 2],
    [7, 8, 5, 2, 6, 3, 9, 1, 4],
    [5, 7, 9, 3, 2, 6, 8, 4, 1],
    [3, 2, 1, 8, 9, 4, 6, 5, 7],
    [6, 4, 8, 7, 1, 5, 2, 9, 3]
]


# solve() <- board:2d list
#         -> returns board:2d list
# description: recursively solves the board using the backtracking algorithm.
#              returns a list of a list with solution
def solve(board):
    empty_position = find_empty(board)
    if not empty_position:
        return True
    else:
        row, col = empty_position

    for value in range(1, 10):
        if is_valid(board, empty_position, value):
            board[row][col] = value
            if solve(board):
                return board
            board[row][col] = 0

    return False


# find_empty() <- board:2d list
#              -> returns (int, int) or None
# description: iterates through the board to find an empty space.
#              return tuple with the position of the empty space.
#              returns None if no empty spaces are found.
def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None


# is_valid() <- board:list, position:tuple, value:int
#            -> returns True or False
# description: checks the value at the given position to see if the value breaks any game rules
#              returns True if it doesn't
#              returns False if it does
def is_valid(board, position, value):
    # check row. returns False if value is found in the same row, ignoring the current position being checked
    for col in range(9):
        if board[position[0]][col] == value and position[1] != col:
            return False

    # check col. returns False if value is found in the same col, ignoring the current position being checked
    for row in range(9):
        if board[row][position[1]] == value and position[0] != row:
            return False

    # check local box. returns False if value is found in local grid
    # find local box
    box_x = position[1] // 3
    box_y = position[0] // 3

    for row in range(box_y * 3, box_y * 3 + 3):
        for col in range(box_x * 3, box_x * 3 + 3):
            if board[row][col] == value and (row, col) != position:
                return False
    return True


# debugging

# print_board() <- board:list
# description: prints the current board
def print_board(board):
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print('------+-------+------')
        for col in range(9):
            if col % 3 == 0 and col != 0:
                print('| ', end='')
            if col == 8:
                print(str(board[row][col]))
            else:
                print(str(board[row][col]) + ' ', end='')


def main():
    print_board(medium_board)
    solve(medium_board)
    print('===============================')
    print_board(medium_board)
    if medium_board == medium_board_solution:
        print('Solution is correct')
    else:
        print('Solution is incorrect')


if __name__ == '__main__':
    main()
