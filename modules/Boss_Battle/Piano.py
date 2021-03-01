import pygame
from os import getcwd, path
from random import randint, choice
import json
from .. import ENEMY
from .. import ATTACKS
from .. import RAYS

cwd = getcwd()

#NO PIANO IS A BOSS, THE WANDS SOLDIER OR BOSS CUZ THE WAND WAS TAKEN OVER BY SOMEONE ELSE, MIKU"S ENEMY
#PIANO WAS MIND CONTROLLED
# "IMPORTANT!!!"
class PIANO(pygame.sprite.Sprite):
    def __init__(self, clock, display, keysList, spawnpoints, enemies):
        pygame.sprite.Sprite.__init__(self)
        self.allGroup = enemies
        self.keysList = keysList
        self.SPAWNPOINTS = spawnpoints
        self.custom_keys = []
        self.clock = clock
        self.display = display
        #get the boss character info
        with open(path.join(cwd, "sprites\\Piano\\info.json"),"r") as boss:
            data = json.load(boss)
            self.name = data["name"]
            self.TOTALHP = data["health"]
            self.HP = self.TOTALHP
            self.phases = data["phasenum"]
            self.phaseinfo = data["phases"]#a list of 2
            self.phaseHPchange = data["phasechange_health"]
            boss.close()
        self.phase = 0
        self.get_phaseData()
        #WAND art and stuff
        self.animation = []
        self.attack_ani = []
        self.phasechange_ani = []
        #stats and stuff
        self.move_timer = 0
        self.attack_timer = 0
        self.summon_timer = 0
        #some booleans and stuff
        self.facing = False
        self.move_iter = 0
        #load boss sprite
        dimensions = (50,150)
        img = pygame.image.load(path.join(cwd, "sprites\\Piano\\piano.png")).convert()
        img = pygame.transform.scale(img, self.display.get_size())
        img.set_colorkey((0,255,0))
        self.BOSS_Image = img
        self.image = pygame.Surface(self.display.get_size())
        self.image.blit(self.BOSS_Image, (0,0))
        self.rect = self.image.get_rect()
        #attacks and movement paterns
        self.current_move = choice(self.movement_patterns)
        self.set_movement_pattern()
        self.spawnlimit = 10
        self.summon_warrior(choice(self.SPAWNPOINTS))

    def get_phaseData(self):
        self.DMG = self.phaseinfo[self.phase]["damage"]
        self.attackSpeed = self.phaseinfo[self.phase]["attackSpeed"]
        self.movement_patterns = self.phaseinfo[self.phase]["movement"]

    def check_HP(self):
        if self.HP <= self.phaseHPchange[self.phase]:
            self.phase += 1

    def update_timer(self):
        self.attack_timer += self.clock.get_time()
        self.move_timer += self.clock.get_time()
        self.summon_timer += self.clock.get_time()
        if self.move_timer > 10000:
            self.move_timer = 0
            self.move_iter += 1
        if self.summon_timer > 5000:
            self.summon_warrior(choice(self.SPAWNPOINTS))
            self.summon_timer = 0

    def set_movement_pattern(self):
        if self.move_iter >= len(self.current_move):
            self.current_move = choice(self.movement_patterns)
            self.move_iter = 0

    def move_patterns(self):
        if self.attack_timer > self.attackSpeed:
            self.attack_timer = 0
            loco = self.current_move[self.move_iter]
            if loco == "summon":
                self.summon_warrior(choice(self.SPAWNPOINTS))
            
    def summon_warrior(self, loco):
        if len(self.custom_keys) > self.spawnlimit:
            pass
        else:
            self.custom_keys.append(Warrior(loco, self, self.allGroup))
    
    def warrior_physics(self, allBlocks, keysGroup):
        for w in self.custom_keys:
            col = w.checkifonGround(allBlocks)
            col2 = w.checkifonGround(keysGroup)
            if not col and w.onGround and not col2:
                w.onGround = False
            if col or col2:
                w.rect.y -= 1
                w.onGround = True
    
    def prevent_warrior_outside(self, left, right):
        for w in self.custom_keys:
            if w.rect.left < left or w.rect.right > right:
                w.DISTANCE = 1000

    def update(self):
        self.update_timer()
        self.display.blit(self.image, self.rect)
        


#USE TILED TO MAKE THE BATTLE MAP
class White_Key(pygame.sprite.Sprite):
    def __init__(self, col, row, layer, map, clock, keysGroup, keysList):
        pygame.sprite.Sprite.__init__(self)
        self.column = col
        self.row = row
        self.image = pygame.Surface((32,96))
        self.rect = self.image.get_rect()
        self.top = map.get_tile_image(col, row, layer)
        self.middle = map.get_tile_image(col, row+1, layer)
        self.bottom = map.get_tile_image(col, row+2, layer)
        self.height = 0
        self.start_timer = 0
        self.start_limit = col * 20 - col * 10
        keysGroup.add(self)
        keysList.append(self)
        self.draw_key()
        self.dif = 1
    
    def draw_key(self):
        self.image.blit(self.top, (0,0))
        self.image.blit(self.middle, (0,32))
        self.image.blit(self.bottom, (0,64))
    
    def update_timer(self):
        if not self.start_timer > self.start_limit:
            self.start_timer += 1
        else:
            self.height -= self.dif
            if self.height < -50 or self.height > 0:
                self.dif *= -1
    
    def updatePos(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def get_moved_y(self):
        return self.row * 32 + int(self.height)

    def update(self):
        self.update_timer()
        pass

class Warrior(pygame.sprite.Sprite):
    def __init__(self, loco, piano, allGroup):
        pygame.sprite.Sprite.__init__(self)
        allGroup.append(self)
        self.PIANO = piano
        #animations
        self.V_MOVEMENT = [0,0,0,1,1,2,2,3,4,-4,-3,-2,-2,-1,-1]
        self.H_MOVEMENT = [0,0,1,1,1,1,1,2,2,2,2]
        rotations = [0,0,1,1,2,2,3,4,3,2,2,1,1,0,0,-1,-1,-2,-2,-3,-4,-3,-2,-2,-1,-1]
        self.base_ani = []
        img = pygame.image.load(path.join(cwd, "sprites\\Piano\\piano_warrior.png")).convert()
        img = pygame.transform.scale(img, (50,50))
        img.set_colorkey((0,255,0))
        for r in rotations:
            self.base_ani.append(pygame.transform.rotate(img, r))
        self.frame = 0
        #rect and stuff
        self.image = self.base_ani[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = int(loco.x)
        self.rect.y = int(loco.y)
        #spawntimer
        self.spawn_time = 0
        self.attack_timer = 0
        self.move_timer = 0
        #chunks and stuff
        self.INCHUNK = False
        self.onGround = False
        self.idle = True
        self.attacking = False
        self.facing = self.get_facing()
        self.MOVE = False
        #movement
        self.H_S = 0
        self.DISTANCE = 0
        self.D_LIMIT = randint(300,8000)
        self.PAUSE = 1000
        self.P_LIMIT = randint(400,1000)
        self.HP = 50
        #ray
        self.rays = pygame.sprite.Group()
        self.ray = RAYS.V_RayLine(self, 0.5 ,self.rays)
    
    def get_facing(self):
        if self.rect.centerx > 600:
            return True
        else:
            return False

    def run_gravity(self):
        if not self.onGround:
            self.rect.y += 1

    def update_timer(self):
        if self.MOVE:
            if self.DISTANCE > self.D_LIMIT:
                self.MOVE = False
                self.DISTANCE = 0
                self.D_LIMIT = randint(300,2000)
                self.facing = not self.facing
            self.DISTANCE += 1
        if not self.MOVE:
            if self.PAUSE > self.P_LIMIT:
                self.MOVE = True
                self.PAUSE = 0
                self.P_LIMIT = randint(400,1000)
            self.PAUSE += 1
        self.attack_timer += 1
        self.move_timer += 1
    
    def checkifonGround(self, group):
        col = pygame.sprite.groupcollide(self.rays, group, False, False, collided = None)
        return col

    def InChunk(self, size):
        if self.rect.right < 0 or self.rect.left > size[0] or self.rect.top > size[1] or self.rect.bottom < 0:
            self.facing = not self.facing
            self.INCHUNK = False
        else:
            self.INCHUNK = True

    def updatePos(self, x, y):
        self.rect.x += x
        self.rect.y = y
    
    def HitBlock(self, b):
        col = pygame.sprite.collide_rect(self,b)
        if col:
            self.MOVE = False
            if b.rect.right - 10 < self.rect.left < b.rect.right:
                self.rect.left = b.rect.right + 1
            elif b.rect.left + 10 > self.rect.right > b.rect.left:
                self.rect.right = b.rect.left - 1

    def draw(self, display):
        display.blit(self.image, self.rect)

    def idle_ani(self):
        if self.idle:
            if self.frame >= len(self.base_ani):
                self.frame = 0
            if self.facing:
                self.image = self.base_ani[self.frame]
            else:
                self.image = pygame.transform.flip(self.base_ani[self.frame], True, False)
            self.frame += 1

    def X_Move(self):
        if self.MOVE:
            if self.H_S >= len(self.H_MOVEMENT):
                self.H_S = len(self.H_MOVEMENT) - 3
            if self.facing:
                self.rect.x -= self.H_MOVEMENT[self.H_S]
            else:
                self.rect.x += self.H_MOVEMENT[self.H_S]
            self.H_S += 1

    def update(self):
        self.update_timer()
        self.run_gravity()
        self.ray.draw_image(self.PIANO.display)
        self.rays.update()
        self.idle_ani()
        self.X_Move()