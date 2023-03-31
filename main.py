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
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True


def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*2.5, 1)
    return new_bird


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):  # # replace the score position at end game screen with high score
    if game_state == 'main game':
        score_surface = game_font.render(f'Score:{int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score:{int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 625 ))
        screen.blit(high_score_surface, high_score_rect)


def up_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# compile the sound file to help python recognize it easier
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)  # add everytime insert sound
pygame.init()

# set up flappy bird display
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

# create variables for game
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# background image
bg = pygame.image.load('assets/background-night.png').convert()
# could add '.convert()' in order for pygame to load images faster
bg = pygame.transform.scale2x(bg)
# floor image
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# bird image
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
# create a rectangle around the bird to detect position
bird_rect = bird.get_rect(center=(100, 384))

# create pipe
surface_pipe = pygame.image.load('assets/pipe-green.png').convert_alpha()
surface_pipe = pygame.transform.scale2x(surface_pipe)
# add all the pipes create in this list
pipe_list = []

# end game screen
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

# bird timer
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200 )
# pipe timer
pipe_spawn = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn, 1200)
pipe_height = [200, 300, 400]

# add sound to game
sound_flap = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

# create a whi le  loop until the player quits the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -11
                sound_flap.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == pipe_spawn:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
        bird, bird_rect = bird_animation()

    # blit image onto surface
    screen.blit(bg, (0, 0))
    if game_active:
        # create bird gravity to make it appear to be falling
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement*0.8
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # take all the pipes in pipelist to put on the screen
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = up_score(score, high_score)
        score_display('game over')

    # make the floor go backwards to seem like the bird is running forward
    floor_x_pos -= 1

    # called the function and swap the 2 floor position as stated with conditions above
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    # if the user exit the game the window is update and the frame rate is set to 60
    pygame.display.update()
    clock.tick(120)
