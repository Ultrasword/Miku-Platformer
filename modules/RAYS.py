import pygame
import math
from os import path, getcwd
from . import COLOURS as colour

cwd = getcwd()

#spinning line
class SpinningLine(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((200, 200))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center = (x, y))
        self.angle = 0
    def update(self):
        vec = round(math.cos(self.angle * math.pi / 180) * 100), round(math.sin(self.angle * math.pi / 180) * 100)
        self.angle = (self.angle + 1) % 360
        self.image.fill(0)
        pygame.draw.line(self.image, (255, 255, 0), (100 - vec[0], 100 - vec[1]), (100 + vec[0], 100 + vec[1]), 5)
        self.mask = pygame.mask.from_surface(self.image)


#ralyling
class V_RayLine(pygame.sprite.Sprite):
    def __init__(self, sprite, playerxPos, group=None): #playerxPos is
        super().__init__()
        self.sprite = sprite
        self.color = colour.red
        self.image = pygame.Surface((1,50))
        self.rect = self.image.get_rect()
        self.ratio = playerxPos
        self.playerxPos = int(self.sprite.rect.width * self.ratio)
        self.top = (self.sprite.rect.x + self.playerxPos, self.sprite.rect.centery)
        self.bottom = (self.sprite.rect.centerx, self.top[1] + 50)
        if not group == None:
            group.add(self)
    
    def draw_image(self, display):
        self.image.fill((255,0,0))
        display.blit(self.image, self.rect)

    def update(self):
        self.playerxPos = self.sprite.rect.width * self.ratio
        self.rect.x = self.sprite.rect.x + self.playerxPos
        self.rect.y = self.sprite.rect.centery
        #confusion
        self.top = (self.rect.x, self.sprite.rect.centery)
        self.bottom = (self.rect.centerx, self.rect.bottom)
        self.mask = pygame.mask.from_surface(self.image)

class H_RayLine(pygame.sprite.Sprite):
    def __init__(self, sprite, playeryPos, group):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = sprite
        self.color = colour.red
        self.image = pygame.Surface((50,1))
        self.rect = self.image.get_rect()
        self.ratio = playeryPos
        self.playeryPos = int(self.sprite.rect.height * self.ratio)
        self.left = (self.sprite.rect.centerx, self.sprite.rect.y + self.playeryPos)
        self.right = (self.left[0] + 50, self.sprite.rect.centery)
        group.add(self)
    
    def update(self):
        self.playeryPos = self.sprite.rect.height * self.ratio
        self.rect.x = self.sprite.rect.centerx
        self.rect.y = self.sprite.rect.y + self.playeryPos
        self.left = (self.sprite.rect.centerx, self.rect.y)
        self.right = (self.rect.x + 30, self.rect.centery)
        self.mask = pygame.mask.from_surface(self.image)

class View_Line(pygame.sprite.Sprite):
    def __init__(self, spr, player):
        pygame.sprite.Sprite.__init__(self)
        self.spr = spr
        self.player = player
        self.image = pygame.Surface((600,1))
        self.rect = self.image.get_rect()
        self.rect.centerx = spr.rect.centerx
        self.rect.centery = spr.rect.centery
    
    def In_Vision(self):
        col = pygame.sprite.collide_rect(self, self.player)
        if col:
            self.spr.attacking = True
        else:
            self.spr.attacking = False

    def update(self):
        self.image.fill((255,0,0))
        self.rect.centerx = self.spr.rect.centerx
        self.rect.centery = self.spr.rect.centery
        self.In_Vision()

"""
d = pygame.display.set_mode((500,500))
c = pygame.time.Clock()
pygame.init()
run = True
ray = RAYL(d)

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    ray.update()
    pygame.display.flip()
    c.tick(30)

"""