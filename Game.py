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

deadSanta_x = window_width/2 - 150
deadSanta_y = 0.648 * window_height

santa_x = 120
santa_y = 10

x = window_width/2 - 150
y = 0.648 * window_height

speed = 4
left = False
right = False
run_count = 0
standing = True


def refresh_window_display():
    global run_count

    window_display.blit(background, (0, 0))

    if run_count + 1 >= 30:
        run_count = 0

    if not standing:
        if left:
            window_display.blit(running_left[run_count//3], (x, y))
            run_count += 1
        elif right:
            window_display.blit(running_right[run_count//3], (x, y))
            run_count += 1
    else:
        if left:
            window_display.blit(running_left[0], (x, y))
        else:
            window_display.blit(running_right[0], (x, y))

    pygame.display.update()


playing = True

while playing:

    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > santa_x + speed:
        x -= speed
        left = True
        right = False
        standing = False

    elif keys[pygame.K_RIGHT] and x < window_width - speed - santa_x:
        x += speed
        right = True
        left = False
        standing = False

    elif keys[pygame.K_DOWN] and y < window_height - speed - 125:
        y += speed
        standing = False

    elif keys[pygame.K_UP] and y > santa_y + speed:
        y -= speed
        standing = False
    else:
        standing = True

    refresh_window_display()

pygame.quit()
