def print_board(grid):
    # Print in correct format
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in grid]))


def possible(y, x, n, grid):
    # Check if n is a legal input in grid[y][x]
    for i in range(0, 9):
        if grid[y][i] == n:
            return False
        if grid[i][x] == n:
            return False
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[(y // 3) * 3 + i][(x // 3) * 3 + j] == n:
                return False
    return True


def multiple_solve(grid):
    print("computing")
    # Generate all possible solutions to grid and count number of solutions
    global num_solution, difficulty
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n, grid):
                        grid[y][x] = n
                        multiple_solve(grid)
                        difficulty += 1
                        grid[y][x] = 0
                return
    print_board(grid)
    print("\n")
    num_solution += 1


num_solution = 0
difficulty = 0

board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
         [6, 0, 0, 1, 9, 5, 0, 0, 0],
         [0, 9, 8, 0, 0, 0, 0, 6, 0],
         [8, 0, 0, 0, 6, 0, 0, 0, 3],
         [4, 0, 0, 8, 0, 3, 0, 0, 1],
         [7, 0, 0, 0, 2, 0, 0, 0, 6],
         [0, 6, 0, 0, 0, 0, 2, 8, 0],
         [0, 0, 0, 4, 1, 9, 0, 0, 5],
         [0, 0, 0, 0, 8, 0, 0, 7, 9]]


multiple_solve(board)
print("Number of solutions to this board: {}".format(num_solution))
print("Difficulty level: {}".format(difficulty))
