import pygame
import sys
from pygame.locals import *
from enum import Enum
#add variable named BLUE and set to color used for background
BLUE = (81, 95, 255)
BLACK = (0, 0, 0)

pygame.init()

screen_width = 800
screen_height = 600

game_display = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption('Winter Wizard Jam')

#load snowman image. I was unable to figure out how to load without full path. error when /images/snowman.png
player_width = 156
player_height = 237
player_speed = 7
player_posx = screen_width/2
player_posy = screen_height - player_height
snowman=pygame.image.load("images/snowman.png").convert_alpha()
snowman = pygame.transform.scale(snowman, (player_width, player_height))


fps = 60
clock = pygame.time.Clock()

game_state = 'INTRO'

play = True



class Player:
    def __init__(self, image, speed, posx, posy, width, height):

        self.image = image
        self.speed = speed
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height


    def update_rect(self, newx, newy):
        self.rect = Rect(newx, newy, width, height)

    def update_image(self, new_image):
        self.image = new_image

    def change_speed(self, new_speed):
        self.speed = new_speed


player = Player(snowman, player_speed, player_posx, player_posy, player_width, player_height)


def intro_screen():
    title_font = pygame.font.Font(None, 100)
    title = title_font.render("Winter Wizard Jam:", 1, BLACK)
    title2 = title_font.render("Snowman Panic", 1, BLACK)
    instruction_font = pygame.font.Font(None, 50)
    start = instruction_font.render("Press Space Bar to start!", 1, BLACK)
    game_display.blit(title, (100, 40))
    game_display.blit(title2,(100, 120))
    game_display.blit(start, (200, 500))

while True:
    game_display.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         pressed_left = True
        #         player.posx -= 10
        #     if event.key == pygame.K_RIGHT:
        #         pressed_right = True
        #         player.posx += 10

    if game_state == 'PLAY':

        keystate = pygame.key.get_pressed()
        if keystate[K_LEFT]:
            if player.posx >= 0:
                player.posx -= player.speed
        if keystate[K_RIGHT]:
            if player.posx <= screen_width - (player.width):
                player.posx += player.speed



    #display image at the bottom in the middle of the screen

        game_display.blit(player.image, (player.posx, player.posy))

    elif game_state == 'INTRO':
        intro_screen()
        keystate = pygame.key.get_pressed()
        if keystate[K_SPACE]:
            game_state = 'PLAY'
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
