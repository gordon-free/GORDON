global lost
from pygame import *
from random import *

lost = 0

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
   def update(self):
       self.rect.y += self.speed
       if self.rect.y < 0:
           self.kill()
        
        

img_bullet = 'bullet.png'

class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_a] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_d] and self.rect.x < win_w - 80:
           self.rect.x += self.speed
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)

class Enemy(GameSprite):
   def update(self):
       self.rect.y += self.speed
       global lost
       if self.rect.y > win_h:
           self.rect.x = randint(80, win_w - 80)
           self.rect.y = 0
           lost = lost + 1
           
lost = 0
score = 0
goal = 10
max_lost = 3

win_w = 700
win_h = 500

window = display.set_mode((win_w, win_h))
display.set_caption('Шутер')

background = transform.scale(image.load('galaxy.jpg'), (700, 500))
hero = Player('rocket.png', 0, win_h - 100, 80, 100, 4)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_w - 80), -50, 80, 50, randint(1,5))
    monsters.add(monster)

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False 

    keys = key.get_pressed()
    if keys[K_SPACE]:
        hero.fire()
        mixer.music.load('fire.ogg')
        mixer.music.play()

    if not finish:
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for e in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        window.blit(background, (0,0))

        font_lost = font1.render("Пропущено: " + str(lost), 1, (255, 255, 55))
        window.blit(font_lost, (20, 70))

        hero.update()
        hero.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

    clock.tick(FPS)
    display.update()