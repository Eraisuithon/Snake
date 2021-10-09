import pygame
from sys import exit
from pygame.math import Vector2
from random import randint
import json
from os.path import isfile


class Snake:
    def __init__(self, window):
        self.ate = False

        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
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

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def play_crunch(self):
        self.crunch_sound.play()

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
        background_rect = pygame.Rect(apple_rect.left - 1, apple_rect.top - 3, apple_rect.width + score_rect.width + 5,
                                      apple_rect.height + 5)  # I added or subtracted how I thought looked best

        pygame.draw.rect(self.screen, (167, 209, 61), background_rect)
        pygame.draw.rect(self.screen, (56, 74, 12), background_rect, 2)
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


class File:
    def __init__(self):
        self.file_name = 'Scores.txt'
        self.initialize_file_if_it_is_nonexistant()
        with open('Scores.txt') as file:
            self.data = json.load(file)

    @staticmethod
    def initialize_file_if_it_is_nonexistant():
        if not isfile('Scores.txt'):
            with open('Scores.txt', 'w') as file:
                json.dump([], file)

    def add_to_file(self, name, score):
        index = None
        for i, player in enumerate(self.data):
            if score >= player['Score']:
                index = i
                break
        else:
            self.data.append({'Name': name, 'Score': score})

        if index is not None:
            self.data.insert(index, {'Name': name, 'Score': score})

        if len(self.data) > 10:
            self.data = self.data[:-1]

        with open('Scores.txt', 'w') as file:
            json.dump(self.data, file)


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)  # I got these numbers from a suggestion online
        pygame.init()
        self.window = Window()
        self.clock = pygame.time.Clock()
        self.frame_rate = 60

        self.snake = Snake(self.window)
        self.fruit = Fruit(self.window)

        self.screen_update = pygame.USEREVENT
        pygame.time.set_timer(self.screen_update, 150)

        self.file = File()

        self.score = 0

    def did_lose(self):
        if not 0 <= self.snake.body[0].x < self.window.cell.number or \
                not 0 <= self.snake.body[0].y < self.window.cell.number:
            return True

        for block in self.snake.body[3:]:
            if self.snake.body[0] == block:
                return True

        return False

    def show_scores(self):
        self.window.screen.fill((175, 215, 70))
        self.window.draw_grass()

        x_pos = 0
        index = 0
        for player in self.file.data:
            text_surface = self.window.font(64).render(f"{player['Name']} : {player['Score']}", True, (56, 74, 12))

            cell_size = self.window.cell.size

            y_pos = 2 * index * cell_size
            index += 1

            text_rect = text_surface.get_rect(topleft=(x_pos, y_pos))

            self.window.screen.blit(text_surface, text_rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_r or event.key == pygame.K_RETURN:
                        self.__init__()
                        self.run()
                        pygame.quit()
                        exit()

    def game_over(self):
        game_over_surface = self.window.font(64).render('GAME OVER', True, (56, 74, 12))
        quit_surface = self.window.font(16).render('To Quit press Q', True, (56, 74, 12))
        retry_surface = self.window.font(16).render('To Retry press R', True, (56, 74, 12))
        save_score_surface = self.window.font(16).render('To Save Score press S', True, (56, 74, 12))

        x_pos = self.window.cell.size * self.window.cell.number / 2
        y_pos = self.window.cell.size * self.window.cell.number / 2

        game_over_rect = game_over_surface.get_rect(midbottom=(x_pos, y_pos))
        quit_rect = quit_surface.get_rect(topright=game_over_rect.bottomright)
        retry_rect = retry_surface.get_rect(topleft=game_over_rect.bottomleft)
        save_score_rect = save_score_surface.get_rect(topleft=retry_rect.bottomleft)

        cell_size = self.window.cell.size
        background_rect = pygame.Rect(cell_size * 5, cell_size * 8, cell_size * 10, cell_size * 3)

        self.window.draw_grass()
        pygame.draw.rect(self.window.screen, (167, 209, 61), background_rect)
        self.window.screen.blit(game_over_surface, game_over_rect)
        self.window.screen.blit(quit_surface, quit_rect)
        self.window.screen.blit(retry_surface, retry_rect)
        self.window.screen.blit(save_score_surface, save_score_rect)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_r:
                        self.__init__()
                        self.run()
                    if event.key == pygame.K_s:
                        self.input_score_screen()

            pygame.display.update()

    def input_score_screen(self):
        text = 'Enter your name: '
        inputed_text = ''

        x_pos = 0
        y_pos = 0

        while True:
            text_surface = self.window.font(32).render(text + inputed_text, True, (56, 74, 12))

            text_rect = text_surface.get_rect(topleft=(x_pos, y_pos))

            self.window.screen.fill((175, 215, 70))
            self.window.draw_grass()
            self.window.screen.blit(text_surface, text_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        inputed_text = inputed_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(inputed_text) == 4:
                            self.file.add_to_file(inputed_text, self.score)
                            self.show_scores()
                    elif len(inputed_text) < 4:
                        inputed_text += event.unicode

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
                        self.game_over()
                        pygame.quit()
                        exit()
                    if self.did_snake_eat():
                        self.score += 1

                        self.snake.play_crunch()
                        self.fruit.randomize_pos()
                        while self.did_fruit_spawn_on_snake():
                            self.fruit.randomize_pos()
                        self.snake.ate = True

                if event.type == pygame.KEYDOWN and not already_changed:
                    if self.make_move(event):
                        already_changed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.game_over()
                        pygame.quit()
                        exit()

            self.update()
            self.clock.tick(self.frame_rate)

    def did_fruit_spawn_on_snake(self):
        for block in self.snake.body:
            if block == self.fruit.pos:
                return True
        return False

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
        self.window.draw_score(self.score, self.fruit.image)
        pygame.display.update()
