import pygame
import sys
from os import path

window_width = 1280
window_height = 768

wall_size = 64
grid_width = window_width/wall_size
grid_height = window_height/wall_size
black_colour = (0, 0, 0)
crimson_colour = (220, 20, 60)
orange_colour = (225, 173, 0)
white_colour = (255, 255, 255)
green_colour = (124, 252, 0)

window_display = pygame.display.set_mode((window_width, window_height))

running_right = [pygame.image.load(f'santa_running_right/Run{frame}.png') for frame in range(1, 11)]
running_left = [pygame.image.load(f'santa_running_left/Run{frame}.png') for frame in range(1, 11)]


class Santa(object):
    def __init__(self, game, x, y):
        self.santa_width = 200
        self.santa_height = 137
        self.x = x
        self.y = y
        self.speed = 5
        self.left = False
        self.right = False
        self.run_count = 0
        self.standing = True
        self.x_col = 0
        self.y_col = 0
        self.game = game
        self.hitbox = (self.x + 60, self.y + 5, 80, 120)

    def hit(self):
        print('hit')

    def move_santa(self, window_display):

        if self.run_count + 1 >= 30:
            self.run_count = 0

        if not self.standing:
            if self.left:
                window_display.blit(running_left[self.run_count // 3], (self.x, self.y))
                self.run_count += 1
            elif self.right:
                window_display.blit(running_right[self.run_count // 3], (self.x, self.y))
                self.run_count += 1
        else:
            if self.left:
                window_display.blit(running_left[0], (self.x, self.y))
            else:
                window_display.blit(running_right[0], (self.x, self.y))

        self.hitbox = (self.x + 60, self.y + 5, 80, 120)
        pygame.draw.rect(window_display, green_colour, self.hitbox, 2)

    def collisions(self):
        for block in self.game.blocks:
            if self.hitbox[1] > block.x < self.hitbox[1] + self.hitbox[3]:
                if block.y > self.hitbox[2] - self.hitbox[4] and block.y < self.hitbox[2]:
                    Santa.hit()


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


class Game:
    def __init__(self):
        pygame.init()
        self.window_width = 1280
        self.window_height = 736
        self.window_display = pygame.display.set_mode((window_width, window_height))
        self.caption = pygame.display.set_caption("A way out")
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat()
        self.maze()

    def maze(self):
        folder = path.dirname(__file__)
        self.maze_rows = []
        with open(path.join(folder, 'maze.txt'), 'r') as file:
            for line in file:
                self.maze_rows.append(line)

    def running_game(self):

        self.playing = True

        man = Santa(self, -30, 0)

        while self.playing:

            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    sys.exit()

            keys = pygame.key.get_pressed()
            man.move_santa(window_display)

            if keys[pygame.K_LEFT] and man.x > man.speed - 70:
                man.x -= man.speed
                man.left = True
                man.right = False
                man.standing = False

            elif keys[pygame.K_RIGHT] and man.x < window_width - man.speed - man.santa_width + 70:
                man.x += man.speed
                man.right = True
                man.left = False
                man.standing = False

            elif keys[pygame.K_DOWN] and man.y < window_height - man.speed - 125:
                man.y += man.speed
                man.standing = False

            elif keys[pygame.K_UP] and man.y > man.santa_height - man.speed - 125:
                man.y -= man.speed
                man.standing = False
            else:
                man.standing = True

            self.all_sprites.update()
            self.draw()
            man.move_santa(window_display)
            pygame.display.update()

    def start(self):
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        for row, tiles in enumerate(self.maze_rows):
            for column, tile in enumerate(tiles):
                if tile == '1':
                    Block(self, column, row)


    def grid(self):
        for x in range(0, window_width, wall_size):
            pygame.draw.line(self.window_display, white_colour, (x, 0), (x, window_height))
        for y in range(0, window_height, wall_size):
            pygame.draw.line(self.window_display, white_colour, (0, y), (window_width, y))

    def draw(self):
        self.window_display.fill(black_colour)
        self.grid()
        self.all_sprites.draw(self.window_display)
        pygame.display.flip()


s = Game()
while True:
    s.start()
    s.running_game()
