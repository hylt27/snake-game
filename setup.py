import pygame, sys
from pygame.math import Vector2
import random

class Rat:
    def __init__(self):
        self.randomize()


    def draw_rat(self):
        # create a rect for the rat and draw it
        rat_rect = pygame.Rect(self.position.x*cell_size, self.position.y*cell_size, cell_size, cell_size)
        screen.blit(rat, rat_rect)


    def randomize(self):
        # creates a random position vector
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.position = Vector2(self.x, self.y)

class Snake:
    def __init__(self):
        # create the body of a snake with 3 blocks length
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  # each element is a position vector
        self.direction = Vector2(0,0)
        self.new_block = False

        # sprites for snake body
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        # sound
        self.crunch_sound = pygame.mixer.Sound('Sound/Sound_crunch.wav')

    def draw_snake(self):
        for index, block in enumerate(self.body):
            x_pos = block.x*cell_size
            y_pos = block.y*cell_size
            snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)


            if index == 0:
                self.update_head_graphics(snake_rect)
            elif index == len(self.body) - 1:
                self.update_tail_graphics(snake_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, snake_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, snake_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, snake_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, snake_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, snake_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, snake_rect)

    def update_head_graphics(self, rect):
        head_direction = self.body[0] - self.body[1]

        if head_direction == Vector2(1,0):
            screen.blit(self.head_right, rect)
        elif head_direction == Vector2(-1,0):
            screen.blit(self.head_left, rect)
        elif head_direction == Vector2(0,1):
            screen.blit(self.head_down, rect)
        elif head_direction == Vector2(0,-1):
            screen.blit(self.head_up, rect)

    def update_tail_graphics(self, rect):
        tail_direction = self.body[-2] - self.body[-1]

        if tail_direction == Vector2(1,0):
            screen.blit(self.tail_left, rect)
        elif tail_direction == Vector2(-1,0):
            screen.blit(self.tail_right, rect)
        elif tail_direction == Vector2(0,1):
            screen.blit(self.tail_up, rect)
        elif tail_direction == Vector2(0,-1):
            screen.blit(self.tail_down, rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset_snake(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0,0)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.rat = Rat()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.rat.draw_rat()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        # checks if the snake ate the rat and then add a new block to the body
        if self.rat.position == self.snake.body[0]:
            self.rat.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.rat.position:
                self.rat.randomize()

    def check_fail(self):
        # checks if the snake hits the walls
        if self.snake.body[0].x < 0 or self.snake.body[0].x >= cell_number:
            self.game_over()
        if self.snake.body[0].y < 0 or self.snake.body[0].y >= cell_number:
            self.game_over()

        # checks if the snake hits its own body
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_grass(self):
        grass_color = (40,71,52)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, False, (0, 0, 0))
        x_pos = cell_size*cell_number - 60
        y_pos = cell_size*cell_number - 40
        score_rect = score_surface.get_rect(center = (x_pos, y_pos))
        rat_rect = rat.get_rect(midright = (score_rect.left, score_rect.centery))


        screen.blit(score_surface, score_rect)
        screen.blit(rat, rat_rect)

    def game_over(self):
        self.snake.reset_snake()




# general settings
pygame.mixer.pre_init()
pygame.init()
cell_size = 40
cell_number = 15
screen = pygame.display.set_mode((cell_size*cell_number, cell_size*cell_number))
clock = pygame.time.Clock()
rat = pygame.image.load('Graphics/rat.png').convert_alpha()
game_font = pygame.font.Font('LLPIXEL3.ttf', 25)

surface = pygame.Surface((100, 200))
surface.fill('blue')
test_rect = surface.get_rect(center=(200, 250))

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

while True:
    # check player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)


    screen.fill((21,71,52))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
