import pygame
from . import COLOURS as colour
from . import textwrapper as TW
from os import path, getcwd

cwd = getcwd()

class Block(pygame.sprite.Sprite):
    def __init__(self, column, row, layer, chunk, map, allBlock): #chunk should be a list of sprite groups
        pygame.sprite.Sprite.__init__(self)
        #add to respective chunks
        self.chunk = column // 10 #10 is the chunk size.    anything left beyond the map will be black
        chunk[self.chunk][1].append(self)
        chunk[self.chunk][0].add(self)
        #sprite stuff
        self.column = column
        self.row = row
        self.map = map
        self.map_position = (column, row)
        img = self.map.get_tile_image(column, row, layer)
        img.set_colorkey(colour.blue)
        self.image = img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        allBlock.add(self)
    
    def updatePos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)

class Transparent(pygame.sprite.Sprite):
    def __init__(self, column, row, layer, trans_chunk, map):
        pygame.sprite.Sprite.__init__(self)
        #add to respective chunks
        self.chunk = column // 10
        trans_chunk.add(self)
        #sprite stuff
        self.column = column
        self.row = row
        self.map = map
        img = self.map.get_tile_image(column, row, layer)
        img.set_colorkey(colour.blue)
        self.image = img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.ONSCREEN = False
    
    def checkinscreen(self, size):
        if self.rect.x > 0 and self.rect.x < size[0]:
            self.ONSCREEN = True

    def updatePos(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.mask = pygame.mask.from_surface(self.image)

class Portal(pygame.sprite.Sprite):
    def __init__(self, column, row, layer, trans_chunk, map, GAMEWORLD): #use gameowrld to change the world level
        pygame.sprite.Sprite.__init__(self)
        self.GAMEWORLD = GAMEWORLD
        self.chunk = column // 10
        self.column = column
        self.row = row
        trans_chunk.add(self)
        #sprite stuff
        self.image = map.get_tile_image(column, row, layer)
        self.rect = self.image.get_rect()
        self.ONSCREEN = False
        #TEXT
        self.Help_Text = WrappedText(self, "Press 'F' to use the door!", 25, 15)
    
    def checkinscreen(self, size):
        if self.rect.x > 0 and self.rect.x < size[0]:
            self.ONSCREEN = True

    def draw(self, display):
        display.blit(self.image, self.rect)
        #display.blit(self.bottom, (self.rect.x, self.rect.y+32))
    
    def checkifchange(self, player):
        col = pygame.sprite.collide_rect(self, player)
        if col:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                self.GAMEWORLD.level += 1

    def updatePos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.Help_Text.update()
        self.Help_Text.draw(self.GAMEWORLD.display)

class Coin(pygame.sprite.Sprite):
    def __init__(self, column, row, layer, trans_chunk, map):
        self.floating = [0,0,1,1,2,2,1,0,-1,-1,-2,-2,-1]
        self.i = 0
        pygame.sprite.Sprite.__init__(self)
        self.chunk = column // 10
        self.column = column
        self.row = row
        trans_chunk.add(self)
        #sprite stuff
        img = map.get_tile_image(column, row, layer)
        img.set_colorkey(colour.green)
        self.image = img
        self.rect = self.image.get_rect()
        self.ONSCREEN = False
    
    def updatePos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def checkinscreen(self, size):
        if self.rect.x > 0 and self.rect.x < size[0]:
            self.ONSCREEN = True

    def update(self):
        if self.i >= 13:
            self.i = 0
        self.rect.y += self.floating[self.i]
        self.i += 1

class JumpBoost(pygame.sprite.Sprite):
    def __init__(self, column, row, layer, trans_chunk, map):
        pygame.sprite.Sprite.__init__(self)
        self.chunk = column // 10
        self.column = column
        self.row = row
        trans_chunk.add(self)
        #sprite stuff
        img = map.get_tile_image(column, row, layer)
        img.set_colorkey(colour.green)
        self.image = img
        self.rect = self.image.get_rect()
        self.ONSCREEN = False
    
    def updatePos(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def checkinscreen(self, size):
        if self.rect.x > 0 and self.rect.x < size[0]:
            self.ONSCREEN = True

    def playerontop(self, player):
        col = pygame.sprite.collide_rect(self, player)
        if col:
            player.JUMP_BOOST = True
            player.jump_boost_timer = 0

    def update(self):
        pass

class WrappedText(pygame.sprite.Sprite):
    def __init__(self, parent, text, limit, size):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.texts = []
        font = pygame.font.Font(path.join(cwd, "game\\textures\\text\\font.ttf"), size)
        for x in TW.textwrap(text, limit):
            render = font.render(str(x), False, (0,0,0))
            self.texts.append(render)
        width = max([x.get_rect().width for x in self.texts])
        self.height = len(self.texts) * render.get_rect().height
        self.image = pygame.Surface((width, self.height))
        self.image.fill(colour.green)
        self.image.set_colorkey(colour.green)
        for x in range(len(self.texts)):
            rect = self.texts[x].get_rect()
            self.image.blit(self.texts[x], (0, rect.height * x))
        self.rect = self.image.get_rect()
        #################
    
    def updatePos(self):
        self.rect.centerx = self.parent.rect.centerx
        self.rect.y = self.parent.rect.top - self.height

    def draw(self, d):
        if self.parent.ONSCREEN:
            d.blit(self.image, self.rect)

    def update(self):
        self.updatePos()
        
class TextBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, text, d):
        pygame.sprite.Sprite.__init__(self)
        self.d = d
        self.image = pygame.Surface((1,1))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.TEXT = WrappedText(self, text, 30, 20)
        self.ONSCREEN = False
        self.INCHUNK = False

    def updatePos(self, x, y):
        self.rect.x += x
        self.rect.y = y
    
    def HitBlock(self, o):
        pass

    def InChunk(self, size): 
        if self.TEXT.rect.right > 0 and self.TEXT.rect.left < size[0]:
            self.ONSCREEN = True
            self.INCHUNK = True
        else:
            self.ONSCREEN, self.INCHUNK = False, False

    def update(self):
        self.TEXT.update()
        self.TEXT.draw(self.d)
