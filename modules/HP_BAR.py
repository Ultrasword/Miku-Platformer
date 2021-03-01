import pygame
import math
from . import CHARACTER
from . import COLOURS as colour
from os import getcwd, path


cwd = getcwd()

class HP(pygame.sprite.Sprite):
    def __init__(self, parent, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.d_x = 120
        self.d_y = 40
        img = pygame.image.load(path.join(cwd, "game\\textures\\backgrounds\\HPBAR.png")).convert()
        img = pygame.transform.scale(img, (self.d_x, self.d_y))
        img.set_colorkey(colour.green)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w_x = self.rect.x + 10
        self.w_y = self.rect.y + 17
        self.white_bar = pygame.Surface((100,15))
        self.hp = self.parent.HP
        self.red_bar = pygame.Surface((self.hp,15))
    
    def reSize(self):
        pass

    def change_HP(self, health):
        if health < 0:
            self.hp = 0
        else:
            self.hp = health
        self.red_bar = pygame.Surface((self.hp,15))

    def update(self):
        self.white_bar.fill(colour.grey)
        self.red_bar.fill(colour.HP_BAR_red)
        self.parent.display.blit(self.image, self.rect)
        self.parent.display.blit(self.white_bar, (self.w_x, self.w_y))
        self.parent.display.blit(self.red_bar, (self.w_x,self.w_y))
        
