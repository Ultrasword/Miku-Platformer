import pygame
from modules import SCREEN
from modules import CHARACTER
from modules import PLATFORM
from modules import Score
pygame.init()

class Game:
    def __init__(self):
        self.run = False
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((1080, 720), pygame.DOUBLEBUF|pygame.HWSURFACE)
        self.sprGroups = []
        self.PLAYERS = self.make_new_sprGroup()
        self.ENEMIES = self.make_new_sprGroup()
        self.BOSS = self.make_new_sprGroup()
        self.RAYGRP = self.make_new_sprGroup()
        self.PARTICLES = self.make_new_sprGroup()
        self.OBJECTS = self.make_new_soloGroup()
        self.SUG = []
        self.level = 3
        self.pastlevel = self.level
        self.changelevel = False
        self.playerdeath = False
        
    def change_display_size(self):
        self.display = pygame.display.set_mode(self.display.get_size(), )

    def startMenu(self):
        start = SCREEN.Start_Screen(self.display)
        start.show_start()
        if start.exit:
            self.exitGame()
            start.exit = False
            return
        self.run = True

    def exitGame(self):
        self.run = False
        self.game = False
    
    def make_new_sprGroup(self):
        grp = pygame.sprite.Group()
        self.sprGroups.append(grp)
        return grp
    
    def make_new_soloGroup(self):
        grp = pygame.sprite.GroupSingle()
        self.sprGroups.append(grp)
        return grp
    
    def load_level(self, level):
        self.PLAYER = CHARACTER.MIKU(self.display, 1, self.PLAYERS, self.SUG, self.clock)
        self.GAME = PLATFORM.Platform(self.display, self.PLAYER, level, self.PARTICLES, self)
        self.COUNTER = Score.Counter(self.display)
        self.OBJECTS.add(self.COUNTER)

    def changeLevel(self):
        if self.level != self.pastlevel:
            self.run = False
            self.changelevel = True
            self.pastlevel = self.level

    def check_if_gameover(self):
        self.GAME.Player_Death()
        if self.GAME.end:
            self.run = False
            self.playerdeath = True

    def runGame(self, level):
        self.load_level(level)
        while self.run:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.exitGame()
                elif e.type == pygame.VIDEORESIZE:
                    #videoresize groups iter through to resize
                    for spr in self.SUG:
                        spr.reSize()
                    self.GAME.reSize()
            
            #end game continue game idk
            self.check_if_gameover()
            #change this
            #in future
            self.GAME.update()
            self.GAME.Coin_Collision(self.COUNTER)
            for grp in self.sprGroups:
                grp.update()
                grp.draw(self.display)
            pygame.display.flip()
            self.clock.tick(30)
            self.changeLevel()

        if self.changelevel:
            self.GAME.killall()
            self.game = True
            self.run = True
            self.changelevel = False
        elif self.playerdeath:
            pass
        else:
            self.game = False
    
    def update(self):
        self.game = True
        while self.game:
            if not self.run:
                self.startMenu()
            self.runGame(self.level)



if __name__ == "__main__":
    g = Game()
    g.update()

pygame.quit()
