import pygame
import sys
from os import path
from time import sleep

window_width = 1280
window_height = 768
window_display = pygame.display.set_mode((window_width, window_height))

wall_size = 64
grid_width = window_width/wall_size
grid_height = window_height/wall_size
black_colour = (0, 0, 0)
crimson_colour = (220, 20, 60)
pink_colour = (255, 20, 147)
green_colour = (43, 255, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((wall_size, wall_size))
        self.image.fill(pink_colour)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def moving(self, x_m=0, y_m=0):
        if not self.collisions(x_m, y_m):
            self.x += x_m
            self.y += y_m

    def collisions(self, x_m=0, y_m=0):
        for block in self.game.blocks:
            if block.x == self.x + x_m and block.y == self.y + y_m:
                return True
        return False

    def refresh(self):
        self.rect.x = self.x * wall_size
        self.rect.y = self.y * wall_size

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.all_sprites = pygame.sprite.Group
        self.groups = game.all_sprites, game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((wall_size, wall_size))
        self.image.fill(crimson_colour)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * wall_size
        self.rect.y = y * wall_size
        self.window_display = window_display


class WinningTile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.all_sprites = pygame.sprite.Group
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((wall_size, wall_size))
        self.image.fill(green_colour)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * wall_size
        self.rect.y = y * wall_size
        self.window_display = window_display


class Game:
    def __init__(self):
        pygame.init()
        self.window_width = 1280
        self.window_height = 736
        self.window_display = pygame.display.set_mode((window_width, window_height))
        self.caption = pygame.display.set_caption("A way out")
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.maze()

    def maze(self):
        folder = path.dirname(__file__)
        self.maze_rows = []
        with open(path.join(folder, 'maze.txt'), 'r') as file:
            for line in file:
                self.maze_rows.append(line)

    def running_game(self):
        self.playing = True

        man = Player(self, 1, 1)

        while self.playing:

            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                man.moving(x_m=-1)
            elif keys[pygame.K_RIGHT]:
                man.moving(x_m=1)
            elif keys[pygame.K_DOWN]:
                man.moving(y_m=1)
            elif keys[pygame.K_UP]:
                man.moving(y_m=-1)

            if man.x == 12 and man.y == 3:
                win_screen = pygame.image.load('win.png')
                self.window_display.blit(win_screen, (1, 1))
                pygame.display.update()
                sleep(3)
                quit()
                sys.exit()

            self.all_sprites.update()
            man.refresh()
            self.draw()
            pygame.display.update()

    def start(self):
        self.all_sprites = pygame.sprite.Group()
        self.man = Player(self, 0, 0)
        self.blocks = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        for row, tiles in enumerate(self.maze_rows):
            for column, tile in enumerate(tiles):
                if tile == '1':
                    Block(self, column, row)
                if tile == 'W':
                    WinningTile(self, column, row)


    def draw(self):
        self.window_display.fill(black_colour)
        self.all_sprites.draw(self.window_display)
        pygame.display.update()


play = Game()
while True:
    play.start()
    play.running_game()
