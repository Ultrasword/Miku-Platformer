import pygame
from os import getcwd, path
from . import SCREEN
from . import COLOURS as colour

cwd = getcwd()

class Counter(pygame.sprite.Sprite):
    def __init__(self, display):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((150,50))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(colour.black)
        self.score = 0
        self.base = 0
        self.T_GROUP = pygame.sprite.GroupSingle()
        self.display = display
        self.TEXT = SCREEN.Text(self.rect.centerx,self.rect.centery,self.score,True,colour.white,20,self.T_GROUP,self.display)
        self.setPos()

    def setPos(self):
        size = self.display.get_size()
        self.rect.x = size[0] - self.rect.width
        self.rect.y = 0

    def change(self):
        if self.base != self.score:
            self.TEXT.changeText(self.score,True,colour.white,20)
        self.base = self.score

    def update(self):
        self.image.fill((0,0,0,0))
        self.change()
        self.T_GROUP.update()
        self.T_GROUP.draw(self.image)
