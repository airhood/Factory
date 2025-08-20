import pygame

class LevelManager():
    def __init__(self, gamescene):
        self.gamescene = gamescene

    def load_level(self, map_file):
        self.gamescene.player.camera_position = pygame.math.Vector2(0, 0)
        self.gamescene.tilemap.load_map(f"{str(map_file)}.csv")
        self.gamescene.items = []