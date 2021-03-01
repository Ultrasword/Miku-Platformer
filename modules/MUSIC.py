from pygame import mixer
from os import getcwd, path

cwd = getcwd()

class Effect:
    def __init__(self, c: int=0):
        self.effects = {}
        self.layers = []
        self.channel = c
        self.add_layer(self.channel)
        self.timer = 10

    def update_time(self):
        self.timer += 1

    def play_effect(self,sound,c,vol:int=1):
        if str(sound) not in self.effects:
            self.load_soundeffect(sound)
        self.set_volume(c,vol)
        self.layers[c].play(self.effects[str(sound)])

    def load_soundeffect(self,sound):
        s = mixer.Sound(path.join(cwd, f"game\\audio\\effects\\{sound}.wav"))
        self.effects[str(sound)] = s

    def add_layer(self, c):
        l = mixer.Channel(c)
        self.layers.append(l)
    
    def timer_effect(self,sound,c,time,vol):
        self.update_time()
        if self.timer > time:
            self.timer = 0
            self.play_effect(sound,c,vol)
    
    def set_volume(self, c, vol):
        self.layers[c].set_volume(vol)

class Music:
    def __init__(self, platform):
        self.platform = platform
        self.mixer = mixer

    def load_music(self,level):
        self.mixer.music.load(path.join(cwd, f"game\\audio\\music\\{level}.mp3"))
    
    def set_volume(self,vol):
        self.mixer.music.set_volume(vol)
    
    def play(self,pt):
        self.mixer.music.play(pt)
    
    def set_up(self, level, vol):
        self.load_music(level)
        self.set_volume(vol)