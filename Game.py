import pygame

pygame.init()

window_width = 1280
window_height = 720

window_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("A way out")
clock = pygame.time.Clock()

running_right = [pygame.image.load(f'santa_running_right/Run{frame}.png') for frame in range(1, 11)]
running_left = [pygame.image.load(f'santa_running_left/Run{frame}.png') for frame in range(1, 11)]
background = pygame.image.load('background/bulkhead-walls.png')


class Santa(object):
    def __init__(self, santa_x, santa_y, x, y):
        self.deadSanta_x = window_width/2 - 150
        self.deadSanta_y = 0.648 * window_height
        self.santa_x = santa_x
        self.santa_y = santa_y
        self.x = x
        self.y = y
        self.speed = 5
        self.left = False
        self.right = False
        self.run_count = 0
        self.standing = True

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


def refresh_window_display():

    window_display.blit(background, (0, 0))
    man.move_santa(window_display)
    pygame.display.update()


playing = True

man = Santa(120, 10, window_width/2 - 150, 0.648 * window_height)

while playing:

    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man.x > man.speed:
        man.x -= man.speed
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < window_width - man.speed - man.santa_x:
        man.x += man.speed
        man.right = True
        man.left = False
        man.standing = False

    elif keys[pygame.K_DOWN] and man.y < window_height - man.speed - 125:
        man.y += man.speed
        man.standing = False

    elif keys[pygame.K_UP] and man.y > man.santa_y + man.speed:
        man.y -= man.speed
        man.standing = False
    else:
        man.standing = True

    refresh_window_display()

pygame.quit()
