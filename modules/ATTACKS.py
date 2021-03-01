import pygame
from os import getcwd, path
from . import COLOURS as colour

cwd = getcwd()
strength = [5,10,20,50]
angles = [0,1,1,1,1,3,3,5,6,6,5,3,3,1,1,1,1,0,-1,-1,-1,-1,-3,-3,-5,-6,-6,-5,-3,-3,-1,-1,-1,-1]
bounce = [0,1,1,1,1,2,2,3,2,2,1,1,1,1,0,-1,-1,-1,-1,-2,-2,-3,-2,-2,-1,-1,-1,-1]

class Note(pygame.sprite.Sprite):
    def __init__(self, caster, player, dmg: int):
        pygame.sprite.Sprite.__init__(self)
        global strength, angles, bounce
        self.bounce = bounce
        self.player = player
        #images
        self.DMG = strength[dmg]
        img = pygame.image.load(path.join(cwd, f"game\\particles\\{self.DMG}.png")).convert()
        img = pygame.transform.scale(img, (16, 22))
        img.set_colorkey(colour.green)
        self.ani_list = []
        for a in angles:
            i = pygame.transform.rotate(img, a)
            self.ani_list.append(i)
        self.b_iter = 0
        self.frame = 0
        self.image = self.ani_list[self.frame]
        self.rect = self.image.get_rect()
        #rect
        self.rect.x = caster.rect.centerx
        self.rect.y = caster.rect.centery
        self.CalculateTrajectory()
        #bools
        self.speed = 3
    
    def NoteBounce(self):
        if self.b_iter >= len(self.bounce):
            self.b_iter = 0
        self.rect.y += self.bounce[self.b_iter]
        self.b_iter += 1

    def NoteAnimation(self):
        if self.frame >= len(self.ani_list):
            self.frame = 0
        if not self.DIR:
            self.image = self.ani_list[self.frame]
        else:
            self.image = pygame.transform.flip(self.ani_list[self.frame], True, False)
        self.frame += 1

    def CalculateTrajectory(self):
        tx = self.player.rect.centerx - self.rect.centerx
        if tx > 0:
            self.DIR = True
        else:
            self.DIR = False
        ty = self.player.rect.centery - self.rect.centery
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2((tx,ty)).normalize()

    def NoteMove(self):
        self.pos += self.direction * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def NoteKill(self):
        size = self.player.display.get_size()
        if self.rect.right < 0:
            self.kill()
        elif self.rect.left > size[0]:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.top > size[1]:
            self.kill()

    def update(self):
        self.NoteAnimation()
        self.NoteMove()
        self.NoteKill()


"""d = pygame.display.set_mode((500,500))
c = pygame.time.Clock()
pygame.init()
run = True
s = Note(2, 3, 2)

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    s.update()
    d.fill((0,0,0))
    d.blit(s.image, s.rect)
    pygame.display.flip()
    c.tick(30)"""