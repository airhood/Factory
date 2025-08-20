import pygame
from config import *
import math

class ItemEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, number, tilemap, block_spritesheet, number_icon, font):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.number = number
        self.block_spritesheet = block_spritesheet
        self.number_icon = number_icon
        self.image = number_icon
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * TILE_SIZE + 8, y * TILE_SIZE + 8
        self.tilemap = tilemap
        self.initial_grid_pos = (x, y)
        self.current_grid_pos = (x, y)
        self.target_grid_pos = None
        self.calculate_target_pos() # 초기 이동 목표 좌표 설정
        self.font = font
        self.remove_this = False
        self.stop_move = False
    
    def calculate_target_pos(self): # 다음 아이템 이동 목표 좌표 계산
        if self.tilemap.tiles[self.current_grid_pos[0]][self.current_grid_pos[1]] is None:
            self.target_grid_pos = self.current_grid_pos
            self.moving_dir = -1
            return
        rotation = self.tilemap.tiles[self.current_grid_pos[0]][self.current_grid_pos[1]].rotation
        x, y = self.current_grid_pos[0], self.current_grid_pos[1]
        if self.target_grid_pos is not None:
            if (self.rect.x + 16) != (self.target_grid_pos[0] * TILE_SIZE + 24) or (self.rect.y + 16) != (self.target_grid_pos[1] * TILE_SIZE + 24):
                return
        if self.tilemap.tiles[self.current_grid_pos[0]][self.current_grid_pos[1]].id == 5:
            chip_tile = self.tilemap.tiles[self.current_grid_pos[0]][self.current_grid_pos[1]]
            rotation_chip = chip_tile.rotation + self.moving_dir * 90

            if rotation_chip == 0:
                chip_tile.chip.add_input('C', self.number)
                self.remove_this = True
            elif rotation_chip == 90:
                chip_tile.chip.add_input('B', self.number)
                self.remove_this = True
            elif rotation_chip == 180:
                chip_tile.chip.add_input('A', self.number)
                self.remove_this = True
            elif rotation_chip == 270:
                chip_tile.chip.add_input('D', self.number)
                self.remove_this = True
                
            # if chip_tile.rotation == 0:
            #     if chip_tile.chip.portC_saved is None:
            #         chip_tile.chip.portC_saved = self.number
            #         self.remove_this = True
            #     else:
            #         self.stop_move = True
            #         return
            # elif chip_tile.rotation == 90:
            #     if chip_tile.chip.portB_saved is None:
            #         chip_tile.chip.portB_saved = self.number
            #         self.remove_this = True
            #     else:
            #         self.stop_move = True
            #         return
            # elif chip_tile.rotation == 180:
            #     if chip_tile.chip.portA_saved is None:
            #         chip_tile.chip.portA_saved = self.number
            #         self.remove_this = True
            #     else:
            #         self.stop_move = True
            #         return
            # elif chip_tile.rotation == 270:
            #     if chip_tile.chip.portD_saved is None:
            #         chip_tile.chip.portD_saved = self.number
            #         self.remove_this = True
            #     else:
            #         self.stop_move = True
            #         return
                                    
        next_target_pos = None
        if rotation == 0: # up
            self.moving_dir = 0
            next_target_pos = (x, y - 1)
        elif rotation == 90: # right
            self.moving_dir = 1
            next_target_pos = (x + 1, y)
        elif rotation == 180: # down
            self.moving_dir = 2
            next_target_pos = (x, y + 1)
        elif rotation == 270: # left
            self.moving_dir = 3
            next_target_pos = (x -1, y)
        next_target_pos_tile = self.tilemap.tiles[next_target_pos[0]][next_target_pos[1]]
        if next_target_pos_tile is not None:
            if next_target_pos_tile.id == 1 or next_target_pos_tile.id == 5:
                self.target_grid_pos = next_target_pos
            elif self.block_spritesheet.parse_sprite(next_target_pos_tile.id - 1):
                pass
            else:
                self.moving_dir = -1
                self.target_grid_pos = self.current_grid_pos
        else:
            self.moving_dir = -1
            self.target_grid_pos = self.current_grid_pos
    
    def move(self):
        if self.stop_move:
            return
        
        if self.moving_dir == -1:
            pass
        if self.moving_dir == 0: # up
            self.rect.x, self.rect.y = self.rect.x, self.rect.y - CONVEYOR_SPEED
        elif self.moving_dir == 1: # right
            self.rect.x, self.rect.y = self.rect.x + CONVEYOR_SPEED, self.rect.y
        elif self.moving_dir == 2: # down
            self.rect.x, self.rect.y = self.rect.x, self.rect.y + CONVEYOR_SPEED
        elif self.moving_dir == 3: # left
            self.rect.x, self.rect.y = self.rect.x - CONVEYOR_SPEED, self.rect.y
    
    def update_grid_pos(self):
        self.current_grid_pos = (math.floor((self.rect.x + 12) / TILE_SIZE), math.floor((self.rect.y + 12) / TILE_SIZE))

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        text = self.font.render(str(self.number), True, (255, 255, 255))
        surface.blit(text, (self.rect.x - text.get_rect().width/2 + 12 + 4, self.rect.y - text.get_rect().height/2 + 12 + 4))
    
    def tick(self):
        self.update_grid_pos()
        self.calculate_target_pos()
        self.move()

    def reset(self):
        self.target_grid_pos = None
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.initial_grid_pos[0] * TILE_SIZE + 8, self.initial_grid_pos[1] * TILE_SIZE + 8
        self.update_grid_pos()
        self.calculate_target_pos()