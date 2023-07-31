import pygame, csv, os
from config import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spritesheet.parse_sprite(image), (32, 32))
        self.x = x
        self.y = y
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet, player):
        self.tile_size = TILE_SIZE
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.player = player
        self.map_w, self.map_h = None, None
        self.tiles = [[None for j in range(100)] for i in range(100)]
        self.set_map_size(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_tiles(filename)
        #self.load_map()

    def draw(self, surface, parent_pos):
        surface.blit(self.map_surface, (parent_pos[0], parent_pos[1]))

    def load_map(self):
        for row in self.tiles:
            for tile in row:
                if (tile is not None):
                    tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map
    
    def set_tile(self, x, y, id):
        if (self.map_w is not None):
            if (x > self.map_w): return None
            elif (y > self.map_h): return None
        print({'x': x, 'y': y})

        if id == '-1':
            self.tiles[x][y] = None
        if id == '0':
            self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
        elif id == '1':
            self.tiles[x][y] = (Tile('grass.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
        elif id == '2':
            self.tiles[x][y] = (Tile('grass2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))

        if (self.tiles[x][y] is not None):
            self.tiles[x][y].draw(self.map_surface)
        return True

    def load_tiles(self, filename):
        map = self.read_csv(filename)
        x, y = 0, 0
        # x: column, y: row
        for row in map:
            x = 0
            for tile in row:
                self.set_tile(x, y, tile)
                x += 1
            y += 1

    def set_map_size(self, filename):
        map = self.read_csv(filename)
        x, y = 0, 0
        # x: column, y: row
        for row in map:
            x = 0
            for tile in row:
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size










