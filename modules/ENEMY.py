import pygame
from os import path, getcwd
from random import randint
from . import RAYS
from . import ATTACKS
from . import COLOURS as colour
from . import MUSIC

cwd = getcwd()

class Flute(pygame.sprite.Sprite):
    def __init__(self, x, y, clock, particles, player):
        pygame.sprite.Sprite.__init__(self) 
        self.particles = particles
        self.player = player
        #iDLE animation
        self.clock = clock
        self.idle_ani = []
        img = pygame.image.load(path.join(cwd, "sprites\\Flute\\0.png")).convert()
        img = pygame.transform.scale(img, (40,40))
        img.set_colorkey((0,255,0))#switch to colour.green
        for a in [0,0,1,1,2,2,4,4,5,4,4,2,2,1,1,0,0,-1,-1,-2,-2,-4,-4,-5,-4,-4,-2,-2,-1,-1]:
            t = pygame.transform.rotate(img, a)
            self.idle_ani.append(t)
        #attack ani
        #rect and stuff
        self.frame = 0
        self.image = self.idle_ani[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.V_ACCEL = [0,0,1,1,1,1,1,2,2,-1,-1,-1,-1,-1,-2,-2]
        self.H_ACCEL = [0,0,1,1,1,1,2,2]
        self.A_S = 0
        self.V_S = 0
        self.gravity = 6
        #stats
        self.HP = 20
        #bools
        self.IDLE = True
        self.ATTACK = False
        self.DIR = False
        self.MOVE = False
        self.INCHUNK = False
        self.SEEPLAYER = False
        #time
        self.PAUSE = 0
        self.DISTANCE = 0
        self.P_LIMIT = 4000
        self.D_LIMIT = 3000
        self.ATTACK_TIMER = 0
        #rays
        self.VISION = RAYS.View_Line(self, self.player)
        self.attacking = False
        #sound
        self.AUDIO = MUSIC.Effect(3)
        self.AUDIO.set_volume(0,0.02)
        
    def HitBlock(self, b):
        col = pygame.sprite.collide_rect(self,b)
        if col:
            self.MOVE = False
            if b.rect.right - 10 < self.rect.left < b.rect.right:
                self.rect.left = b.rect.right + 1
            elif b.rect.left + 10 > self.rect.right > b.rect.left:
                self.rect.right = b.rect.left - 1

    def update_timer(self):
        if self.MOVE:
            if self.DISTANCE > self.D_LIMIT:
                self.MOVE = False
                self.DISTANCE = 0
                self.D_LIMIT = randint(2500,6000)
                self.DIR = not self.DIR
            self.DISTANCE += self.clock.get_time()
        if not self.MOVE:
            if self.PAUSE > self.P_LIMIT:
                self.MOVE = True
                self.PAUSE = 0
                self.P_LIMIT = randint(4000,10000)
            self.PAUSE += self.clock.get_time()
        self.ATTACK_TIMER += self.clock.get_time()

    def InChunk(self, size):
        if self.rect.right < 0 or self.rect.left > size[0] or self.rect.bottom < 0 or self.rect.top > size[1]:
            self.INCHUNK = False
        else:
            self.INCHUNK = True

    def updatePos(self, x, y):
        self.rect.x += x
        self.rect.y = y
    
    def FluteIdle(self):
        if self.IDLE:
            if self.frame >= len(self.idle_ani):
                self.frame = 0
            if self.DIR:
                self.image = self.idle_ani[self.frame]
            else:
                self.image = pygame.transform.flip(self.idle_ani[self.frame],True,False)
            self.frame += 1
    
    def V_Move(self):
        if self.A_S >= len(self.V_ACCEL):
            self.A_S = 0
        self.rect.y += self.V_ACCEL[self.A_S]
        self.A_S += 1

    def FluteAttack(self):
        if self.ATTACK_TIMER > 5000 and self.attacking:
            self.AUDIO.play_effect("Flute_attack",0,0.01)
            self.ATTACK_TIMER = 0
            a = ATTACKS.Note(self, self.player, 0)
            self.particles.add(a)

    def X_Move(self):
        if self.MOVE:
            if self.V_S >= len(self.H_ACCEL):
                self.V_S = 0
            if self.DIR:
                self.rect.x -= self.H_ACCEL[self.V_S]
            else:
                self.rect.x += self.H_ACCEL[self.V_S]
            self.V_S += 1

    def FluteAnimation(self):
        self.FluteIdle()
        self.V_Move()
        self.X_Move()

    def update(self):
        if self.INCHUNK:
            self.update_timer()
            self.FluteAnimation()
            self.FluteAttack()
            self.VISION.update()

class Trumpet(pygame.sprite.Sprite):
    def __init__(self, x, y, clock, particles, player):
        pygame.sprite.Sprite.__init__(self)
        self.particles = particles
        self.player = player
        #iDLE animation
        self.clock = clock
        self.idle_ani = []
        img = pygame.image.load(path.join(cwd, "sprites\\Trumpet\\0.png")).convert()
        img.set_colorkey(colour.green)
        img = pygame.transform.scale(img, (50,40))
        for a in [0,0,1,1,2,2,4,4,5,4,4,2,2,1,1,0,0,-1,-1,-2,-2,-4,-4,-5,-4,-4,-2,-2,-1,-1]:
            t = pygame.transform.rotate(img, a)
            self.idle_ani.append(t)
        #attack ani
        #rect and stuff
        self.frame = 0
        self.image = self.idle_ani[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.V_ACCEL = [0,0,0,1,1,1,1,1,1,2,2,-1,-1,-1,-1,-1,-1,-2,-2]
        self.H_ACCEL = [0,0,0,1,1,1,1,1,2,2]
        self.A_S = 0
        self.V_S = 0
        self.gravity = 6
        #stats
        self.HP = 30
        #bools
        self.IDLE = True
        self.ATTACK = False
        self.DIR = False
        self.MOVE = False
        self.INCHUNK = False
        self.SEEPLAYER = False
        #time
        self.PAUSE = 0
        self.DISTANCE = 0
        self.P_LIMIT = 4000
        self.D_LIMIT = 3000
        self.ATTACK_TIMER = 0
        #rays
        self.VISION = RAYS.View_Line(self, self.player)
        self.attacking = False
        #sound
        self.AUDIO = MUSIC.Effect(3)
        self.AUDIO.set_volume(0,0.02)

    def HitBlock(self, b):
        col = pygame.sprite.collide_rect(self,b)
        if col:
            self.MOVE = False
            if b.rect.right - 10 < self.rect.left < b.rect.right:
                self.rect.left = b.rect.right + 1
            elif b.rect.left + 10 > self.rect.right > b.rect.left:
                self.rect.right = b.rect.left - 1

    def update_timer(self):
        if self.MOVE:
            if self.DISTANCE > self.D_LIMIT:
                self.MOVE = False
                self.DISTANCE = 0
                self.D_LIMIT = randint(3000,8000)
                self.DIR = not self.DIR
            self.DISTANCE += self.clock.get_time()
        if not self.MOVE:
            if self.PAUSE > self.P_LIMIT:
                self.MOVE = True
                self.PAUSE = 0
                self.P_LIMIT = randint(4000,10000)
            self.PAUSE += self.clock.get_time()
        self.ATTACK_TIMER += self.clock.get_time()

    def InChunk(self, size):
        if self.rect.right < 0 or self.rect.left > size[0] or self.rect.bottom < 0 or self.rect.top > size[1]:
            self.INCHUNK = False
        else:
            self.INCHUNK = True

    def updatePos(self, x, y):
        self.rect.x += x
        self.rect.y = y
    
    def TrumpetIdle(self):
        if self.IDLE:
            if self.frame >= len(self.idle_ani):
                self.frame = 0
            if self.DIR:
                self.image = self.idle_ani[self.frame]
            else:
                self.image = pygame.transform.flip(self.idle_ani[self.frame],True,False)
            self.frame += 1
    
    def V_Move(self):
        if self.A_S >= len(self.V_ACCEL):
            self.A_S = 0
        self.rect.y += self.V_ACCEL[self.A_S]
        self.A_S += 1

    def TrumpetAttack(self):
        if self.ATTACK_TIMER > 10000 and self.attacking:
            self.ATTACK_TIMER = 0
            a = ATTACKS.Note(self, self.player, 2)
            self.particles.add(a)

    def X_Move(self):
        if self.MOVE:
            if self.V_S >= len(self.H_ACCEL):
                self.V_S = 0
            if self.DIR:
                self.rect.x -= self.H_ACCEL[self.V_S]
            else:
                self.rect.x += self.H_ACCEL[self.V_S]
            self.V_S += 1

    def TrumpetAnimation(self):
        self.TrumpetIdle()
        self.V_Move()
        self.X_Move()

    def update(self):
        if self.INCHUNK:
            self.update_timer()
            self.TrumpetAnimation()
            self.TrumpetAttack()
            self.VISION.update()


"""d = pygame.display.set_mode((500,500))
g = pygame.sprite.Group()
f = Flute(250,250)
g.add(f)
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    d.fill((0,0,0))
    g.update()
    g.draw(d)
    f.InChunk(d)

    pygame.display.update()
    clock.tick(30)"""
        