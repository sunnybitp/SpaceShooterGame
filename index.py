import pygame 
import random
from os import path
img_dir=path.join(path.dirname(__file__),'image')
snd_dir=path.join(path.dirname(__file__),'snd')

WIDTH = 360
HEIGHT = 480
FPS = 30

#defining Color
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

# initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("mygame")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('Showcard Gothic')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface , text_rect)

def newmob():
    m=Mob() 
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf,x,y,pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img,img_rect)





class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite. __init__(self)
        self.image = pygame.transform.scale(player_img,[50,38])
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH /2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10

        if keystate[pygame.K_RIGHT]:
            self.speedx = 10

        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

    def hide(self):
        self.hidden = True 
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite. __init__(self)
        self.image_orig = random.choice(rock_img)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width  * .85/ 2)
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update  > 50:
            self.last_update = now 
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig,self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center 
      
        


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top  > HEIGHT + 10 or self.rect.left< -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite. __init__(self)
    
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10


    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now 
            self.frame +=1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()

            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background,background_rect)
    draw_text(screen,"SPACE SHOOTER",40,WIDTH/2,HEIGHT/4)
    draw_text(screen,"SPACE TO FIRE",22,WIDTH/2,HEIGHT/2)
    draw_text(screen,"DEVELOPED BY : SUNNY",25,WIDTH/2,HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYUP:
                waiting = False


background = pygame.image.load(path.join(img_dir,"background.png")).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir,"player.png")).convert()
 
player_mini_img =pygame.transform.scale(player_img,(25,19))
player_mini_img.set_colorkey(BLACK)
 

bullet_img = pygame.image.load(path.join(img_dir,"laser.png")).convert()

rock_img = []
rock_list = ['rock1.png','rock2.png','rock3.png','rock4.png','rock5.png','rock6.png','rock7.png']

for rock in rock_list:
    rock_img.append(pygame.image.load(path.join(img_dir,rock)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'explosion{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)


    

#load Sound

shoot_sound = pygame.mixer.Sound(path.join(snd_dir,'laser.wav'))
explosion_sound = pygame.mixer.Sound(path.join(snd_dir,'explosion.wav'))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir,'rumble1.ogg'))
pygame.mixer.music.load(path.join(snd_dir,'background.wav'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)
game_over = True

running = True

while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets  = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        for i in range(8):
            newmob()
        score = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    hits= pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        score += 50 - hit.radius
        explosion_sound.play()
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        newmob()
    
    hits = pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
    for hit in  hits:
        player.shield -= hit.radius*2
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
           player_die_sound.play()
           death_explosion = Explosion(player.rect.center, 'player')
           all_sprites.add(death_explosion)
           player.hide()
           player.lives -= 1
           player.shield = 100

    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score),20,WIDTH/2,10)
    draw_lives(screen,WIDTH - 100,5,player.lives,player_mini_img)
    draw_shield_bar(screen,5,5,player.shield)

    pygame.display.flip()

pygame.quit()
