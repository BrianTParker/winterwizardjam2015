import pygame
import sys
from pygame.locals import *
#add variable named BLUE and set to color used for background
BLUE = (81, 95, 255)

pygame.init()
print("hello")
screen_width = 800
screen_height = 600
game_display = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption('Winter Wizard Jam')

#load snowman image. I was unable to figure out how to load without full path. error when /images/snowman.png
snowman=pygame.image.load("images/snowman.png").convert_alpha()
#snowman = pygame.transform.scale(snowman, (200, 300))
x = 250
y = 300

fps = 60
clock = pygame.time.Clock()

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

	def update_position(self, speed):
		self.posx += speed
		self.rect = self.rect = Rect(self.posx, self.posy + 200, 10, 1)


player = Player(snowman, 7, 200, 350, 156, 237)


while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         pressed_left = True
        #         player.posx -= 10
        #     if event.key == pygame.K_RIGHT:
        #         pressed_right = True
        #         player.posx += 10
    keystate = pygame.key.get_pressed()
    if keystate[K_LEFT]:
        if player.posx >= 0:
            player.posx -= player.speed
    if keystate[K_RIGHT]:
        if player.posx <= screen_width - (player.width):
            player.posx += player.speed

    game_display.fill(BLUE)

    #display image at the bottom in the middle of the screen

    game_display.blit(player.image, (player.posx, player.posy))

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
