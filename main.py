# import modules
import pygame
import sys

# create 2 floor to call and swap position when the bird reaches the latter 
def draw_floor():
    screen.blit(floor, (floor_x_pos,600))
    screen.blit(floor, (floor_x_pos+432,600))

pygame.init()

# set up flappy bird display
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
# background image
bg = pygame.image.load('assets/background-night.png')
bg = pygame.transform.scale2x(bg)
# floor image
floor = pygame.image.load('assets/floor.png')
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# bird image
bird = pygame.image.load('assets/yellowbird-midflap.png')
bird = pygame.transform.scale2x(bird)

# create a loop until the player quits the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # if the user exit the game the window is update and the frame rate is set to 60
    pygame.display.update()
    clock.tick(60)
    # blit image onto surface
    screen.blit(bg,(0, 0))
    screen.blit(floor, (floor_x_pos,600))
    # make the floor go backwards to seem like the bird is running forward
    floor_x_pos -= 1
    # called the function and swap the 2 floor position as stated with conditions above
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

# generate bird
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/yellowbird-midflap.png')
