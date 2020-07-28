import random
import math


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
    # Generate all possible solutions to grid and count number of solutions
    global num_solution, difficulty_score
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n, grid):
                        grid[y][x] = n
                        multiple_solve(grid)
                        difficulty_score += 1
                        grid[y][x] = 0
                return
    num_solution += 1


def single_solve():
    # Solve the board and produce a single fully legal board
    global seed
    if number_filled(seed) == 81:
        return True
    for y in range(9):
        for x in range(9):
            if seed[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n, seed):
                        seed[y][x] = n
                        if single_solve():
                            return True
                        seed[y][x] = 0
                return False


def number_filled(grid):
    # Return number of filled spaces in grid
    number = 0
    for y in range(9):
        for x in range(9):
            if grid[y][x] != 0:
                number += 1
    return number


difficulty = input("Please type in Difficulty level: Easy, Medium, Hard. ")
minimum_score = 4000
maximum_score = math.inf
while difficulty.lower() not in ["easy", "medium", "hard"]:
    difficulty = input("Please type in Difficulty level: Easy, Medium, Hard. ")
if difficulty.lower() == "easy":
    maximum_score = 5000
    clue = 50
if difficulty.lower() == "medium":
    minimum_score = 5000
    maximum_score = 6000
    clue = 40
if difficulty.lower() == "hard":
    minimum_score = 6000
    clue = 30
temp = 0  # A temporary value to hold while determining whether the location of removal is valid
tested_spot = []  # Keep track of locations that has been tested before
num_solution = 0  # Initialize number of solutions. At this point, the solved board has 0 solutions
difficulty_score = 0  # Initialize difficulty of the board. At this point, the solved board has difficulty level 0
while not (minimum_score < difficulty_score < maximum_score):
    # Number of attempts the while loop can try to generate a board, this is to prevent the loop from getting stuck
    attempt = 0
    # Initialize a randomized seed
    seed = [[random.randrange(10), 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, random.randrange(10), 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, random.randrange(10)],
            [0, 0, 0, random.randrange(10), 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, random.randrange(10), 0],
            [0, 0, random.randrange(10), 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, random.randrange(10), 0, 0],
            [0, random.randrange(10), 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, random.randrange(10), 0, 0, 0]]
    single_solve()  # Produce a single fully solved board
    while number_filled(seed) > clue:
        if attempt > 1000:  # To prevent the possibility of never reaching the defined clue number filled
            break
        # Remove a filled space randomly
        y_remove = random.randrange(9)
        x_remove = random.randrange(9)
        while seed[y_remove][x_remove] == 0 or (y_remove, x_remove) in tested_spot:
            if attempt > 1000:  # To prevent the case of having all possible spot tested
                break
            y_remove = random.randrange(9)
            x_remove = random.randrange(9)
            attempt += 1
        # Store the value temporarily
        temp = seed[y_remove][x_remove]
        # Empty the selected space, producing a "test board"
        seed[y_remove][x_remove] = 0
        # Solved the test board for number of total solutions
        multiple_solve(seed)
        # If board has more than 1 solutions, the number is returned, the location of removal is stored
        if num_solution > 1:
            seed[y_remove][x_remove] = temp
            tested_spot.append((y_remove, x_remove))
        # Reset the solution counter for next test board
        num_solution = 0
        attempt += 1

print("Difficulty level: {}".format(difficulty.lower().capitalize()))
print("The generated Sudoku is:")
print_board(seed)
single_solve()
print("The solution to the Sudoku is:")
print_board(seed)
