import pygame
import pytmx
from os import path, getcwd
from . import MUSIC
from . import OBJECTS as OBJ

cwd = getcwd()

class SubLevel:
    def __init__(self, ID, player, particles, GAMEWORLD):
        self.player = player
        self.display = GAMEWORLD.display
        self.particles = particles.empty()
        self.GAMEWORLD = GAMEWORLD
        #load the world
        #and the map
        self.map = pytmx.load_pygame(path.join(cwd, f"game\\levels\\sublevel{ID}.tmx"))
        self.allBlocks = pygame.sprite.Group()
        self.baseSize = self.display.get_size()
        self.TransChunks = pygame.sprite.Group()
        self.ID = ID
        ########### load only specific chunks #####
        self.chunks = 0
        x = 0
        while x < self.map.width:
            CHUNK = (pygame.sprite.Group(),[])
            self.chunks.append(CHUNK)
            x += 10
        ####### audio and stuff ########
        self.AUDIO = MUSIC.Effect()
        self.AUDIO.set_volume(0,0.3)
        self.MUSIC = MUSIC.Music(self)
        self.MUSIC.set_up("1",0.05)
        self.MUSIC.play(-1)
        ####### display stuff ########
        self.left_chunk = 0
        self.right_chunk = display.get_size()[0] // self.map.tilewidth // 10 + 1
        ################background
        self.IMG = pygame.image.load(path.join(cwd, f"game\\textures\\backgrounds\\{ID}.JPG")).convert()
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