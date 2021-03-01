import pygame
from os import path, getcwd
from random import randint
from . import COLOURS as colour

cwd = getcwd()

clock = pygame.time.Clock()

class Button(pygame.sprite.Sprite):
    def __init__(self, display, image: int, function, grp, parent):
        pygame.sprite.Sprite.__init__(self)
        self.clock = clock
        #scaling and resizing
        self.display = display
        self.og_size = self.display.get_size()
        self.parent = parent
        #image
        img = pygame.image.load(path.join(cwd, f"game\\textures\\menu\\{image}.png")).convert()
        img = pygame.transform.scale(img, (self.og_size[0] // 3, self.og_size[1] // 8))
        self.IMG = img
        self.img = self.IMG
        self.image = self.IMG
        #animation
        self.ani_img = []
        for x in range(2):
            img = pygame.image.load(path.join(cwd, f"game\\textures\\menu\\{image}sel{x}.png")).convert()
            img = pygame.transform.scale(img, (self.og_size[0] // 3, self.og_size[1] // 8))
            self.ani_img.append(img)
        self.frame = 0
        self.ani_speed = 0
        #rect and positioning
        self.rect = self.image.get_rect()
        self.rect.centerx = self.og_size[0] // 2
        self.rect.centery = self.og_size[1] * (0.2 * image) + self.og_size[1] * 0.6
        self.yloco = image
        #button functions
        self.letter = function
        grp.add(self)
    
    def timers(self):
        self.ani_speed += self.clock.get_time()
    
    def reSize(self):
        size = self.display.get_size()
        newX = size[0] // 3
        newY = size[1] // 8
        self.img = pygame.transform.scale(self.IMG, (newX, newY))
        for x in range(len(self.ani_img)):
            img = pygame.transform.scale(self.ani_img[x], (newX, newY))
            self.ani_img[x] = img
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.centerx = size[0] // 2
        self.rect.y = size[1] * (0.2 * self.yloco) + size[1] * 0.6
    
    def check(self):
        m = pygame.mouse.get_pos()
        if self.rect.left < m[0] < self.rect.right and self.rect.top < m[1] < self.rect.bottom:
            c = pygame.mouse.get_pressed()
            self.animation()
            if c[0] == 1:
                self.function()
        else:
            self.image = self.img
        
    def animation(self):
        if self.frame == len(self.ani_img):
            self.frame = 0
        if self.ani_speed > 500:
            self.image = self.ani_img[self.frame]
            self.frame += 1
            self.ani_speed = 0

    def function(self):
        if self.letter == "s":
            self.parent.startgame()
        elif self.letter == "e":
            self.parent.leavegame()
            
    def update(self):
        self.timers()
        self.check()

class Text(pygame.sprite.Sprite):
    def __init__(self, cx, cy, text, bold, color, size, group, display):
        pygame.sprite.Sprite.__init__(self)
        font = pygame.font.Font(path.join(cwd, "game\\textures\\text\\font.ttf"), size)
        render = font.render(f"{text}", bold, color)
        self.image = render
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy
        self.display = display
        self.baseSize = display.get_size()
        group.add(self)
    
    def reSize(self):
        size = self.display.get_size()
        ratiox = self.baseSize[0] / size[0] * self.rect.width
        ratioy = self.baseSize[1] / size[1] * self.rect.height
        self.image = pygame.transform.scale(self.image, (int(ratiox), int(ratioy)))
        self.baseSize = size

    def changeText(self, text: str, bold: bool, color: tuple, size: int):
        font = pygame.font.Font(path.join(cwd, "game\\textures\\text\\font.ttf"), size)
        render = font.render(f"{text}", bold, color)
        self.image = render
    
    def changePos(self, cx, cy):
        self.rect.centerx = cx
        self.rect.centery = cy
    
    def update(self):
        pass

class Start_Screen:
    def __init__(self, display):
        self.clock = clock
        self.BUTTONS = pygame.sprite.Group()
        Button(display, 0, "s", self.BUTTONS, self)
        Button(display, 1, "e", self.BUTTONS, self)
        #set up the start screen
        self.og_size = display.get_size()
        self.display = display
        img = pygame.image.load(path.join(cwd, "game\\textures\\backgrounds\\background.jpg")).convert()#"game\\textures\\menu\\background.png")).convert()
        self.IMG = img
        self.image = img
        self.imgs = [self.image, self.image]
        self.x = -self.image.get_size()[0]
        self.speed = 1
        self.tempSize = self.og_size
        self.speed_timer= 0

        #exiting
        self.exit = False
        self.run = True
        self.show = True

        #game title!
        self.TITLE = Text(self.og_size[0] // 2, self.og_size[1] // 3, "HAPPY BIRTHDAY", True, colour.white, 100, self.BUTTONS, display)
        self.RGB = (4,4,4)
        self.increaser, self.increaseg, self.increaseb = 1,2,3
        #TIMER FOR title
        self.title_timer = 0
        with open(path.join(cwd, "game\\textures\\text\\titles.txt"), "r") as titles:
            data = titles.read()
            self.titles = [str(x) for x in data.split("\n")]
        self.current_title = self.titles[0]
            
    def leavegame(self):
        self.exit = True
        self.run = False

    def startgame(self):
        self.show = False
        self.run = False

    def transition(self):
        if self.show == False:
            for spr in self.BUTTONS:
                spr.kill()

    def BackGround(self):
        self.speed_timer += self.clock.get_time()
        for x in range(len(self.imgs)):
            self.display.blit(self.imgs[x], (self.x + (x * self.imgs[0].get_size()[0]), 0))
            if self.speed_timer > 10:
                self.x += self.speed
                self.speed_timer = 0
            if self.x > 0:
                self.x = -self.imgs[0].get_size()[0]

    def reSize(self):
        #get the image resize
        size = self.display.get_size()
        newX = self.image.get_size()[0] // self.tempSize[0] * size[0]
        newY = self.image.get_size()[1] // self.tempSize[1] * size[1]
        self.image = pygame.transform.scale(self.IMG, (newX, newY))
        for b in self.BUTTONS:
            b.reSize()
        self.tempSize = size
        self.x = -self.image.get_size()[0] // 2

    def rainbowText(self):
        for c in range(len(self.RGB)):
            if self.RGB[c] > 250 or self.RGB[c] < 4:
                if c == 0:
                    self.increaser *= -1
                elif c == 1:
                    self.increaseg *= -1 
                else:
                    self.increaseb *= -1
        r = self.RGB[0] + self.increaser
        g = self.RGB[1] + self.increaseg
        b = self.RGB[2] + self.increaseb
        self.RGB = (r,g,b)
        self.TITLE.changeText(self.current_title, True, self.RGB, 100)

    def show_start(self):
        while self.run:
            self.title_timer += 1
            if self.title_timer > 1000:
                self.title_timer = 0
                self.current_title = self.titles[randint(1,len(self.titles)-1)]
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.exit = True
                    self.run = False
                elif e.type == pygame.VIDEORESIZE:
                    self.reSize()
            
            self.BackGround()
            self.BUTTONS.update()
            self.BUTTONS.draw(self.display)
            self.rainbowText()
            pygame.display.flip()
            self.clock.tick(60)
            self.transition()

class Menu_Screen:
    def __init__(self, display):
        self.display = display



