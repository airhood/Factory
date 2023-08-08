import pygame, csv, os
from config import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, id, x, y, rotation, block_spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(block_spritesheet.parse_sprite(id - 1), (TILE_SIZE, TILE_SIZE))
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.image, 360 - self.rotation)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.id = id

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, block_spritesheet, player):
        self.tile_size = TILE_SIZE
        self.block_spritesheet = block_spritesheet
        self.player = player
        self.tiles = [[None for j in range(TILEMAP_SIZE)] for i in range(TILEMAP_SIZE)]
        self.map_surface = pygame.Surface((TILEMAP_SIZE * TILE_SIZE, TILEMAP_SIZE * TILE_SIZE))
        self.map_surface.set_colorkey((0, 0, 0))
        self.isLoading = True
        self.load_map()
        self.isLoading = False

    def draw(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        self.map_surface = pygame.Surface((TILEMAP_SIZE * TILE_SIZE, TILEMAP_SIZE * TILE_SIZE))
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
        if (x > TILEMAP_SIZE): return None
        elif (y > TILEMAP_SIZE): return None

        if id == '0':
            self.tiles[x][y] = None
        elif id == '1-0':
            self.tiles[x][y] = (Tile(1, x * self.tile_size, y * self.tile_size, 0, self.block_spritesheet))
        elif id == '1-1':
            self.tiles[x][y] = (Tile(1, x * self.tile_size, y * self.tile_size, 90, self.block_spritesheet))
        elif id == '1-2':
            self.tiles[x][y] = (Tile(1, x * self.tile_size, y * self.tile_size, 180, self.block_spritesheet))
        elif id == '1-3':
            self.tiles[x][y] = (Tile(1, x * self.tile_size, y * self.tile_size, 270, self.block_spritesheet))
        else:
            self.tiles[x][y] = (Tile(int(id), x * self.tile_size, y * self.tile_size, 0, self.block_spritesheet))
        
        if not self.isLoading:
            self.load_map()
        
        return True

    def load_tiles(self, filename):
        print("loading tiles")
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