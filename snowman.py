import pygame

#add variable named BLUE and set to color used for background
BLUE = (81, 95, 255)

pygame.init()
print("hello")
game_display = pygame.display.set_mode((800,600))

pygame.display.set_caption('Winter Wizard Jam')

#load snowman image. I was unable to figure out how to load without full path. error when /images/snowman.png
snowman=pygame.image.load("images/snowman.png").convert_alpha()

fps = 60
clock = pygame.time.Clock()

play = True

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    game_display.fill(BLUE)

    #display image at the bottom in the middle of the screen
    game_display.blit(snowman, (250,300))

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
