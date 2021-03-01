import pygame
import pytmx
import json
from os import getcwd, path
from . import OBJECTS as OBJ #change to from .
from . import COLOURS as colour
from . import ENEMY
from . import MUSIC
from .Boss_Battle import Piano

cwd = getcwd()
pygame.init()

class Platform:
    def __init__(self, display, player, level, particles, GAMEWORLD):
        self.player = player
        self.display = display
        self.particles = particles
        self.GAMEWORLD = GAMEWORLD
        #load map
        self.map = pytmx.load_pygame(path.join(cwd, f"game\\levels\\level{level}.tmx"))
        self.allBlocks = pygame.sprite.Group()
        self.baseSize = self.display.get_size()
        self.TransChunks = pygame.sprite.Group()
        self.keysGroup = pygame.sprite.Group()
        self.keysList = []
        self.level = level
        self.MAPLEFT = 0
        self.MAPRIGHT = self.map.width * 32
        #######idk why this is here
        self.chunks = []
        x = 0
        while x < self.map.width:
            CHUNK = (pygame.sprite.Group(),[])
            self.chunks.append(CHUNK)
            x += 10
        ########
        self.AUDIO = MUSIC.Effect()
        self.AUDIO.set_volume(0,0.3)
        self.MUSIC = MUSIC.Music(self)
        self.MUSIC.set_up("1",0.05)
        self.MUSIC.play(-1)
        #display size
        self.left_chunk = 0
        self.right_chunk = display.get_size()[0] // self.map.tilewidth // 10 + 1
        #background
        self.IMG = pygame.image.load(path.join(cwd, f"game\\textures\\backgrounds\\level{level}_background.JPG")).convert()
        self.background = pygame.transform.scale(self.IMG, (display.get_size()[0] * 2, display.get_size()[1]))
        self.B_rect = self.background.get_rect()
        self.b_x = 0
        self.b_y = 0
        #draw all blocks
        self.ENEMIES = []
        self.BOSS_SPAWNPOINTS = []
        self.s_x = 0
        self.s_y = display.get_size()[1] - self.map.height * self.map.tileheight
        self.entire_map_width = self.map.width * self.map.tilewidth
        for layer in range(len(self.map.layers)):
            if isinstance(self.map.layers[layer], pytmx.pytmx.TiledObjectGroup):
                self.Spawn_Enemy(self.map.layers[layer])
            elif isinstance(self.map.layers[layer], pytmx.TiledTileLayer):
                if self.map.layers[layer].name == "Transparent":
                    for column in range(self.map.width):
                        for row in range(self.map.height):
                            temp = self.map.get_tile_image(column, row, layer)
                            if temp == None:
                                continue
                            temp = self.map.get_tile_properties(column, row, layer)
                            if "portal" in temp:
                                OBJ.Portal(column, row, layer, self.TransChunks, self.map)
                            elif temp["type"] == "Coin":
                                OBJ.Coin(column, row, layer, self.TransChunks, self.map)
                            elif temp["type"] == "Key":
                                Piano.White_Key(column, row, layer, self.map, self.player.clock, self.keysGroup, self.keysList)
                            elif temp["type"] == "door":
                                OBJ.Portal(column, row, layer, self.TransChunks, self.map, self.GAMEWORLD)
                            elif temp["type"] == "jboost":
                                OBJ.JumpBoost(column, row, layer, self.TransChunks, self.map)
                            else:
                                OBJ.Transparent(column, row, layer, self.TransChunks, self.map)
                else:
                    for column in range(self.map.width):
                        for row in range(self.map.height):
                            temp = self.map.get_tile_image(column, row, layer)
                            if temp == None:
                                continue
                            OBJ.Block(column, row, layer, self.chunks, self.map, self.allBlocks)
        self.end = False
        self.boss_level()
        self.MOVING = True
        
    def Spawn_Enemy(self, layer):
        for e in layer:
            if e.name == "Flute":
                f = ENEMY.Flute(int(e.x),int(e.y),self.player.clock,self.particles,self.player)
                self.ENEMIES.append(f)
            elif e.name == "Player":
                self.player.rect.x = int(e.x)
                self.player.rect.y = int(e.y)
                if e.x > 600:
                    if self.baseSize[0] - int(e.x) > 0:
                        self.s_x -= self.baseSize[0] - int(e.x)
            elif e.name == "Trumpet":
                t = ENEMY.Trumpet(int(e.x),int(e.y),self.player.clock,self.particles,self.player)
                self.ENEMIES.append(t)
            elif e.name == "warrior_spawn":
                self.BOSS_SPAWNPOINTS.append(e)
            elif e.name == "text":
                text = OBJ.TextBlock(int(e.x), int(e.y), e.text, self.display)
                self.ENEMIES.append(text)

    def reSize(self):
        #self.right_chunk = self.display.get_size()[0] // self.map.tilewidth // 10 + 1 + self.left_chunk
        size = self.display.get_size()
        self.background = pygame.transform.scale(self.IMG, size)
        self.b_x = int(-self.map.width * 0.3 * self.map.tilewidth)
        p_y = int(self.player.rect.y / self.baseSize[1] * size[1])
        self.player.rect.y = p_y
        self.s_y = size[1] - self.map.height * self.map.tileheight
        if self.s_x <= -size[0]:
            self.s_x = -size[0]
            self.renderChunk()
            self.b_x = -self.s_x
        for obj in self.allBlocks:
            obj.updatePos(obj.rect.x + self.s_x, obj.rect.y + self.s_y)
        self.baseSize = size

    def renderChunk(self):
        size = self.display.get_size()
        for c in self.chunks:
            for b in c[1]:
                x = self.s_x + b.column * 32
                y = self.s_y + b.row * 32
                b.updatePos(x, y)
            c[0].update()
            c[0].draw(self.display)
        for b in self.TransChunks:
            x = self.s_x + b.column * 32
            y = self.s_y + b.row * 32
            b.updatePos(x, y)
            b.checkinscreen(size)
            if type(b) == OBJ.JumpBoost:
                b.playerontop(self.player)
            b.update()
            if b.ONSCREEN:
                self.display.blit(b.image, b.rect)
        self.keysGroup.update()
        self.keysGroup.draw(self.display)
        for k in self.keysList:
            x = self.s_x + k.column * 32
            y = self.s_y + k.get_moved_y()
            k.updatePos(x, y)
    
    def draw_Background(self):
        self.display.blit(self.background, (self.b_x, self.b_y))

    def check_for_collision(self):
        for c in self.chunks:
            for b in c[1]:
                col = pygame.sprite.collide_rect(b, self.player)
                if col:
                    #FIX THE ISSUE
                    if self.player.onGround:
                        if b.rect.top < self.player.rect.bottom < b.rect.top + 3 and (b.rect.left + 10 < self.player.rect.centerx < b.rect.right - 10):
                            self.player.falling = False
                            self.player.rect.bottom = b.rect.top - 1
                        if b.rect.left < self.player.rect.right < b.rect.left + 8:
                            self.player.rect.right = b.rect.left
                            self.MOVING = False
                        elif b.rect.right > self.player.rect.left > b.rect.right - 8:
                            self.player.rect.left = b.rect.right
                            self.MOVING = False
                            
                        
                    #check if something is underneath, if nothing, fall, otherwise, check for collision horizontal
                    #chekc if miku hits head
                    elif not self.player.onGround:
                        if b.rect.top < self.player.rect.bottom < b.rect.top + 15:
                            self.player.onGround = True
                            self.player.falling = False
                            self.player.rect.bottom = b.rect.top - 1
                        elif b.rect.left < self.player.rect.right <= b.rect.left + 10:
                            self.player.rect.right = b.rect.left - 1
                            self.MOVING = False
                        elif b.rect.right - 10 < self.player.rect.left <= b.rect.right:
                            self.player.rect.left = b.rect.right + 1
                            self.MOVING = False
                        elif b.rect.bottom > self.player.rect.top > b.rect.bottom - 15:
                            self.player.rect.top = b.rect.bottom + 1
                            self.player.jumping = False
                            self.player.falling = True
                for e in self.ENEMIES:
                    if e.INCHUNK:
                        #continue script
                        e.HitBlock(b)
        #print(self.player.rect.top)
        col = pygame.sprite.groupcollide(self.player.group, self.keysGroup, False, False, collided = None)
        if col:
            k = col[self.player][0]
            if k.rect.top < self.player.rect.bottom < k.rect.top + 20 and k.rect.left < self.player.rect.centerx < k.rect.right:
                self.player.rect.bottom = k.rect.top - 1
                self.player.falling = False
                self.player.onGround = True
            else:
                self.player.rect.bottom = k.rect.top - 1
            if k.rect.left < self.player.rect.right < k.rect.left + 10:
                self.player.rect.right = k.rect.left - 1
                self.MOVING = False
            if k.rect.right > self.player.rect.left > k.rect.right - 10:
                self.player.rect.left = k.rect.right + 1
                self.MOVING = False

        col = self.player.checkifonGround(self.allBlocks)
        col2 = self.player.checkifonGround(self.keysGroup)
        if not col and self.player.onGround and not col2:
            self.player.onGround = False
        if self.level in [5,10]:
            self.BOSS.warrior_physics(self.allBlocks, self.keysGroup)
            self.BOSS.prevent_warrior_outside(self.MAPLEFT, self.MAPRIGHT)
        self.player.Damage(self.particles)

    def Move_Map(self):
        self.player.Restrict_Miku_Movement(self)
        size = self.display.get_size()
        for s in self.ENEMIES:
            s.InChunk(size)
            s.update()
            if self.player.HITEDGE and self.MOVING:
                if self.player.facing:
                    x = -self.player.speed * 2
                else:
                    x = self.player.speed * 2
                s.updatePos(x, s.rect.y)
            if s.INCHUNK:
                self.display.blit(s.image, s.rect)
        self.MOVING = True
    
    def Player_Death(self):
        if self.player.fallIntoVoid():
            self.player.kill()
            self.end = True
        if self.player.HP <= 0:
            self.player.kill()
            self.end = True

    def Coin_Collision(self,score):
        col = pygame.sprite.groupcollide(self.player.group, self.TransChunks, False, False, collided = None)
        if col:
            for c in col[self.player]:
                if type(c) == OBJ.Coin:
                    c.kill()
                    score.score += 1
                    self.AUDIO.set_volume(0,0.05)
                    self.AUDIO.play_effect("pickup_coin",0,0.05)
                elif type(c) == OBJ.Portal:
                    self.door_collisions(c)

    def door_collisions(self, door):
        door.checkifchange(self.player)

    def boss_level(self):
        if self.level in [5,10]:
            if self.level == 5:
                self.BOSS = Piano.PIANO(self.player.clock, self.display, self.keysList, self.BOSS_SPAWNPOINTS, self.ENEMIES)
    
    def boss_Update(self):
        if self.level in [5,10]:
            self.BOSS.update()

    def killall(self):
        for s in self.allBlocks:
            s.kill()
        for s in self.TransChunks:
            s.kill()
        for s in self.keysGroup:
            s.kill()
        for s in self.chunks:
            for x in s[0]:
                x.kill()
        self.player.kill()
        for e in self.ENEMIES:
            e.kill()
        for p in self.particles:
            p.kill()
        self.MUSIC.stop()

    def update(self):
        self.draw_Background()
        self.boss_Update()
        self.renderChunk()
        self.check_for_collision()
        self.Move_Map()
        
