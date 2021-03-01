import pygame
from os import path, getcwd
from random import randint, choice
import json

cwd = getcwd()

class Piano_Battle:
    def __init__(self, clock, display, boss: str):
        self.clock = clock
        self.display = display
        
        
        