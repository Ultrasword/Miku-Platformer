import pygame
from os import path, getcwd
from . import COLOURS as colour
from . import RAYS
from . import HP_BAR
from . import MUSIC

cwd = getcwd()

class MIKU(pygame.sprite.Sprite):
    def __init__(self, display, level, group, SUG, clock):
        pygame.sprite.Sprite.__init__(self)
        #load images
        self.dimensions = (40, 60)
        self.clock = clock
        #running
        self.run_ani = []
        for x in range(9):
            img = pygame.image.load(path.join(cwd, f"sprites\\Miku\\{x}.png")).convert()
            img = pygame.transform.scale(img, self.dimensions)
            img.set_colorkey(colour.green)
            self.run_ani.append(img)
        #jumping
        self.jump_ani = []
        for x in range(5):
            img = pygame.image.load(path.join(cwd, f"sprites\\Miku\\jump{x}.png")).convert()
            img = pygame.transform.scale(img, self.dimensions)
            img.set_colorkey(colour.green)
            self.jump_ani.append(img)
        #falling
        self.fall_ani = []
        for x in range(4):
            img = pygame.image.load(path.join(cwd, f"sprites\\Miku\\fall{x}.png")).convert()
            img = pygame.transform.scale(img, (self.dimensions))
            img.set_colorkey(colour.green)
            self.fall_ani.append(img)
        #idle
        self.idle_ani = []
        img = pygame.image.load(path.join(cwd, f"sprites\\Miku\\0.png")).convert()
        img = pygame.transform.scale(img, self.dimensions)
        img.set_colorkey(colour.green)
        self.idle_ani.append(img)
        #attack
        #do these later
        self.idle = True
        self.facing = True
        self.falling = False
        self.jumping = False
        self.crouching = False
        self.onGround = False
        self.running = False
        self.not_running = True
        self.frame = 0
        self.jframe = 0
        self.current_ani = self.idle_ani
        self.image = self.current_ani[self.frame]
        self.rect = self.image.get_rect()
        self.gravity = 6
        self.jump_speed = 13
        self.HITEDGE = False
        self.JUMP_BOOST = False
        #global things
        self.display = display
        self.baseSize = display.get_size()
        self.AUDIO = MUSIC.Effect(1)
        self.AUDIO.set_volume(0,0.05)
        self.AUDIO.add_layer(2)
        self.AUDIO.set_volume(1, 0.01)
        #stats
        self.HP = 100
        self.DMG = 8
        self.PWR = None
        self.speed = 2
        #timers
        self.jump_timer = 0
        self.jump_air_time = 0
        self.ani_speed = 0
        self.jump_boost_timer = 0
        #HPBAR
        self.HP_BAR = HP_BAR.HP(self, 20, self.baseSize[1] * 0.9)
        #rays
        self.rays = pygame.sprite.Group()
        ray = RAYS.V_RayLine(self, 0.3, self.rays)
        ray = RAYS.V_RayLine(self, 0.7, self.rays)
        #GROUPS
        SUG.append(self)
        group.add(self)
        self.group = group
        #map restrictions
        #cannot go beyond 1/3 of map (left) and 2/3 of map (right)
        self.R_left = self.baseSize[0] // 3
        self.R_right = self.baseSize[1] // 3 * 2

    def update_timer(self):
        self.ani_speed += self.clock.get_time()
        self.jump_timer += self.clock.get_time()
        if self.JUMP_BOOST:
            self.jump_boost_timer += self.clock.get_time()

    def jump_boost(self):
        if self.JUMP_BOOST:
            if self.jump_boost_timer > 1500:
                self.jump_boost_timer = 0
                self.JUMP_BOOST = False
            self.jump_speed = 20
        else:
            self.jump_speed = 13

    def reSize(self):
        size = self.display.get_size()
        self.R_left = size[0] // 3
        self.R_right = self.R_left * 2
        self.baseSize = size
    
    def Restrict_Miku_Movement(self, map):
        if map.s_x >= 0:
            if self.rect.right > self.R_right:
                self.rect.right = self.R_right
                self.HITEDGE = True
                if self.running:
                    map.s_x -= self.speed * 2
                elif self.falling or self.jumping:
                    map.s_x -= self.speed
                else:
                    map.s_x -= self.speed
            elif self.rect.left <= 0:
                self.rect.left = 0
        elif map.s_x <= -(map.entire_map_width - self.baseSize[0]):
            if self.rect.left < self.R_left:
                self.rect.left = self.R_left
                self.HITEDGE = True
                if self.running:
                    map.s_x += self.speed * 2
                elif self.falling or self.jumping:
                    map.s_x += self.speed
                else:
                    map.s_x += self.speed
            elif self.rect.right >= self.baseSize[0]:
                self.rect.right = self.baseSize[0]
        else:
            if self.rect.left < self.R_left:
                self.rect.left = self.R_left
                self.HITEDGE = True
                if self.running:
                    map.s_x += self.speed * 2
                elif self.falling or self.jumping:
                    map.s_x += self.speed * 2
                else:
                    map.s_x += self.speed
            elif self.rect.right > self.R_right:
                self.rect.right = self.R_right
                self.HITEDGE = True
                if self.running:
                    map.s_x -= self.speed * 2
                elif self.falling or self.jumping:
                    map.s_x -= self.speed * 2
                else:
                    map.s_x -= self.speed        

    def controls(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.rect.x += self.speed * 2
            self.facing = True
            self.running = False
            if self.onGround:
                self.current_ani = self.run_ani
                self.running = True
        elif (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.rect.x += -self.speed * 2
            self.facing = False
            self.running = False
            if self.onGround:
                self.current_ani = self.run_ani
                self.running = True
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.facing = False
            self.running = False
            if self.onGround:
                self.current_ani = self.run_ani
                self.running = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.facing = True
            self.running = False
            if self.onGround:
                self.current_ani = self.run_ani
                self.running = True
        else:
            self.running = False
            self.HITEDGE = False
        if not self.running:
            self.HITEDGE = False
        if keys[pygame.K_LSHIFT] or keys[pygame.K_DOWN]:
            self.crouching = True
            self.frame = 0
        else:
            self.crouching = False
            x = self.rect.x
            y = self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump_air_time += self.clock.get_time()
            if self.jump_timer > 500 and self.onGround:
                self.AUDIO.set_volume(0,0.01)
                self.AUDIO.play_effect("player_jump",0,0.01)
                self.jumping = True
                self.onGround = False
                self.current_ani = self.jump_ani
                self.jframe = 0
                self.jump_timer = 0
        else:
            self.jump_air_time = 0
            if self.jumping:
                self.jumping = False
                self.falling = True
                self.jframe = 0
            if not self.running and not self.falling and not self.jumping and self.onGround:
                self.frame = 0
                self.current_ani = self.idle_ani
                self.idle = True
                
    def MikuJump(self):
        if self.jumping:
            self.idle = False
            self.running = False
            self.rect.y -= self.jump_speed
            if self.jump_air_time > 460:
                self.jump_air_time = 0
                self.frame = 0
                self.jframe = 0
                self.jumping = False
                self.falling = True
                self.current_ani = self.fall_ani
            if self.jframe >= len(self.current_ani):
                self.jframe = len(self.current_ani) - 2
            if self.facing:
                self.image = pygame.transform.flip(self.current_ani[self.jframe], True, False)
            else:
                self.image = self.current_ani[self.jframe]
            if self.ani_speed > 100:
                self.jframe += 1
                self.ani_speed = 0
    
    def MikuFall(self):
        if self.falling:
            if self.jframe >= len(self.fall_ani):
                self.jframe = 0
            if self.facing:
                self.image = pygame.transform.flip(self.fall_ani[self.jframe], True, False)
            else:
                self.image = self.fall_ani[self.jframe]
            if self.ani_speed > 80:
                self.jframe += 1
                self.ani_speed = 0
    
    def MikuRun(self):
        if self.running:
            self.AUDIO.set_volume(1,0.01)
            self.AUDIO.timer_effect("player_walk",1,7,0.01)
            if self.frame >= len(self.current_ani):
                self.frame = 0
            if self.facing:
                self.image = pygame.transform.flip(self.current_ani[self.frame], True, False)
            else:
                self.image = pygame.transform.flip(self.current_ani[self.frame], False, False)
            if self.ani_speed > 80:
                self.frame += 1
                self.ani_speed = 0
    
    def MikuSneak(self):
        if self.crouching:
            self.image = pygame.transform.scale(self.image, (45, 50))
            x = self.rect.x
            y = self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def MikuIdle(self):
        if self.idle:
            self.not_running = True
            self.falling = False
            if self.frame >= len(self.current_ani):
                self.frame = 0
            if self.facing:
                self.image = pygame.transform.flip(self.current_ani[self.frame], True, False)
            else:
                self.image = pygame.transform.flip(self.current_ani[self.frame], False, False)
            if self.ani_speed > 80:
                self.frame += 1
                self.ani_speed = 0
        else:
            self.not_running = False

    def MikuAnimation(self):
        self.MikuIdle()
        self.MikuJump()
        self.MikuFall()
        self.MikuRun()
        self.MikuSneak()
        self.rays.update()
        self.HP_BAR.update()
    
    def checkifonGround(self, group):
        col = pygame.sprite.pygame.sprite.groupcollide(self.rays, group, False, False, collided = None)
        return col
        #implement into other script
    
    def runGravity(self):
        if not self.onGround:
            self.rect.y += self.gravity
        if not self.jumping and not self.onGround:
            self.falling = True
            self.current_ani = self.fall_ani
        self.jump_boost()

    def fallIntoVoid(self):
        if self.rect.top > self.display.get_size()[1]:
            return True
        else:
            return False

    def Damage(self, particles):
        col = pygame.sprite.groupcollide(self.group, particles, False, False, collided = None)
        if col:
            for c in col[self]:
                self.HP -= c.DMG
                self.HP_BAR.change_HP(self.HP)
                c.kill()            

    def update(self):
        self.update_timer()
        self.controls()
        self.MikuAnimation()
        self.runGravity()