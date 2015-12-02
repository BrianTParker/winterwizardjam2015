import pygame
import sys
from pygame.locals import *
from enum import Enum
import random

BLUE = (81, 95, 255)
BLACK = (0, 0, 0)

pygame.init()


FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples


pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)

screen_width = 800
screen_height = 600

game_display = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption('Winter Wizard Jam')

player_width = 156
player_height = 237
player_speed = 7
player_posx = screen_width/2
player_posy = screen_height - player_height
snowman=pygame.image.load("images/snowman.png").convert_alpha()
snowman = pygame.transform.scale(snowman, (player_width, player_height))

water_drop = pygame.image.load("images/drop.png").convert_alpha()
water_drop = pygame.transform.scale(water_drop, (20, 50))

melted=pygame.image.load("images/melted.png").convert_alpha()
melted = pygame.transform.scale(melted, (player_width, player_height))


fps = 60
clock = pygame.time.Clock()

game_state = 'INTRO'

play = True



class Player(pygame.sprite.Sprite):
    def __init__(self, image, speed, posx, posy, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.speed = speed
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.rect = Rect(self.posx, self.posy, self.width, self.height)

    def move_right(self):
        self.posx += self.speed
        self.rect = Rect(self.posx, self.posy, self.width, self.height)

    def move_left(self):
        self.posx -= self.speed
        self.rect = Rect(self.posx, self.posy, self.width, self.height)

    def move_down(self):
        self.posy += self.speed
        self.rect = Rect(self.posx, self.posy, self.width, self.height)
    def update_rect(self):
        self.rect.x = self.posx
        self.rect.y = self.posy

    def update_image(self, new_image):
        self.image = new_image

    def change_speed(self, new_speed):
        self.speed = new_speed

    def get_random_position(self):
        self.posx =  random.randint(100, screen_width - 100)
        self.posy = random.randint(-500, -100)
        self.rect = Rect(self.posx, self.posy, 10, self.height)

player = Player(snowman, player_speed, player_posx, player_posy, player_width/2, player_height)
drop_list = []
for x in range(0,4):
    drop_list.append(Player(water_drop, 4, random.randint(100, screen_width - 100), random.randint(-500, -100), 20, 50))

music_playing = False
def intro_screen():
    global music_playing
    title_font = pygame.font.Font(None, 100)
    title = title_font.render("Winter Wizard Jam:", 1, BLACK)
    textrect = title.get_rect()
    textrect.centerx = game_display.get_rect().centerx
    textrect.top = game_display.get_rect().top + 40
    game_display.blit(title, textrect)

    title2 = title_font.render("Snowman Panic", 1, BLACK)
    textrect = title2.get_rect()
    textrect.centerx = game_display.get_rect().centerx
    textrect.top = game_display.get_rect().top + 110
    game_display.blit(title2, textrect)

    instruction_font = pygame.font.Font(None, 50)
    start = instruction_font.render("Press Space Bar to start!", 1, BLACK)

    if music_playing == False:
        music_playing = True
        pygame.mixer.music.load('music/menutrack.ogg')
        pygame.mixer.music.play(-1)

    textrect = start.get_rect()
    textrect.centerx = game_display.get_rect().centerx
    textrect.bottom = game_display.get_rect().bottom - 40
    game_display.blit(start, textrect)

while True:
    game_display.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if game_state == 'PLAY':

        keystate = pygame.key.get_pressed()
        if keystate[K_LEFT]:
            if player.posx >= 0:
                player.move_left()

        if keystate[K_RIGHT]:
            if player.posx <= screen_width - (player.width):
                player.move_right()


        game_display.blit(player.image, (player.posx, player.posy))
        for drop1 in drop_list:


            drop1.move_down()

            game_display.blit(drop1.image, (drop1.posx, drop1.posy))
            if drop1.posy >= screen_height + drop1.height:
                drop1.get_random_position()
            if pygame.sprite.collide_mask(player, drop1):
                player.update_image(melted)




        #game_display.blit(melted, (250, 250))

    elif game_state == 'INTRO':
        intro_screen()
        keystate = pygame.key.get_pressed()
        if keystate[K_SPACE]:
            game_state = 'PLAY'
            pygame.mixer.music.stop()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()


def check_for_collision(obj1, obj2):
    pass
