import pygame
import random
import sys

# 0:T, 1:S, 2:Z, 3:J, 4:L, 5:I, 6:O

tetriminos_shape = [
    [[1, 1, 1],
     [0, 1, 0]],
    [[0, 2, 2],
     [2, 2, 0]],
    [[3, 3, 0],
     [0, 3, 3]],
    [[4, 0, 0],
     [4, 4, 4]],
    [[0, 0, 5],
     [5, 5, 5]],
    [[6, 6, 6, 6]],
    [[7, 7],
     [7, 7]]
]

tetriminos_colors = [
    pygame.Color(117, 80, 123),
    pygame.Color(78, 154, 6),
    pygame.Color(204, 0, 0),
    pygame.Color(52, 101, 164),
    pygame.Color(211, 215, 207),
    pygame.Color(6, 152, 154),
    pygame.Color(196, 160, 0)
]

FPS = 30


class Tetris:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        # Initial config of game window
        self.g_width = 450
        self.g_height = self.g_width * 2
        self.block_size = int(self.g_width / 10)
        self.w_width = self.g_width + 5 * self.block_size
        self.w_height = self.g_height
        self.fgColor = pygame.Color(255, 253, 252)
        self.bgColor = pygame.Color(37, 37, 37)
        self.tiny_font = pygame.font.Font('ArcadeClassic.TTF', 20)
        self.small_font = pygame.font.Font('ArcadeClassic.TTF', 40)
        self.big_font = pygame.font.Font('ArcadeClassic.TTF', 80)
        self.tetris_ai = Ai()

        self.window = pygame.display.set_mode((self.w_width, self.w_height + 1))
        pygame.display.set_caption('Tetris')
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.key.set_repeat(250, 25)

        # Initial game state
        self.bag = [0, 1, 2, 3, 4, 5, 6]
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.n_piece = tetriminos_shape[random.choice(self.bag)]
        self.bag.remove(tetriminos_shape.index(self.n_piece))
        self.c_piece = None
        self.c_piece_x = None
        self.c_piece_y = None
        self.new_piece()
        self.pause = False
        self.in_game = True
        self.ai = False
        self.level = 0
        self.score = 0
        self.line = 0
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    def new_piece(self):
        self.c_piece = self.n_piece
        if len(self.bag) == 0:
            self.bag = [0, 1, 2, 3, 4, 5, 6]
        self.n_piece = tetriminos_shape[random.choice(self.bag)]
        self.bag.remove(tetriminos_shape.index(self.n_piece))
        self.c_piece_x = int(5 - len(self.c_piece[0]) / 2)
        self.c_piece_y = 0

        if self.collision(self.c_piece, (self.c_piece_x, self.c_piece_y)):
            self.in_game = False

    def draw_background(self):
        # Draw all none moving pieces
        self.window.fill(self.bgColor)
        # Draw play field
        pygame.draw.lines(self.window, self.fgColor, True, [(0, 0), (self.g_width, 0),
                                                            (self.g_width, self.g_height), (0, self.g_height)])
        for x in range(1, 10):
            for y in range(1, 20):
                pygame.draw.circle(self.window, self.fgColor, (x * self.block_size, y * self.block_size), 2)
        # Draw side label: Next piece, level, score, line, and control descriptions
        next_text = self.small_font.render("Next", 1, self.fgColor)
        self.window.blit(next_text,
                         (int(self.g_width + (self.w_width - self.g_width) / 2 - next_text.get_width() / 2), 0))
        pygame.draw.lines(self.window, self.fgColor, True,
                          [(int(self.g_width + (self.w_width - self.g_width) / 2 - 2 * self.block_size),
                            next_text.get_height()),
                           (int(self.g_width + (self.w_width - self.g_width) / 2 + 2 * self.block_size),
                            next_text.get_height()),
                           (int(self.g_width + (self.w_width - self.g_width) / 2 + 2 * self.block_size),
                            next_text.get_height() + 2 * self.block_size - 1),
                           (int(self.g_width + (self.w_width - self.g_width) / 2 - 2 * self.block_size),
                            next_text.get_height() + 2 * self.block_size - 1)])
        for x in range(1, 4):
            pygame.draw.circle(self.window, self.fgColor, (
                int(self.g_width + (self.w_width - self.g_width) / 2 - 2 * self.block_size) + x * self.block_size,
                next_text.get_height() + self.block_size), 2)
        level = self.small_font.render("Level", 1, self.fgColor)
        self.window.blit(level, (int(self.g_width + (self.w_width - self.g_width) / 2 - level.get_width() / 2),
                                 next_text.get_height() + 2 * self.block_size))
        score = self.small_font.render("Score", 1, self.fgColor)
        self.window.blit(score, (int(self.g_width + (self.w_width - self.g_width) / 2 - score.get_width() / 2),
                                 4 * next_text.get_height() + 2 * self.block_size))
        line = self.small_font.render("Line", 1, self.fgColor)
        self.window.blit(line, (int(self.g_width + (self.w_width - self.g_width) / 2 - line.get_width() / 2),
                                6 * next_text.get_height() + 2 * self.block_size))
        # best = self.small_font.render("Best Score", 1, self.fgColor)
        # self.window.blit(best, (int(self.g_width + (self.w_width - self.g_width) / 2 - best.get_width() / 2),
        #                         10 * next_text.get_height() + 2 * self.block_size))
        up = self.tiny_font.render("Up", 1, self.fgColor)
        self.window.blit(up, (int(self.g_width + (self.w_width - self.g_width) / 4 - up.get_width() / 2),
                              13 * next_text.get_height() + 2 * self.block_size))
        rotate = self.tiny_font.render("Rotate", 1, self.fgColor)
        self.window.blit(rotate,
                         (int(self.g_width + (self.w_width - self.g_width) * 3 / 4 - rotate.get_width() / 2),
                          13 * next_text.get_height() + 2 * self.block_size))
        down = self.tiny_font.render("Down", 1, self.fgColor)
        self.window.blit(down, (int(self.g_width + (self.w_width - self.g_width) / 4 - down.get_width() / 2),
                                14 * next_text.get_height() + 2 * self.block_size))
        soft_drop = self.tiny_font.render("Soft     Drop", 1, self.fgColor)
        self.window.blit(soft_drop, (
            int(self.g_width + (self.w_width - self.g_width) * 3 / 4 - soft_drop.get_width() / 2),
            14 * next_text.get_height(
            ) + 2 * self.block_size))
        space = self.tiny_font.render("Space", 1, self.fgColor)
        self.window.blit(space, (int(self.g_width + (self.w_width - self.g_width) / 4 - space.get_width() / 2),
                                 15 * next_text.get_height() + 2 * self.block_size))
        hard_drop = self.tiny_font.render("Hard     Drop", 1, self.fgColor)
        self.window.blit(hard_drop, (
            int(self.g_width + (self.w_width - self.g_width) * 3 / 4 - hard_drop.get_width() / 2),
            15 * next_text.get_height(
            ) + 2 * self.block_size))
        p = self.tiny_font.render("P", 1, self.fgColor)
        self.window.blit(p, (int(self.g_width + (self.w_width - self.g_width) / 4 - p.get_width() / 2),
                             16 * next_text.get_height() + 2 * self.block_size))
        pause = self.tiny_font.render("Pause", 1, self.fgColor)
        self.window.blit(pause, (int(self.g_width + (self.w_width - self.g_width) * 3 / 4 - pause.get_width() / 2),
                                 16 * next_text.get_height() + 2 * self.block_size))
        escape = self.tiny_font.render("Escape", 1, self.fgColor)
        self.window.blit(escape, (int(self.g_width + (self.w_width - self.g_width) / 4 - escape.get_width() / 2),
                                  17 * next_text.get_height() + 2 * self.block_size))
        exit_game = self.tiny_font.render("Exit     Game", 1, self.fgColor)
        self.window.blit(exit_game, (
            int(self.g_width + (self.w_width - self.g_width) * 3 / 4 - exit_game.get_width() / 2),
            17 * next_text.get_height(
            ) + 2 * self.block_size))
        a = self.tiny_font.render("A", 1, self.fgColor)
        self.window.blit(a, (int(self.g_width + (self.w_width - self.g_width) / 4 - a.get_width() / 2),
                             18 * next_text.get_height() + 2 * self.block_size))
        toggle_ai = self.tiny_font.render("Toggle       AI", 1, self.fgColor)
        self.window.blit(toggle_ai, (
            int(self.g_width + (self.w_width - self.g_width) * 3 / 4 - toggle_ai.get_width() / 2),
            18 * next_text.get_height(
            ) + 2 * self.block_size))
        if self.ai:
            ai = self.small_font.render("AI     On", 1, self.fgColor)
        else:
            ai = self.small_font.render("AI     Off", 1, self.fgColor)
        self.window.blit(ai, (int(self.g_width + (self.w_width - self.g_width) / 2 - ai.get_width() / 2),
                              int(self.w_height - ai.get_height())))

    def draw_number(self):
        le_number = self.big_font.render(str(self.level), 1, self.fgColor)
        pygame.draw.rect(self.window, self.bgColor,
                         pygame.Rect((int(self.g_width + (self.w_width - self.g_width) / 2 - le_number.get_width() / 2),
                                      le_number.get_height() + 2 * self.block_size),
                                     (le_number.get_width(), le_number.get_height())))
        self.window.blit(le_number, (int(self.g_width + (self.w_width - self.g_width) / 2 - le_number.get_width() / 2),
                                     le_number.get_height() + 2 * self.block_size))
        s_number = self.small_font.render(str(self.score), 1, self.fgColor)
        pygame.draw.rect(self.window, self.bgColor,
                         pygame.Rect((int(self.g_width + (self.w_width - self.g_width) / 2 - s_number.get_width() / 2),
                                      5 * s_number.get_height() + 2 * self.block_size),
                                     (s_number.get_width(), s_number.get_height())))
        self.window.blit(s_number, (int(self.g_width + (self.w_width - self.g_width) / 2 - s_number.get_width() / 2),
                                    5 * s_number.get_height() + 2 * self.block_size))
        li_number = self.small_font.render(str(self.line), 1, self.fgColor)
        pygame.draw.rect(self.window, self.bgColor,
                         pygame.Rect((int(self.g_width + (self.w_width - self.g_width) / 2 - li_number.get_width() / 2),
                                      7 * li_number.get_height() + 2 * self.block_size),
                                     (li_number.get_width(), li_number.get_height())))
        self.window.blit(li_number, (int(self.g_width + (self.w_width - self.g_width) / 2 - li_number.get_width() / 2),
                                     7 * li_number.get_height() + 2 * self.block_size))

    def draw_foreground(self):
        for y, row in enumerate(self.c_piece):  # Draw Current Piece
            for x, val in enumerate(row):
                if val > 0:
                    pygame.draw.rect(self.window, tetriminos_colors[self.c_piece[y][x] - 1], pygame.Rect(
                        (self.c_piece_x + x) * self.block_size + 1, (self.c_piece_y + y) * self.block_size + 1,
                        self.block_size - 2, self.block_size - 2))
        for y, row in enumerate(self.board):  # Draw Board
            for x, val in enumerate(row):
                if val > 0:
                    pygame.draw.rect(self.window, tetriminos_colors[self.board[y][x] - 1], pygame.Rect(
                        x * self.block_size + 1, y * self.block_size + 1, self.block_size - 2, self.block_size - 2))
        example_text = self.small_font.render("", 1, self.fgColor)
        for y, row in enumerate(self.n_piece):  # Draw Next Piece
            for x, val in enumerate(row):
                if val > 0:
                    pygame.draw.rect(self.window, tetriminos_colors[self.n_piece[y][x] - 1], pygame.Rect(
                        ((int(self.g_width + (
                                self.w_width - self.g_width) / 2 - 2 * self.block_size + x * self.block_size + 1),
                          int(example_text.get_height() + y * self.block_size + 1),
                          self.block_size - 2, self.block_size - 2))))

    def collision(self, piece, offset):
        off_x, off_y = offset
        for cy, row in enumerate(piece):
            for cx, cell in enumerate(row):
                try:
                    if cell and self.board[cy + off_y][cx + off_x]:
                        return True
                except IndexError:
                    return True
        return False

    def move(self, delta_x):
        if self.in_game and not self.pause:
            next_x = self.c_piece_x + delta_x
            if next_x < 0:
                next_x = 0
            if next_x > 10 - len(self.c_piece[0]):
                next_x = 10 - len(self.c_piece[0])
            if not self.collision(self.c_piece, (next_x, self.c_piece_y)):
                self.c_piece_x = next_x

    def drop(self, soft_drop=False):
        if self.in_game and not self.pause:
            self.score += 1 if soft_drop else 0
            self.c_piece_y += 1
        if self.collision(self.c_piece, (self.c_piece_x, self.c_piece_y)):
            # Add currently piece to board
            for cy, row in enumerate(self.c_piece):
                for cx, val in enumerate(row):
                    self.board[cy + self.c_piece_y - 1][cx + self.c_piece_x] += val
            self.new_piece()
            cleared_rows = 0
            while True:
                for i, row in enumerate(self.board):
                    if 0 not in row:
                        del self.board[i]
                        self.board = [[0 for _ in range(10)]] + self.board
                        cleared_rows += 1
                        break
                else:
                    break
            line_scores = [0, 40, 100, 300, 1200]
            self.line += cleared_rows
            self.score += line_scores[cleared_rows] * self.level
            if self.line >= self.level * 6:
                self.level += 1
                delay = 1000 - 50 * (self.level - 1)
                delay = 100 if delay < 100 else delay
                pygame.time.set_timer(pygame.USEREVENT + 1, delay)
            return True
        return False

    def hard_drop(self):
        if self.in_game and not self.pause:
            while not self.drop(soft_drop=True):
                pass

    def rotate_piece(self):
        if self.in_game and not self.pause:
            temp_piece = [[self.c_piece[y][x] for y in range(len(self.c_piece))] for x in
                          range(len(self.c_piece[0]) - 1, -1, -1)]
            if not self.collision(temp_piece, (self.c_piece_x, self.c_piece_y)):
                self.c_piece = temp_piece

    def toggle_pause(self):
        self.pause = not self.pause

    def toggle_ai(self):
        self.ai = not self.ai

    def new_game(self):
        if not self.in_game:
            # Initial game state
            self.bag = [0, 1, 2, 3, 4, 5, 6]
            self.board = [[0 for _ in range(10)] for _ in range(20)]
            self.n_piece = tetriminos_shape[random.choice(self.bag)]
            self.bag.remove(tetriminos_shape.index(self.n_piece))
            self.new_piece()
            self.pause = False
            self.in_game = True
            self.ai = False
            self.level = 0
            self.score = 0
            self.line = 0
            pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    def run(self):
        global best_score
        key_actions = {
            'ESCAPE': sys.exit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': lambda: self.drop(soft_drop=True),
            'UP': self.rotate_piece,
            'SPACE': self.hard_drop,
            'p': self.toggle_pause,
            'RETURN': self.new_game,
            'a': self.toggle_ai
        }
        clock = pygame.time.Clock()
        while True:
            if not self.in_game:
                game_over = self.small_font.render("Game Over", 1, self.fgColor)
                self.window.blit(game_over, (
                    int(self.g_width / 2 - game_over.get_width() / 2),
                    int(self.g_height / 2 - game_over.get_height() / 2)))
                return_message = self.small_font.render("Press RETURN", 1, self.fgColor)
                self.window.blit(return_message, (int(self.g_width / 2 - return_message.get_width() / 2),
                                                  int(game_over.get_height() / 2 + self.g_height / 2 -
                                                      return_message.get_height() / 2)))
            else:
                if self.pause:
                    paused = self.small_font.render("Paused", 1, self.fgColor)
                    self.window.blit(paused, (
                        int(self.g_width / 2 - paused.get_width() / 2),
                        int(self.g_height / 2 - paused.get_height() / 2)))
                else:
                    self.draw_background()
                    self.draw_number()
                    self.draw_foreground()
            pygame.display.update()
            for event in list(pygame.event.get()):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.USEREVENT + 1:
                    self.drop(soft_drop=False)
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval('pygame.K_' + key):
                            key_actions[key]()
            if self.ai:
                target_r, target_x = self.tetris_ai.next_move(self.board, self.c_piece, self.n_piece)
                if self.c_piece == target_r and self.c_piece_x == target_x:
                    key_actions['SPACE']()
                elif self.c_piece != target_r:
                    key_actions['UP']()
                elif self.c_piece == target_r:
                    if self.c_piece_x < target_x:
                        key_actions['RIGHT']()
                    elif self.c_piece_x > target_x:
                        key_actions['LEFT']()
            clock.tick(FPS)


class Ai:
    def __init__(self):
        self.counter = 0
        self.best_x = 0  # integer of horizontal position
        self.best_r = None  # Matrix of the correction orientation of c_piece

        self.board = None
        self.c_piece = None
        self.n_piece = None

    def all_rotation(self, piece):
        list_of_rotations = [piece]
        rotated_piece = piece
        for _ in range(3):  # Tetriminos have max 4 unique rotations, the input rotation is already logged
            rotated_piece = [[rotated_piece[y][x] for y in range(len(rotated_piece))] for x in
                             range(len(rotated_piece[0]) - 1, -1, -1)]
            if rotated_piece not in list_of_rotations:
                list_of_rotations.append(rotated_piece)
            else:
                break
        return list_of_rotations

    def collision(self, board, piece, x, y):
        for cy, row in enumerate(piece):
            for cx, cell in enumerate(row):
                try:
                    if cell and board[cy + y][cx + x]:
                        return True
                except IndexError:
                    return True
        return False

    def simulate_board(self, board, piece, x):
        test_y = 0
        simulated_board = [row[:] for row in board]
        while not self.collision(simulated_board, piece, x, test_y):  # Simulate Hard Drop
            test_y += 1
        for cy, row in enumerate(piece):  # Add the piece to the simulated board
            for cx, val in enumerate(row):
                simulated_board[cy + test_y - 1][cx + x] += val

        return simulated_board

    def score(self, board):
        tol_height = 0
        for x in range(10):
            for y in range(20):
                if board[y][x] != 0:
                    tol_height += (20 - y)
                    break
        hole_count = 0
        for y in range(1, 20):
            for x in range(10):
                if board[y][x] == 0:
                    for i in range(1, y + 1):
                        if board[y - i][x] != 0:
                            hole_count += 1
                            break
        line_cleared = 0
        for row in board:
            if 0 not in row:
                line_cleared += 1
        bumpiness = 0
        for i in range(9):
            h = [20, 20]
            for y1 in range(20):
                if board[y1][i] != 0:
                    h[0] = y1
                    break
            for y2 in range(20):
                if board[y2][i + 1] != 0:
                    h[1] = y2
                    break
            bumpiness += abs(h[0] - h[1])

        data = [line_cleared, tol_height, hole_count, bumpiness]
        weight = [0.76, -0.51, -0.36, -0.18]
        return weight[0] * data[0] + weight[1] * data[1] + weight[2] * data[2] + weight[3] * data[3]

    def best_move(self, next_piece_knowledge=False):
        score = -100
        # For each possible rotation of the current piece and position
        for test_c_r in self.all_rotation(self.c_piece):
            for test_c_x in range(11 - len(test_c_r[0])):
                if not self.collision(self.board, test_c_r, test_c_x, 0):
                    if next_piece_knowledge:
                        next_board = self.simulate_board(self.board, test_c_r, test_c_x)
                        # Given where the current piece,
                        # for each possible rotation of the current piece and position
                        for test_n_r in self.all_rotation(self.n_piece):
                            for test_n_x in range(11 - len(test_n_r[0])):
                                if not self.collision(next_board, test_n_r, test_n_x, 0):
                                    if self.score(self.simulate_board(next_board, test_n_r, test_n_x)) > score:
                                        score = self.score(self.simulate_board(next_board, test_n_r, test_n_x))
                                        self.best_r = test_c_r
                                        self.best_x = test_c_x
                    else:
                        if self.score(self.simulate_board(self.board, test_c_r, test_c_x)) > score:
                            score = self.score(self.simulate_board(self.board, test_c_r, test_c_x))
                            self.best_r = test_c_r
                            self.best_x = test_c_x

    def next_move(self, board, c_piece, n_piece):
        self.board = board
        self.c_piece = c_piece
        self.n_piece = n_piece

        # Next Piece Knowledge determined whether AI uses the next piece to plan the best move
        self.best_move(next_piece_knowledge=False)

        return self.best_r, self.best_x


if __name__ == '__main__':
    Tetris = Tetris()
    Tetris.run()
