import pygame
import sys
from pygame.locals import *
import random
import threading
import mysql.connector
import os



BLUE = (81, 95, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
cnx = ""
connected = False

try:
  cnx = mysql.connector.connect(user='player', password='Password!',
    host='bp72520.webfactional.com', port = '31730',
    database='leaderboards')
  if cnx.is_connected():
      print("Connected")
  else:
      print("Not Connected")
  connected = True

except mysql.connector.Error as err:
  pass
except AttributeError:
    pass



music_playing = False

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

snowman_slightly_melted=pygame.image.load("images/slightly_melted2.png").convert_alpha()
#snowman_slightly_melted = pygame.transform.scale(snowman_slightly_melted, (player_width, player_height))

snowman_mostly_melted=pygame.image.load("images/mostly_melted2.png").convert_alpha()
#snowman_mostly_melted = pygame.transform.scale(snowman_mostly_melted, (player_width, player_height))

water_drop = pygame.image.load("images/drop.png").convert_alpha()
water_drop = pygame.transform.scale(water_drop, (20, 40))

snow_flake = pygame.image.load("images/snowflake.png").convert_alpha()
snow_flake = pygame.transform.scale(snow_flake, (20, 40))

snowman_panic=pygame.image.load("images/snowmanpanic.png").convert_alpha()

spacebar=pygame.image.load("images/spacebar.png").convert_alpha()

snowman_head=pygame.image.load("images/snowman_head.png").convert_alpha()


melted=pygame.image.load("images/melted.png").convert_alpha()
#melted = pygame.transform.scale(melted, (player_width, player_height))

hit_sound = pygame.mixer.Sound("sfx/hit.wav")
snowflake_sound = pygame.mixer.Sound('sfx/snowflake.wav')
move_sound = pygame.mixer.Sound("sfx/move.wav")

drop_list = []

fps = 60
clock = pygame.time.Clock()

game_state = 'INTRO'

play = True

time = 0 #time in seconds
pygame.time.set_timer(USEREVENT+1, 1000)#1 second is 1000 milliseconds

class Player(pygame.sprite.Sprite):
    def __init__(self, image, speed, posx, posy, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.speed = speed
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.rect = Rect(self.posx + 50,self.posy + 40,self.width - 20,self.height - 80)

        self.health = 3
        self.score = 0

    def get_new_rect(self):
        self.rect = Rect(self.posx + 50,self.posy + 40,self.width - 20,self.height - 80)

    def move_right(self):
        self.posx += self.speed
        self.get_new_rect()

    def move_left(self):
        self.posx -= self.speed
        self.get_new_rect()

    def move_down(self):
        self.posy += self.speed
        self.get_new_rect()
    def update_rect(self):
        self.rect.x = self.posx + 40
        self.rect.y = self.posy

    def update_image(self):
        global player_height
        if self.health == 3:
            self.image = snowman
            self.height = 237
            self.posy = screen_height - self.height
        elif self.health == 2:
            self.image = snowman_slightly_melted

            self.height = 210
            self.posy = screen_height - self.height
        elif self.health == 1:
            self.image = snowman_mostly_melted
            self.height = 140
            self.posy = screen_height - self.height
        elif self.health == 0:
            self.height = 237
            self.posy = screen_height - self.height
            self.image = melted
        self.get_new_rect()


    def get_new_rect_other(self):
        self.rect = Rect(self.posx, self.posy, self.width, self.height)
    def draw_rectangle(self):
        pygame.draw.rect(game_display,BLACK,(self.posx + 50,self.posy + 40,self.width - 20,self.height - 80))



    def change_speed(self, new_speed):
        self.speed = new_speed

    def get_random_position(self):
        self.posx =  random.randint(10, screen_width - 100)
        self.posy = random.randint(-500, -100)
        self.rect = Rect(self.posx, self.posy, 10, self.height)

    def subtract_health(self):
        self.health -= 1
        if self.health < 0:
            health = 0

    def add_health(self):
        self.health += 1
        if self.health > 3:
            self.health = 3



class Object(pygame.sprite.Sprite):
    def __init__(self, image, speed, posx, posy, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.speed = speed
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.rect = Rect(self.posx + 50, self.posy, self.width, self.height)
        self.direction = "right"
        self.initialpos = posx

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

    def update_image(self):
        pass

    def get_new_rect(self):
        self.rect = Rect(self.posx, self.posy, self.width, self.height)
    def get_new_rect_other(self):
        self.rect = Rect(self.posx, self.posy, self.width, self.height)
    def draw_rectangle(self):
        pygame.draw.rect(game_display,BLACK,(self.posx,self.posy,self.width,self.height))



    def change_speed(self, new_speed):
        self.speed = new_speed

    def get_random_position(self):
        self.posx =  random.randint(10, screen_width - 100)
        self.posy = random.randint(-500, -100)
        self.rect = Rect(self.posx, self.posy, 10, self.height)

    def subtract_health(self):
        self.health -= 1
        if self.health < 0:
            health = 0

    def add_health(self):
        self.health += 1
        if self.health > 3:
            self.health = 3

    def switch_direction(self):
        if self.direction == "right":
            self.direction = "left"
        else:
            self.direction = "right"



drop_list = []
player = Player(snowman, player_speed, player_posx, player_posy, player_width/2, player_height)


for x in range(0,4):
    new_drop = Object(water_drop, 4, random.randint(10, screen_width - 100), random.randint(-500, -100), 20, 40)
    new_drop.get_new_rect_other()
    drop_list.append(new_drop)

snowflake = Object(snow_flake, 4, random.randint(10, screen_width - 100), -100, 20 , 40)


hit_buffer = 0
just_got_hit = False


def intro_screen():
    global music_playing

    if music_playing == False:
        music_playing = True
        pygame.mixer.music.load('music/menutrack.mp3')
        pygame.mixer.music.play(-1)


    title_font = pygame.font.Font("FreeSansBold.ttf", 70)
    #title = title_font.render("Winter Wizard Jam:", 1, BLACK)
    #textrect = title.get_rect()
    #textrect.centerx = game_display.get_rect().centerx
    #textrect.top = game_display.get_rect().top
    #game_display.blit(title, textrect)

    game_display.blit(snowman_panic, (0,0))

    snowman_head_left=pygame.transform.rotate(snowman_head, 20)
    game_display.blit(snowman_head_left, (-5, 225))
    snowman_head_right=pygame.transform.rotate(snowman_head, 340)
    game_display.blit(snowman_head_right, (585, 225))

    #title2 = title_font.render("Snowman Panic", 1, BLACK)
    #textrect = title2.get_rect()
    #textrect.centerx = game_display.get_rect().centerx
    #textrect.top = game_display.get_rect().top + 60
    #game_display.blit(title2, textrect)

    instruction_font = pygame.font.Font("FreeSansBold.ttf", 30)
    start = instruction_font.render(" ", 1, BLACK)

    game_display.blit(spacebar, (0, 450))

    high_score_count = 1
    high_score_offset = 10
    score_font = pygame.font.Font("FreeSansBold.ttf", 20)
    try:
        cursor = cnx.cursor()
        query = ("SELECT userName, score FROM scores "
         "order by score desc, id limit 10")

        top_scores = instruction_font.render("TOP SCORES", 1, WHITE)
        game_display.blit(top_scores, (290, 170))

        cursor.execute(query)
        for (userName, score) in cursor:
            score = score_font.render(str(high_score_count) + ". " + userName + "   " + str(score), 1, WHITE)
            game_display.blit(score, (230, 195 + high_score_offset))

            high_score_offset += 30
            high_score_count += 1
        cursor.close()

    except mysql.connector.Error as err:
        pass
    except AttributeError:
        pass



    textrect = start.get_rect()
    textrect.centerx = game_display.get_rect().centerx
    textrect.bottom = game_display.get_rect().bottom - 40
    game_display.blit(start, textrect)


def reset_game():
    global time
    global player
    global drop_list
    global game_state
    global music_playing
    music_playing = False
    time = 0
    drop_list = []
    player = Player(snowman, player_speed, player_posx, player_posy, player_width/2, player_height)
    for x in range(0,4):
        drop_list.append(Player(water_drop, 4, random.randint(10, screen_width - 100), random.randint(-500, -100), 20, 50))
    game_state = 'INTRO'




def increase_drop_rate():
    for drops in drop_list:
        drops.speed += .5
        #if drops.speed > 15.5:
            #drops.speed = 15.5


submit_score = True
kick_off_timer = False

##Input box code##################################
def get_key():
  while 1:

    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    elif event.type == pygame.QUIT:
        cnx.close()
        pygame.quit()
        quit()
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font("FreeSansBold.ttf",10)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 200,
                    (screen.get_height() / 2) - 10,
                    400,20), 0)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 200,
                    (screen.get_height() / 2) - 12,
                    400,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (0,0,0)),
                ((screen.get_width() / 2) - 195, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + " ".join(current_string))
  while 1:
    inkey = get_key()
    game_display.blit(player.image, (player.posx, player.posy))
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + " ".join(current_string))
  return " ".join(current_string)

##################################################
drop_snow_flake = False
while True:

    if player.health == 0:
        game_state = 'DEAD'
        music_playing = False
        pygame.mixer.music.stop()
    if just_got_hit == True:
        hit_buffer += 1
        if hit_buffer >= 50:
            hit_buffer = 0
            just_got_hit = False

    game_display.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT and game_state == "PLAY":
                move_sound.play()

            elif event.key == K_RIGHT and game_state == "PLAY":
                move_sound.play()
        if event.type == pygame.QUIT:
            try:
                cnx.close()
            except:
                pass
            pygame.quit()
            quit()

        if game_state == 'PLAY':
            if event.type == USEREVENT+1:
                time += 1
                if time % 2 == 0:
                    increase_drop_rate()
                if time % 20 == 0:
                    drop_snow_flake = True
                    snowflake = Object(snow_flake, 4, random.randint(10, screen_width - 100), -100, 20 , 40)


    if game_state == 'PLAY':

        if music_playing == False:
            music_playing = True
            pygame.mixer.music.load('music/mainsong.mp3')
            pygame.mixer.music.play(-1)

        counter_font = pygame.font.Font("FreeSansBold.ttf", 70)
        counter = counter_font.render(str(time), 1, WHITE)
        textrect = counter.get_rect()
        textrect.centerx = game_display.get_rect().centerx
        textrect.top = game_display.get_rect().top + 40
        game_display.blit(counter, textrect)


        keystate = pygame.key.get_pressed()
        if keystate[K_LEFT]:
            if player.posx >= 0:
                player.move_left()

        if keystate[K_RIGHT]:
            if player.posx <= screen_width - (player_width):
                player.move_right()



        game_display.blit(player.image, (player.posx, player.posy))
        #player.draw_rectangle()
        for drop1 in drop_list:


            drop1.move_down()

            game_display.blit(drop1.image, (drop1.posx, drop1.posy))
            if drop1.posy >= screen_height + drop1.height:
                drop1.get_random_position()
            if drop1.rect.colliderect(player.rect) and just_got_hit == False:
                hit_sound.play()
                just_got_hit = True
                player.subtract_health()
                player.update_image()




        if drop_snow_flake == True:
            game_display.blit(snowflake.image, (snowflake.posx, snowflake.posy))
            if snowflake.direction == "right":
                snowflake.posx += snowflake.speed/2
            else:
                snowflake.posx -= snowflake.speed/2
            if snowflake.posx >= snowflake.initialpos + 30:
                snowflake.direction = "left"
            if snowflake.posx <= snowflake.initialpos - 30:
                snowflake.direction = "right"
            snowflake.posy += snowflake.speed
            snowflake.get_new_rect()

            if(snowflake.rect.colliderect(player.rect)):
                drop_snow_flake = False
                snowflake_sound.play()
                player.add_health()
                player.update_image()
            elif snowflake.posy >=  screen_height:
                drop_snow_flake = False



    elif game_state == 'INTRO':
        intro_screen()
        keystate = pygame.key.get_pressed()
        if keystate[K_SPACE]:
            game_state = 'PLAY'
            pygame.mixer.music.stop()
            music_playing = False
    elif game_state == 'DEAD':
        print(drop_list[0].speed)
        if music_playing == False:
            music_playing = True
            pygame.mixer.music.load('music/deadtrack.mp3')
            pygame.mixer.music.play(-1)
        game_display.blit(counter, textrect)
        game_display.blit(player.image, (player.posx, player.posy))
        player.score = time
        game_state = 'INTRO'

        instructions_font = pygame.font.Font("FreeSansBold.ttf", 15)
        instructions = instructions_font.render("Just start typing your name and hit enter to submit your score.  Leave it blank and nothing will be submitted", 1, WHITE)
        textrect = instructions.get_rect()
        textrect.centerx = game_display.get_rect().centerx
        textrect.top = game_display.get_rect().top + 250
        game_display.blit(instructions, textrect)

        answer = ask(game_display, "Your name")


        if len(answer) > 0:

            try:
                cursor = cnx.cursor()

                add_score = ("INSERT INTO scores "
                     "(userName, score) "
                     "VALUES (%s, %s)")
                values = (answer, time)
                cursor.execute(add_score, values)
                cnx.commit()
                cursor.close()
            except mysql.connector.Error as err:
                pass
            except AttributeError:
                pass


        reset_game()

        music_playing = False
        pygame.mixer.music.stop()


    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()

            # call a function
