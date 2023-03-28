# import modules
import pygame
import sys
import random


# create game constant
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = surface_pipe.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = surface_pipe.get_rect(midtop=(500, random_pipe_pos - 650))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(surface_pipe, pipe)
        else:
            flip_pipe = pygame.transform.flip(surface_pipe, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True


pygame.init()

# set up flappy bird display
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()

# create variables for game
gravity = 0.25
bird_movement = 0
game_active = True

# background image
bg = pygame.image.load(
    'assets/background-night.png').convert()  # could add '.convert()' in order for pygame to load images faster
bg = pygame.transform.scale2x(bg)
# floor image
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# bird image
bird = pygame.image.load('assets/yellowbird-midflap.png').convert()
bird = pygame.transform.scale2x(bird)
# create a rectangle around the bird to detect position
bird_rect = bird.get_rect(center=(100, 384))

# create pipe
surface_pipe = pygame.image.load('assets/pipe-green.png').convert()
surface_pipe = pygame.transform.scale2x(surface_pipe)
# add all the pipes create in this list
pipe_list = []

# pipe timer
pipe_spawn = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn, 1200)
pipe_height = [200, 300, 400]

# create a loop until the player quits the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -11
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
        if event.type == pipe_spawn:
            pipe_list.extend(create_pipe())
            print(create_pipe)

    # blit image onto surface
    screen.blit(bg, (0, 0))
    if game_active:
        # create bird gravity to make it appear to be falling
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)
        game_active = check_collision(pipe_list)
        # take all the pipes in pipelist to put on the screen
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

    # make the floor go backwards to seem like the bird is running forward
    floor_x_pos -= 1

    # called the function and swap the 2 floor position as stated with conditions above
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    # if the user exit the game the window is update and the frame rate is set to 60
    pygame.display.update()
    clock.tick(120)
