import pygame
import random
import sys

FPS = 30


class Snake:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        # Initial config of game window
        self.b_width = 50
        self.b_height = 25
        self.block_size = 20
        self.w_width = self.b_width * self.block_size
        self.w_height = self.b_height * self.block_size
        self.font = pygame.font.Font('ArcadeClassic.TTF', 40)
        self.window = pygame.display.set_mode((self.w_width + 1, self.w_height + 40))
        pygame.display.set_caption('Snake')
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.fgColor = pygame.Color(255, 255, 255)
        self.bgColor = pygame.Color(0, 0, 0)
        self.sbColor = pygame.Color(255, 255, 255)
        self.apColor = pygame.Color(255, 0, 0)

        # Initialize the Game and Snake Body
        self.board = [[0 for _ in range(self.b_width)] for _ in range(self.b_height)]
        self.board[int(self.b_height / 2)][int(self.b_width / 2) - 1] = 2
        self.board[int(self.b_height / 2)][int(self.b_width / 2)] = 1  # 1 is always head
        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.score = 2
        self.in_game = True
        self.pause = False
        self.ai = False
        self.add_apple()
        pygame.time.set_timer(pygame.USEREVENT + 1, 150)

    def draw_background(self):
        self.window.fill(self.bgColor)
        pygame.draw.lines(self.window, self.fgColor, True,
                          ((0, 0), (self.w_width, 0), (self.w_width, self.w_height), (0, self.w_height)))
        for j in range(1, self.b_height):
            for i in range(1, self.b_width):
                pygame.draw.circle(self.window, self.fgColor, (i * self.block_size, j * self.block_size), radius=1)
        score = self.font.render("Score     {}".format(self.score), 1, self.fgColor)
        self.window.blit(score, (int(self.w_width - score.get_width()), int(self.w_height)))
        if self.ai:
            ai = self.font.render("AI   ON".format(self.score), 1, self.fgColor)
        else:
            ai = self.font.render("AI   OFF".format(self.score), 1, self.fgColor)
        self.window.blit(ai, (0, int(self.w_height)))

    def draw_board(self):
        if self.in_game and not self.pause:
            # 0: Nothing, >=1: Snake Body, -1: Apple
            for j in range(self.b_height):
                for i in range(self.b_width):
                    if self.board[j][i] > 0:
                        pygame.draw.rect(self.window, self.sbColor,
                                         pygame.Rect((i * self.block_size + 1, j * self.block_size + 1),
                                                     (self.block_size - 2, self.block_size - 2)))
                    if self.board[j][i] == -1:
                        pygame.draw.rect(self.window, self.apColor,
                                         pygame.Rect((i * self.block_size + 1, j * self.block_size + 1),
                                                     (self.block_size - 2, self.block_size - 2)))

    def add_apple(self):
        if self.in_game and not self.pause:
            for j in range(self.b_height):
                for i in range(self.b_width):
                    if self.board[j][i] == -1:
                        return

            r_x = random.randrange(0, self.b_width)
            r_y = random.randrange(0, self.b_height)
            while self.board[r_y][r_x] != 0:
                r_x = random.randrange(0, self.b_width)
                r_y = random.randrange(0, self.b_height)
            self.board[r_y][r_x] = -1

    def update(self):
        if self.in_game and not self.pause:
            for j in range(self.b_height):
                for i in range(self.b_width):
                    if self.board[j][i] > 0:
                        self.board[j][i] += 1
                    if self.board[j][i] > self.score:
                        self.board[j][i] = 0
            for j in range(self.b_height):
                for i in range(self.b_width):
                    if self.board[j][i] == 2:
                        if self.left:
                            if i == 0:
                                self.in_game = False
                                return
                            elif self.board[j][i - 1] > 0:
                                self.in_game = False
                                return
                            elif self.board[j][i - 1] == -1:
                                self.board[j][i - 1] = 1
                                self.score += 1
                                self.add_apple()
                                break
                            else:
                                self.board[j][i - 1] = 1
                                break
                        elif self.right:
                            if i == self.b_width-1:
                                self.in_game = False
                                return
                            elif self.board[j][i + 1] > 0:
                                self.in_game = False
                                return
                            elif self.board[j][i + 1] == -1:
                                self.board[j][i + 1] = 1
                                self.score += 1
                                self.add_apple()
                                break
                            else:
                                self.board[j][i + 1] = 1
                                break
                        elif self.up:
                            if j == 0:
                                self.in_game = False
                                return
                            elif self.board[j - 1][i] > 0:
                                self.in_game = False
                                return
                            elif self.board[j - 1][i] == -1:
                                self.board[j - 1][i] = 1
                                self.score += 1
                                self.add_apple()
                                break
                            else:
                                self.board[j - 1][i] = 1
                                break
                        elif self.down:
                            if j == self.b_height-1:
                                self.in_game = False
                                return
                            elif self.board[j + 1][i] > 0:
                                self.in_game = False
                                return
                            elif self.board[j + 1][i] == -1:
                                self.board[j + 1][i] = 1
                                self.score += 1
                                self.add_apple()
                                break
                            else:
                                self.board[j + 1][i] = 1
                                break

    def change_direction(self, direction):
        if direction == 'left' and not self.right:
            self.left = True
            self.right = self.up = self.down = False
        elif direction == 'right' and not self.left:
            self.right = True
            self.left = self.up = self.down = False
        elif direction == 'up' and not self.down:
            self.up = True
            self.left = self.right = self.down = False
        elif direction == 'down' and not self.up:
            self.down = True
            self.left = self.right = self.up = False

    def toggle_pause(self):
        self.pause = not self.pause

    def new_game(self):
        # Initialize the Game
        self.board = [[0 for _ in range(self.b_width)] for _ in range(self.b_height)]
        # Initial Snake Body
        self.board[int(self.b_height / 2)][int(self.b_width / 2)-1] = 2
        self.board[int(self.b_height / 2)][int(self.b_width / 2)] = 1  # 1 is always head
        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.score = 2
        self.in_game = True
        self.pause = False
        self.ai = False
        self.add_apple()
        pygame.time.set_timer(pygame.USEREVENT + 1, 150)

    def run(self):
        key_actions = {
            'ESCAPE': sys.exit,
            'LEFT': lambda: self.change_direction('left'),
            'RIGHT': lambda: self.change_direction('right'),
            'UP': lambda: self.change_direction('up'),
            'DOWN': lambda: self.change_direction('down'),
            'p': self.toggle_pause,
            'RETURN': self.new_game
        }
        while True:
            if not self.in_game:
                game_over = self.font.render("Game Over", 1, self.fgColor)
                self.window.blit(game_over, (
                    int(self.w_width / 2 - game_over.get_width() / 2),
                    int(self.w_height / 2 - game_over.get_height() / 2)))
                return_message = self.font.render("Press RETURN", 1, self.fgColor)
                self.window.blit(return_message, (int(self.w_width / 2 - return_message.get_width() / 2),
                                                  int(game_over.get_height() / 2 + self.w_height / 2 -
                                                      return_message.get_height() / 2)))
            else:
                if self.pause:
                    paused = self.font.render("Paused", 1, self.fgColor)
                    self.window.blit(paused, (
                        int(self.w_width / 2 - paused.get_width() / 2),
                        int(self.w_height / 2 - paused.get_height() / 2)))
                else:
                    self.draw_background()
                    self.draw_board()
            pygame.display.update()
            for event in list(pygame.event.get()):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval('pygame.K_' + key):
                            key_actions[key]()


if __name__ == '__main__':
    Snake = Snake()
    Snake.run()
