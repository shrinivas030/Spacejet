import pygame
import random

mainclock=pygame.time.Clock()
def mos():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

WIDTH = 580
HEIGHT = 700
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
backgrond=pygame.image.load("image/backimgs.png")
pygame.display.set_caption("Shmup!")
mo=[]
momo=["mediam1.png","mediam2.png","mediam1.png","mediam2.png","mediam3.png","mediam4.png","small1.png","small2.png",
      "mediam3.png","small1.png"]
for im in momo:
    mo.append(pygame.image.load(im))
clock = pygame.time.Clock()
play=pygame.mixer.music.load("snd.wav")
snd=pygame.mixer.Sound("Laser.wav")
class Plyare(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("player.png")
        self.mini_image=pygame.transform.scale(self.image,(20,20))
        self.rect=self.image.get_rect()
        self.radius=20
        self.rect.centerx=WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.sheld=100
        self.shoot_time=pygame.time.get_ticks()
        self.live=3
        self.hide_time=pygame.time.get_ticks()
        self.hide_fag=False
    def Shoot(self):
        now=pygame.time.get_ticks()
        if now-self.shoot_time>250:
            self.shoot_time=now
            bullet=Bullet(self.rect.centerx,self.rect.bottom)
            all_sprites.add(bullet)
            bullets.add(bullet)
            snd.play( )

    def update(self):
        if self.hide_fag and pygame.time.get_ticks()-self.hide_time>1000:
            self.hide_fag=False
            self.rect.centerx=WIDTH/2
            self.rect.bottom=HEIGHT-10
        keystatus=pygame.key.get_pressed()
        if keystatus[pygame.K_LEFT]:
            self.speedx-=10
        if keystatus[pygame.K_RIGHT]:
            self.speedx+=10
        self.rect.x=self.speedx

        if keystatus[pygame.K_SPACE]:
            player.Shoot()

        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0

    def hidden(self):
       self.hide_fag=True
       self.hide_time=pygame.time.get_ticks()
       self.rect.center=(WIDTH/2,HEIGHT+200)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.origin_image=random.choice(mo)
        self.image=self.origin_image.copy()
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width*0.9/3)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(10, 20)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed=random.randrange(-8,8)
        self.last_time = pygame.time.get_ticks()
    def rotate(self):
        now_time=pygame.time.get_ticks()
        if now_time-self.last_time>50:
            self.last_time=now_time
            self.rot = (self.rot + self.rot_speed) % 360
            new_imag=pygame.transform.rotate(self.origin_image, self.rot)
            old_center=self.rect.center
            self.image=new_imag
            self.rect=self.image.get_rect()
            self.rect.center=old_center
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(10, 20)
        #if self.rect.x>WIDTH and self.rect.y>HEIGHT:
         #   mos()


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("bulletimg1.png")
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-10
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom< 0:
            self.kill()
class Explore(pygame.sprite.Sprite):
    def __init__(self,size,center):
        pygame.sprite.Sprite. __init__(self)
        self.size=size

        self.image=eplor[self.size][0]
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.frame=0
        self.last_time=pygame.time.get_ticks()
        self.framerate=50

    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last_time>self.framerate:
            self.last_time=now
            self.frame+=1
            if self.frame==len(eplor[self.size]):
               self.kill()

            else:
                center=self.rect.center
                self.image=eplor[self.size][self.frame]
                self.rect=self.image.get_rect()
                self.rect.center=center
def draw_sheild(surface,x,y,pct):
    if pct<0:
        pct=0
    Bar_leng=100
    Bar_hei=10
    fill_pct=(pct/100)*Bar_leng
    out_line=pygame.Rect(x,y,Bar_leng,Bar_hei)
    in_line=pygame.Rect(x,y,fill_pct,Bar_hei)
    pygame.draw.rect(surface,GREEN,in_line,)
    pygame.draw.rect(surface,WHITE,out_line,2)
def draw_live(surface,x,y,lives,img):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x=x+30*i
        img_rect.y=y
        screen.blit(img,img_rect)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets=pygame.sprite.Group()
player = Plyare()
all_sprites.add(player)
for i in range(8):
   mos()

eplor={}
eplor['lg']=[]
eplor['sl']=[]
for i in range(9):
    file_name="image/regularExplosion0{}.png".format(i)
    img=pygame.image.load(file_name).convert()
    img.set_colorkey(BLACK)
    img_rect=img.get_rect()
    img_rect=pygame.transform.scale(img,(75,75))
    eplor['lg'].append(img_rect)
    img_rect=pygame.transform.scale(img_rect,(32,32))
    eplor['sl'].append(img_rect)

score=0
runinng=True
pygame.mixer.music.play(-1)
while runinng:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            runinng = False


    all_sprites.update()
    hit = pygame.sprite.spritecollide(player, mobs, True,pygame.sprite.collide_circle )
    for hits in hit:
        player.sheld -= hits.radius
        eplo=Explore('sl',hits.rect.center)
        all_sprites.add(eplo)
        mos()
        if player.sheld<=0:
            player.hidden()
            player.live -= 1
            player.sheld=100
    if player.live<=0:
        runinng=False

    hits=pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        score+=50-hit. radius
        epl=Explore('lg',hit.rect.center)
        all_sprites.add(epl)
        mos()


    screen.blit(backgrond,(0,0))
    all_sprites.draw(screen)
    draw_sheild(screen,5,5,player.sheld)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_live(screen,WIDTH-100,5,player.live,player.mini_image)
    pygame.display.flip()
    mainclock.tick(100)