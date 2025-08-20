import pygame, csv, os
from config import *
from Chip import Chip
import copy

class Tile(pygame.sprite.Sprite):
    def __init__(self, id, x, y, rotation, block_spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.chip = None
        self.image = pygame.transform.scale(block_spritesheet.parse_sprite(self.id - 1), (TILE_SIZE, TILE_SIZE))
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.image, 360 - self.rotation)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, block_spritesheet, player, chip_list, chip_instances):
        self.tile_size = TILE_SIZE
        self.block_spritesheet = block_spritesheet
        self.player = player
        self.tiles = [[None for j in range(TILEMAP_SIZE)] for i in range(TILEMAP_SIZE)]
        self.map_surface = pygame.Surface((TILEMAP_SIZE * TILE_SIZE, TILEMAP_SIZE * TILE_SIZE))
        self.map_surface.set_colorkey((0, 0, 0))
        self.isLoading = False
        self.chip_list = chip_list
        self.chip_instances = chip_instances

    def draw(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def render_map(self):
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
    
    def set_tile(self, x, y, id, chip=None, isChip=False):
        if (x > TILEMAP_SIZE): return True
        elif (y > TILEMAP_SIZE): return True

        if isChip:
            if id.find('-') != -1:
                split = id.split('-')
                self.tiles[x][y] = (Tile(5, x * self.tile_size, y * self.tile_size, int(split[1]) * 90, self.block_spritesheet))
                self.tiles[x][y].chip = chip # chip
            else:
                self.tiles[x][y] = (Tile(5, x * self.tile_size, y * self.tile_size, 0, self.block_spritesheet))
                self.tiles[x][y].chip = chip # chip

            if not self.isLoading:
                self.render_map()

            return True

        if id == '0':
            self.tiles[x][y] = None
        elif id.find('-') != -1:
            split = id.split('-')
            self.tiles[x][y] = (Tile(int(split[0]), x * self.tile_size, y * self.tile_size, int(split[1]) * 90, self.block_spritesheet))
        else:
            self.tiles[x][y] = (Tile(int(id), x * self.tile_size, y * self.tile_size, 0, self.block_spritesheet))
        
        if not self.isLoading:
            self.render_map()
        
        return True
    
    def set_chip(self, x, y, chip_id, rotation):
        if chip_id < len(self.chip_list):
            chip = copy.deepcopy(self.chip_list[chip_id])
            chip.x = x
            chip.y = y
            chip.activate = True
            self.chip_instances.append(chip)
            result = self.set_tile(x, y, '5-'+str(rotation), chip=chip, isChip=True)
            return result
        return False

    def load_map(self, filename):
        self.isLoading = True
        map = self.read_csv(filename)
        x, y = 0, 0
        # x: column, y: row
        for row in map:
            x = 0
            for tile in row:
                self.set_tile(x, y, tile)
                x += 1
            y += 1
        self.render_map()
        self.isLoading = False

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