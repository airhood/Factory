import pygame

class LevelManager():
    def __init__(self, gamescene):
        self.gamescene = gamescene

    def load_level(self, level_id):
        self.gamescene.player.camera_position = pygame.math.Vector2(0, 0)
        self.gamescene.tilemap.load_map(f"{str(level_id)}.csv")
        self.gamescene.items = []