import pygame,random,sys

# 0:T, 1:S, 2:Z, 3:J, 4:L, 5:I, 6:O
# Re-drawn version of https://gist.github.com/silvasur/565419 with better Tetris rule compliance

tetriminos_shape = [
    [[1,1,1],
     [0,1,0]],
    [[0,2,2],
     [2,2,0]],
    [[3,3,0],
     [0,3,3]],
    [[4,0,0],
     [4,4,4]],
    [[0,0,5],
     [5,5,5]],
    [[6,6,6,6]],
    [[7,7],
     [7,7]]
]

tetriminos_colors = [
    pygame.Color(117,80,123),
    pygame.Color(78,154,6),
    pygame.Color(204,0,0),
    pygame.Color(52,101,164),
    pygame.Color(211,215,207),
    pygame.Color(6,152,154),
    pygame.Color(196,160,0)
]

FPS = 30

class Tetris:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        # Initial config of game window
        self.g_width = 450
        self.g_height = self.g_width*2
        self.block_size = int(self.g_width/10)
        self.w_width = self.g_width+5*self.block_size
        self.w_height = self.g_height
        self.fgColor = pygame.Color(255,253,252)
        self.bgColor = pygame.Color(37,37,37)
        self.small_font = pygame.font.Font('ArcadeClassic.TTF',40)
        self.big_font = pygame.font.Font('ArcadeClassic.TTF',80)

        self.window = pygame.display.set_mode((self.w_width,self.w_height+1))
        pygame.display.set_caption('Tetris')
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.key.set_repeat(250,25)

        # Initial game state
        self.bag = [0,1,2,3,4,5,6]
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.n_piece = tetriminos_shape[random.choice(self.bag)]
        self.bag.remove(tetriminos_shape.index(self.n_piece))
        self.new_piece()
        self.pause = False
        self.in_game = True
        self.level = 0
        self.score = 0
        self.line = 0
        pygame.time.set_timer(pygame.USEREVENT+1,1000)

    def new_piece(self):
        self.c_piece = self.n_piece
        if len(self.bag) == 0:
            self.bag = [0,1,2,3,4,5,6]
        self.n_piece = tetriminos_shape[random.choice(self.bag)]
        self.bag.remove(tetriminos_shape.index(self.n_piece))
        self.c_piece_x = int(5-len(self.c_piece[0])/2)
        self.c_piece_y = 0

        if self.collision(self.c_piece,(self.c_piece_x,self.c_piece_y)):
            self.in_game = False

    def draw_background(self):
        # Draw all none moving pieces
        self.window.fill(self.bgColor)
        # Draw play field
        pygame.draw.lines(self.window,self.fgColor,True,[(0,0),(self.g_width,0),
                                                         (self.g_width,self.g_height),(0,self.g_height)])
        for x in range(1,10):
            for y in range(1,20):
                pygame.draw.circle(self.window,self.fgColor,(x*self.block_size,y*self.block_size),2)
        # Draw side label: Next piece, level, score, and line
        next_text = self.small_font.render("Next",1,self.fgColor)
        self.window.blit(next_text,(int(self.g_width+(self.w_width-self.g_width)/2-next_text.get_width()/2),0))
        pygame.draw.lines(self.window,self.fgColor,True,[(int(self.g_width+(self.w_width-self.g_width)/2-2*self.block_size),next_text.get_height()),
                                                         (int(self.g_width+(self.w_width-self.g_width)/2+2*self.block_size),next_text.get_height()),
                                                         (int(self.g_width+(self.w_width-self.g_width)/2+2*self.block_size),
                                                          next_text.get_height()+2*self.block_size-1),
                                                         (int(self.g_width+(self.w_width-self.g_width)/2-2*self.block_size),
                                                          next_text.get_height()+2*self.block_size-1)])
        for x in range(1,4):
            pygame.draw.circle(self.window,self.fgColor,(int(self.g_width+(self.w_width-self.g_width)/2-2*self.block_size)+x*self.block_size,
                                                         next_text.get_height()+self.block_size),2)
        level = self.small_font.render("Level",1,self.fgColor)
        self.window.blit(level,(int(self.g_width+(self.w_width-self.g_width)/2-level.get_width()/2),next_text.get_height()+2*self.block_size))
        score = self.small_font.render("Score",1,self.fgColor)
        self.window.blit(score,(int(self.g_width+(self.w_width-self.g_width)/2-score.get_width()/2),5*next_text.get_height()+2*self.block_size))
        line = self.small_font.render("Line",1,self.fgColor)
        self.window.blit(line,(int(self.g_width+(self.w_width-self.g_width)/2-line.get_width()/2),8*next_text.get_height()+2*self.block_size))

    def draw_number(self):
        le_number = self.big_font.render(str(self.level),1,self.fgColor)
        pygame.draw.rect(self.window,self.bgColor,pygame.Rect((int(self.g_width+(self.w_width-self.g_width)/2-le_number.get_width()/2),
                                                               le_number.get_height()+2*self.block_size),
                                                              (le_number.get_width(),le_number.get_height())))
        self.window.blit(le_number,(int(self.g_width+(self.w_width-self.g_width)/2-le_number.get_width()/2),
                                    le_number.get_height()+2*self.block_size))
        s_number = self.small_font.render(str(self.score),1,self.fgColor)
        pygame.draw.rect(self.window,self.bgColor,pygame.Rect((int(self.g_width+(self.w_width-self.g_width)/2-s_number.get_width()/2),
                                                               6*s_number.get_height()+2*self.block_size),
                                                              (s_number.get_width(),s_number.get_height())))
        self.window.blit(s_number,(int(self.g_width+(self.w_width-self.g_width)/2-s_number.get_width()/2),
                                   6*s_number.get_height()+2*self.block_size))
        li_number = self.small_font.render(str(self.line),1,self.fgColor)
        pygame.draw.rect(self.window,self.bgColor,pygame.Rect((int(self.g_width+(self.w_width-self.g_width)/2-li_number.get_width()/2),
                                                               9*li_number.get_height()+2*self.block_size),
                                                              (li_number.get_width(),li_number.get_height())))
        self.window.blit(li_number,(int(self.g_width+(self.w_width-self.g_width)/2-li_number.get_width()/2),
                                    9*li_number.get_height()+2*self.block_size))

    def draw_foreground(self):
        for y,row in enumerate(self.c_piece):  # Draw Current Piece
            for x,val in enumerate(row):
                if val > 0:
                    pygame.draw.rect(self.window,tetriminos_colors[self.c_piece[y][x]-1],pygame.Rect(
                        (self.c_piece_x+x)*self.block_size+1,(self.c_piece_y+y)*self.block_size+1,self.block_size-2,self.block_size-2))
        for y,row in enumerate(self.board):  # Draw Board
            for x,val in enumerate(row):
                if val > 0:
                    pygame.draw.rect(self.window,tetriminos_colors[self.board[y][x]-1],pygame.Rect(
                        x*self.block_size+1,y*self.block_size+1,self.block_size-2,self.block_size-2))
        example_text = self.small_font.render("",1,self.fgColor)
        for y,row in enumerate(self.n_piece):  # Draw Next Piece
            for x,val in enumerate(row):
                if val > 0:
                    pygame.draw.rect(self.window,tetriminos_colors[self.n_piece[y][x]-1],pygame.Rect(
                        ((int(self.g_width+(self.w_width-self.g_width)/2-2*self.block_size+x*self.block_size+1),
                          int(example_text.get_height()+y*self.block_size+1),
                          self.block_size-2,self.block_size-2))))

    def collision(self,piece,offset):
        off_x,off_y = offset
        for cy,row in enumerate(piece):
            for cx,cell in enumerate(row):
                try:
                    if cell and self.board[cy+off_y][cx+off_x]:
                        return True
                except IndexError:
                    return True
        return False

    def move(self,delta_x):
        if self.in_game and not self.pause:
            next_x = self.c_piece_x+delta_x
            if next_x < 0:
                next_x = 0
            if next_x > 10-len(self.c_piece[0]):
                next_x = 10-len(self.c_piece[0])
            if not self.collision(self.c_piece,(next_x,self.c_piece_y)):
                self.c_piece_x = next_x

    def drop(self,soft_drop=False):
        if self.in_game and not self.pause:
            self.score += 1 if soft_drop else 0
            self.c_piece_y += 1
        if self.collision(self.c_piece,(self.c_piece_x,self.c_piece_y)):
            # Add currently piece to board
            for cy,row in enumerate(self.c_piece):
                for cx,val in enumerate(row):
                    self.board[cy+self.c_piece_y-1][cx+self.c_piece_x] += val
            self.new_piece()
            cleared_rows = 0
            while True:
                for i,row in enumerate(self.board):
                    if 0 not in row:
                        # Clear the full row
                        del self.board[i]
                        self.board = [[0 for _ in range(10)]]+self.board
                        cleared_rows += 1
                        break
                else:
                    break
            line_scores = [0,40,100,300,1200]
            self.line += cleared_rows
            self.score += line_scores[cleared_rows]*self.level
            if self.line >= self.level*6:
                self.level += 1
                delay = 1000-50*(self.level-1)
                delay = 100 if delay < 100 else delay
                pygame.time.set_timer(pygame.USEREVENT+1,delay)
            return True
        return False

    def hard_drop(self):
        if self.in_game and not self.pause:
            while not self.drop(soft_drop=True):
                pass

    def rotate_piece(self):
        if self.in_game and not self.pause:
            temp_piece = [[self.c_piece[y][x] for y in range(len(self.c_piece))] for x in range(len(self.c_piece[0])-1,-1,-1)]
            if not self.collision(temp_piece,(self.c_piece_x,self.c_piece_y)):
                self.c_piece = temp_piece

    def toggle_pause(self):
        self.pause = not self.pause

    def new_game(self):
        if not self.in_game:
            # Initial game state
            self.bag = [0,1,2,3,4,5,6]
            self.board = [[0 for _ in range(10)] for _ in range(20)]
            self.n_piece = tetriminos_shape[random.choice(self.bag)]
            self.bag.remove(tetriminos_shape.index(self.n_piece))
            self.new_piece()
            self.pause = False
            self.in_game = True
            self.level = 0
            self.score = 0
            self.line = 0
            pygame.time.set_timer(pygame.USEREVENT+1,1000)

    def run(self):
        key_actions = {
            'ESCAPE':sys.exit,
            'LEFT':lambda:self.move(-1),
            'RIGHT':lambda:self.move(+1),
            'DOWN':lambda:self.drop(soft_drop=True),
            'UP':self.rotate_piece,
            'SPACE':self.hard_drop,
            'p':self.toggle_pause,
            'RETURN':self.new_game
        }

        clock = pygame.time.Clock()
        while True:
            if not self.in_game:
                game_over = self.small_font.render("Game Over",1,self.fgColor)
                self.window.blit(game_over,(int(self.g_width/2-game_over.get_width()/2),int(self.g_height/2-game_over.get_height()/2)))
                return_message = self.small_font.render("Press RETURN",1,self.fgColor)
                self.window.blit(return_message,(int(self.g_width/2-return_message.get_width()/2),
                                                 int(game_over.get_height()/2+self.g_height/2-return_message.get_height()/2)))
            else:
                if self.pause:
                    paused = self.small_font.render("Paused",1,self.fgColor)
                    self.window.blit(paused,(int(self.g_width/2-paused.get_width()/2),int(self.g_height/2-paused.get_height()/2)))
                else:
                    self.draw_background()
                    self.draw_number()
                    self.draw_foreground()

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.USEREVENT+1:
                    self.drop(soft_drop=False)
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval('pygame.K_'+key):
                            key_actions[key]()
            clock.tick(FPS)

if __name__ == "__main__":
    Tetris = Tetris()
    Tetris.run()
