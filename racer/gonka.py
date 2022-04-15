import pygame as pg, sys
from pygame.locals import *
import random, time
 
#Initialzing 
pg.init()
 
#Setting up FPS 
FPS = 60
clock = pg.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SPEED1= 3
SCORE = 0
 
#Setting up Fonts
font = pg.font.SysFont("Times new roman", 60)
font_small = pg.font.SysFont("Arial", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pg.image.load("./AnimatedStreet.png")


#Create a white screen 
DISPLAYSURF = pg.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pg.display.set_caption("Gonka")
 
 
 
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pg.image.load("./Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_UP]:
            self.rect.move_ip(0, -5)
            # pg.mixer.music.load('./mus/car_sound.mp3')
            # pg.mixer.music.play()
        if pressed_keys[pg.K_DOWN]:
            self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
            if pressed_keys[pg.K_LEFT]:
             self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[pg.K_RIGHT]:
                self.rect.move_ip(5, 0)

class Enemy(pg.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pg.image.load("./Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            # SCORE += 1
            # self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("./coin1.png")
        self.rect= self.image.get_rect()
        # self.rect.center = (random.randint(40, SCREEN_WIDTH- 40), 0)
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED1)
        if (self.rect.top>600):
            self.rect.top=0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def add(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1= Coin()
#Creating Sprites Groups
enemies = pg.sprite.Group()
enemies.add(E1)
coins= pg.sprite.Group()
coins.add(C1)
all_sprites = pg.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
#Adding a new User event 
INC_SPEED = pg.USEREVENT + 1
pg.time.set_timer(INC_SPEED, 1000)
 
#Game Loop
while True:
    
    #Cycles through all events occurring  
    for event in pg.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.1     
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(f'Score:{SCORE}', True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    #Collision with coin
    if pg.sprite.spritecollideany(P1, coins):
        SCORE+=1
        # pg.mixer.Sound()
        pg.display.update()
        C1.add()


    #To be run if collision occurs between Player and Enemy
    if pg.sprite.spritecollideany(P1, enemies):
          pg.mixer.music.stop()
        #   pg.mixer.Sound('./mus/car crash.mp3').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pg.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(3)
          pg.quit()
          sys.exit()        
         
    pg.display.update()
    clock.tick(FPS)