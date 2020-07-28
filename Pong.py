import pygame
import pygame.freetype
import random
import time
import math

# Variables
width = 1200
height = 600
field_width = 1100
net_width = 3
ball_radius = 10
ball_velocity = 10
paddle_width = 10
paddle_height = 100
paddle_velocity = 6

fgColor = pygame.Color(255, 255, 255)  # White
bgColor = pygame.Color(53, 53, 53)  # Dark Grey

# Draw the background
pygame.font.init()
font = pygame.font.Font("ArcadeClassic.TTF", 50)
screen = pygame.display.set_mode((width, height))
pygame.draw.rect(screen, bgColor, pygame.Rect(0, 0, width, height))
pygame.draw.line(screen, fgColor, (int(width / 2), 0), (int(width / 2), height), net_width)


class Ball:
    def __init__(self):
        self.x = width / 2
        self.y = height / 2
        self.vx = random.choice([-1, 1]) * ball_velocity
        self.vy = math.sqrt(ball_velocity**2-self.vx**2)

    def reset(self, side_won):
        self.x = int(width / 2)
        self.y = int(height / 2)
        if side_won == "left":
            self.vx = random.choice([0.5, 1]) * ball_velocity
        if side_won == "right":
            self.vx = random.choice([0.5, 1]) * -ball_velocity
        self.vy = math.sqrt(ball_velocity**2-self.vx**2)

    def draw(self, color):
        global screen, paddle_width
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), ball_radius)

    def update(self):
        global fgColor, bgColor

        # Collision with the top and bottom border
        if self.y + self.vy <= ball_radius or self.y + self.vy > height - ball_radius:
            self.vy = -self.vy
        # Collision with the left paddle
        if (width - field_width) / 2 - paddle_width <= self.x + self.vx - ball_radius \
                <= (width - field_width) / 2 \
                and self.vx < 0 \
                and l_paddle.y - l_paddle.height / 2 <= self.y <= l_paddle.y + l_paddle.height / 2:
            self.vx = ball_velocity - \
                      math.fabs((self.y - l_paddle.y) / (paddle_height/2) * (ball_velocity / (math.sqrt(2))))
            self.vy = (self.y - r_paddle.y)/math.fabs((self.y - r_paddle.y)) * math.sqrt(ball_velocity**2-self.vx**2) \
                if self.y != l_paddle.y else 0
            print('left', self.vx, self.vy)

        # Collision with the right paddle
        if width - (width - field_width) / 2 + paddle_width >= self.x + self.vx + ball_radius \
                >= width - (width - field_width) / 2 \
                and self.vx > 0 \
                and r_paddle.y - r_paddle.height / 2 <= self.y <= r_paddle.y + r_paddle.height / 2:
            self.vx = -(ball_velocity -
                        math.fabs((self.y - r_paddle.y) / (paddle_height/2) * (ball_velocity / (math.sqrt(2)))))
            self.vy = (self.y - r_paddle.y)/math.fabs((self.y - r_paddle.y)) * math.sqrt(ball_velocity**2-self.vx**2) \
                if self.y != r_paddle.y else 0
            print('right', self.vx, self.vy)

        self.draw(bgColor)
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.draw(fgColor)

        # End game Collision
        if self.x <= -ball_radius:  # Go off of left side
            game("right")
        if self.x >= width + ball_radius:  # Go off of right side
            game("left")


class Paddle:
    def __init__(self, player, side):
        self.y = int(height / 2)
        self.score = 0
        if player in ["Human", "Computer", "Wall"]:
            self.player = player
        if side in ["left", "right"]:
            self.side = side
        if player == "Wall":
            self.height = height
        if player in ["Human", "Computer"]:
            self.height = paddle_height

    def draw(self, color):
        global screen, width, height, paddle_width, paddle_height
        if self.side == "right" and self.player in ["Human", "Computer"]:
            pygame.draw.rect(screen, color, pygame.Rect(
                (int(width - (width - field_width) / 2), int(self.y - (paddle_height / 2))),
                (paddle_width, self.height)))
        elif self.side == "left" and self.player in ["Human", "Computer"]:
            pygame.draw.rect(screen, color, pygame.Rect(
                (int((width - field_width) / 2 - paddle_width), int(self.y - (paddle_height / 2))),
                (paddle_width, self.height)))
        elif self.side == "right" and self.player == "Wall":
            pygame.draw.rect(screen, color, pygame.Rect(
                (int(width - (width - field_width) / 2), 0),
                (paddle_width, self.height)))
        elif self.side == "left" and self.player == "Wall":
            pygame.draw.rect(screen, color, pygame.Rect(
                (int((width - field_width) / 2 - paddle_width), 0),
                (paddle_width, self.height)))

    def update(self):
        global fgColor, bgColor, paddle_height, paddle_velocity
        # Move the paddle
        self.draw(bgColor)
        if self.player == "Human":
            # Use mouse to control paddle location
            if paddle_height / 2 <= pygame.mouse.get_pos()[1] <= height - (paddle_height / 2):
                self.y = pygame.mouse.get_pos()[1]
        elif self.player == "Computer":
            if self.y > ball.y and self.y >= paddle_height / 2:
                self.y -= paddle_velocity
            if self.y < ball.y and self.y <= height - paddle_height / 2:
                self.y += paddle_velocity
        self.draw(fgColor)

    def win(self):
        self.score += 1
        pygame.draw.rect(screen, bgColor, pygame.Rect(0, 0, int((width - field_width) / 2 - paddle_width), height))
        pygame.draw.rect(screen, bgColor, pygame.Rect(int(width - (width - field_width) / 2 + paddle_width),
                                                      0, int((width - field_width) / 2 - paddle_width), height))


def score_update(l_score, r_score):
    if l_score < 10:
        l_score_text = font.render(str(l_score), 1, fgColor)
        pygame.draw.rect(screen, bgColor, pygame.Rect(int(width / 2 - 100 - l_score_text.get_width() / 2), 10,
                                                      l_score_text.get_width(), l_score_text.get_height()))
        screen.blit(l_score_text, (int(width / 2 - 100 - l_score_text.get_width() / 2), 10))
    else:
        win_text = font.render('WIN', 1, fgColor)
        pygame.draw.rect(screen, bgColor, pygame.Rect(int(width / 2 - 100 - win_text.get_width() / 2), 10,
                                                      win_text.get_width(), win_text.get_height()))
        screen.blit(win_text, (int(width / 2 - 100 - win_text.get_width() / 2), 10))
    if r_score < 10:
        r_score_text = font.render(str(r_score), 1, fgColor)
        pygame.draw.rect(screen, bgColor, pygame.Rect(int(width / 2 + 100 - r_score_text.get_width() / 2), 10,
                                                      r_score_text.get_width(), r_score_text.get_height()))
        screen.blit(r_score_text, (int(width / 2 + 100 - r_score_text.get_width() / 2), 10))
    else:
        win_text = font.render('WIN', 1, fgColor)
        pygame.draw.rect(screen, bgColor, pygame.Rect(int(width / 2 + 100 - win_text.get_width() / 2), 10,
                                                      win_text.get_width(), win_text.get_height()))
        screen.blit(win_text, (int(width / 2 + 100 - win_text.get_width() / 2), 10))


def game(side_won):
    global pause
    pause = True
    if side_won == "left":
        l_paddle.win()
        ball.reset("left")
    if side_won == "right":
        r_paddle.win()
        ball.reset("right")


# Main
ball = Ball()
ball.draw(fgColor)
r_paddle = Paddle(player="Human", side="right")
r_paddle.draw(fgColor)
l_paddle = Paddle(player="Computer", side="left")
l_paddle.draw(fgColor)
pygame.display.flip()

pause = False
while l_paddle.score <= 9 and r_paddle.score <= 9:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.draw.line(screen, fgColor, (int(width / 2), 0), (int(width / 2), height), net_width)
    ball.update()
    l_paddle.update()
    r_paddle.update()
    score_update(l_paddle.score, r_paddle.score)
    pygame.display.flip()
    if pause:
        ball.draw(fgColor)
        pygame.display.flip()
        time.sleep(2)
        pause = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
