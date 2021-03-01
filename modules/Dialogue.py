import pygame
from os import path, getcwd
from . import COLOURS as colour
from . import textwrapper as TW
from . import OBJECTS as OBJ

cwd = getcwd()

class Help_Text(pygame.sprite.Sprite):
    def __init__(self, parent, group, size, text, limit):
        pygame.sprite.Sprite.__init__(self)
        group.add(self)
        self.parent = parent
        #create a way to prevent over extending the text outside of box
        texts = TW.textwrap(text, 30)

        ###
        font = pygame.font.Font(path.join(cwd, "game\\textures\\text\\font.ttf"), size)
        render = font.render(f"{text}", True, (0,0,0))
        



        #load image
        x = 10
        y = 10
        self.image = pygame.Surface((x,y))
        
    def splitText(self, text):
        l = text.split()
        temp = ""
        for word in l:
            print(l)

        
    
    def update(self):
        
        pass