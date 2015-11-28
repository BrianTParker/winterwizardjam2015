import pygame

pygame.init()
print("hello")
game_display = pygame.display.set_mode((800,600))

pygame.display.set_caption('Winter Wizard Jam')

fps = 60
clock = pygame.time.Clock()

play = True

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False


    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
