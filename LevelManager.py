import pygame
import json

class LevelManager():
    def __init__(self, gamescene):
        self.gamescene = gamescene
        self.levels_data = None

    def load_levels(self):
        with open('levels.json', 'r', encoding='utf-8') as f:
            self.levels_data = json.load(f)
        f.close()

    def load_level(self, theme, level):
        self.gamescene.player.camera_position = pygame.math.Vector2(0, 0)
        self.gamescene.tilemap.load_map(self.levels_data[theme]['levels'][level]['map_file'])
        self.gamescene.items = []