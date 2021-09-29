import pygame
from sys import exit
from pygame.math import Vector2
from random import randint


# if someone presses two directions really quickly only the first will work
# one way to fix that is if direction can be Vector2(1,1)

class Snake:
    def __init__(self, window):
        self.ate = False

        self.body = [Vector2(6, 9), Vector2(6, 10), Vector2(5, 10)]
        self.window = window
        self.cell = self.window.cell
        self.direction = Vector2(1, 0)

        self.head_down = pygame.image.load('Images/head_down.png').convert_alpha()
        self.head_up = pygame.image.load('Images/head_up.png').convert_alpha()
        self.head_left = pygame.image.load('Images/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('Images/head_right.png').convert_alpha()

        self.body_dl = pygame.image.load('Images/body_dl.png').convert_alpha()
        self.body_ul = pygame.image.load('Images/body_ul.png').convert_alpha()
        self.body_dr = pygame.image.load('Images/body_dr.png').convert_alpha()
        self.body_ur = pygame.image.load('Images/body_ur.png').convert_alpha()

        self.body_vertical = pygame.image.load('Images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Images/body_horizontal.png').convert_alpha()

        self.tail_right = pygame.image.load('Images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Images/tail_left.png').convert_alpha()
        self.tail_up = pygame.image.load('Images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Images/tail_down.png').convert_alpha()

    def draw_snake(self):
        length = len(self.body)
        for i, block in enumerate(self.body):
            x_pos = self.cell.size * int(block.x)
            y_pos = self.cell.size * int(block.y)
            block_rect = pygame.Rect(x_pos, y_pos, self.cell.size, self.cell.size)
            if i == 0:
                next_block = self.body[i + 1]
                if block.x > next_block.x:
                    self.window.screen.blit(self.head_right, block_rect)
                elif block.x < next_block.x:
                    self.window.screen.blit(self.head_left, block_rect)
                elif block.y < next_block.y:
                    self.window.screen.blit(self.head_up, block_rect)
                else:
                    self.window.screen.blit(self.head_down, block_rect)
            elif i == length - 1:
                prev_block = self.body[i - 1]
                if block.x > prev_block.x:
                    self.window.screen.blit(self.tail_right, block_rect)
                elif block.x < prev_block.x:
                    self.window.screen.blit(self.tail_left, block_rect)
                elif block.y < prev_block.y:
                    self.window.screen.blit(self.tail_up, block_rect)
                else:
                    self.window.screen.blit(self.tail_down, block_rect)
            else:
                next_block = self.body[i + 1]
                prev_block = self.body[i - 1]
                if prev_block.x < block.x < next_block.x or prev_block.x > block.x > next_block.x:
                    self.window.screen.blit(self.body_horizontal, block_rect)

                elif prev_block.y < block.y < next_block.y or prev_block.y > block.y > next_block.y:
                    self.window.screen.blit(self.body_vertical, block_rect)

                elif prev_block.x < block.x and block.y < next_block.y or \
                        block.y < prev_block.y and next_block.x < block.x:
                    self.window.screen.blit(self.body_dl, block_rect)

                elif prev_block.x < block.x and block.y > next_block.y or \
                        block.y > prev_block.y and next_block.x < block.x:
                    self.window.screen.blit(self.body_ul, block_rect)

                elif block.y < next_block.y or block.y < prev_block.y:
                    self.window.screen.blit(self.body_dr, block_rect)

                else:
                    self.window.screen.blit(self.body_ur, block_rect)

    def move_snake(self):
        if not self.ate:
            self.body.pop(-1)

        self.ate = False
        self.body.insert(0, self.body[0] + self.direction)


class Fruit:
    def __init__(self, window):
        self.window = window
        self.cell = self.window.cell

        self.pos = None

        self.randomize_pos()

        self.image = pygame.image.load('Images/apple.png').convert_alpha()

    def randomize_pos(self):
        x = randint(0, self.cell.number - 1)
        y = randint(0, self.cell.number - 1)
        self.pos = Vector2(x, y)

    def draw_fruit(self):
        x_pos = self.cell.size * int(self.pos.x)
        y_pos = self.cell.size * int(self.pos.y)
        fruit_rect = pygame.Rect(x_pos, y_pos, self.cell.size, self.cell.size)
        self.window.screen.blit(self.image, fruit_rect)


class Cell:
    def __init__(self, size=40, number=20):
        self.size = size
        self.number = number


class Window:
    def __init__(self):
        self.cell = Cell()
        self.width = self.cell.size * self.cell.number
        self.height = self.cell.size * self.cell.number
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.font = lambda x: pygame.font.Font('Font/PoetsenOne-Regular.ttf', x)

    def draw_score(self, score, apple):
        score_text = str(score)
        score_surface = self.font(25).render(score_text, True, (56, 74, 12))
        x_pos = self.cell.size * self.cell.number - 60
        y_pos = self.cell.size * self.cell.number - 40

        score_rect = score_surface.get_rect(center=(x_pos, y_pos))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))

        self.screen.blit(score_surface, score_rect)
        self.screen.blit(apple, apple_rect)

    def draw_grass(self):
        grass_color = (167, 209, 61)
        grid_size = self.cell.size
        for i in range(0, grid_size, 2):
            for j in range(0, grid_size, 2):
                x_pos = i * int(grid_size)
                y_pos = j * int(grid_size)
                grass_rect = pygame.Rect(x_pos, y_pos, grid_size, grid_size)
                pygame.draw.rect(self.screen, grass_color, grass_rect)

        for i in range(1, grid_size, 2):
            for j in range(1, grid_size, 2):
                x_pos = i * int(grid_size)
                y_pos = j * int(grid_size)
                grass_rect = pygame.Rect(x_pos, y_pos, grid_size, grid_size)
                pygame.draw.rect(self.screen, grass_color, grass_rect)


class Game:
    def __init__(self):
        pygame.init()
        self.window = Window()
        self.clock = pygame.time.Clock()
        self.frame_rate = 60

        self.snake = Snake(self.window)
        self.fruit = Fruit(self.window)

        self.screen_update = pygame.USEREVENT
        pygame.time.set_timer(self.screen_update, 150)

    def did_lose(self):
        if not 0 <= self.snake.body[0].x < self.window.cell.number or \
                not 0 <= self.snake.body[0].y < self.window.cell.number:
            return True

        for block in self.snake.body[3:]:
            if self.snake.body[0] == block:
                return True

        return False

    def run(self):
        already_changed = False
        while True:
            self.window.screen.fill((175, 215, 70))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == self.screen_update:
                    already_changed = False
                    self.snake.move_snake()
                    if self.did_lose():
                        pygame.quit()
                        exit()
                    if self.did_snake_eat():
                        self.fruit.randomize_pos()
                        self.snake.ate = True

                if event.type == pygame.KEYDOWN and not already_changed:
                    if self.make_move(event):
                        already_changed = True

            self.update()
            self.clock.tick(self.frame_rate)

    def did_snake_eat(self):
        return self.snake.body[0] == self.fruit.pos

    def make_move(self, event):
        if event.key == pygame.K_RIGHT and self.snake.direction.x == 0:
            self.snake.direction = Vector2(1, 0)
            return True
        if event.key == pygame.K_LEFT and self.snake.direction.x == 0:
            self.snake.direction = Vector2(-1, 0)
            return True
        if event.key == pygame.K_UP and self.snake.direction.y == 0:
            self.snake.direction = Vector2(0, -1)
            return True
        if event.key == pygame.K_DOWN and self.snake.direction.y == 0:
            self.snake.direction = Vector2(0, 1)
            return True

        return False

    def update(self):
        self.window.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.window.draw_score(len(self.snake.body) - 3, self.fruit.image)
        pygame.display.update()
