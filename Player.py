import pygame
from Spritesheet import Spritesheet
from config import *
import math
from Tiles import Tile

class Player():
    def __init__(self, scene, block_spritesheet, block_select_bar):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY, self.DOWN_KEY, self.FACING_LEFT = False, False, False, False, False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .35, -.12
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.camera_position = pygame.math.Vector2(0, 0)
        self.block_set_rotation = 0
        self.holding_block = None # 플레이어가 선택한 블럭 id
        self.tilemap = None
        self.block_set_image = None # 설치 전, 블럭 설치 미리보기 이미지
        self.scene = scene
        self.block_spritesheet = block_spritesheet
        self.block_select_bar = block_select_bar

    def update(self, dt, surface): # 1프레임마다 실행
        self.check_input(surface)
        self.horizontal_movement(dt)
        self.vertical_movement(dt)

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x += PLAYER_SPEED
        if self.RIGHT_KEY:
            self.acceleration.x -= PLAYER_SPEED
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.camera_position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)

    def vertical_movement(self, dt):
        self.acceleration.y = 0
        if self.UP_KEY:
            self.acceleration.y += PLAYER_SPEED
        if self.DOWN_KEY:
            self.acceleration.y -= PLAYER_SPEED
        self.acceleration.y += self.velocity.y * self.friction
        self.velocity.y += self.acceleration.y * dt
        self.limit_velocity(4)
        self.camera_position.y += self.velocity.y * dt + (self.acceleration.x * .5) * (dt * dt)

    def limit_velocity(self, max_vel):
        min(-max_vel, max(self.velocity.x, max_vel))
        if abs(self.velocity.x) < 0.01: self.velocity.x = 0
    
    def check_input(self, surface):
        pos = pygame.mouse.get_pos()
        calculated_pos = (pos[0] - self.camera_position.x, pos[1] - self.camera_position.y)
        tilemap_pos = (math.floor(calculated_pos[0] / TILE_SIZE), math.floor(calculated_pos[1] / TILE_SIZE))
        if self.block_set_image is not None:
            self.draw_block_set_image(surface, tilemap_pos)
        if pygame.mouse.get_pressed()[0] == 1 and self.holding_block != None and not self.scene.conveyor_run:
            if self.block_select_bar.world_rect.collidepoint(pos) == False:
                if self.tilemap.tiles[tilemap_pos[0]][tilemap_pos[1]] is None and self.holding_block != 0:
                    if self.block_spritesheet.get_rotated(int(self.holding_block) - 1):
                        block_id = str(self.holding_block) + "-" + str(self.block_set_rotation)
                    else:
                        block_id = str(self.holding_block)
                    self.tilemap.set_tile(tilemap_pos[0], tilemap_pos[1], block_id)
                elif self.holding_block == 0: # delete block
                    self.tilemap.set_tile(tilemap_pos[0], tilemap_pos[1], "0")
    
    def draw_block_set_image(self, surface, tilemap_pos): # 블럭 설치 미리보기 이미지 draw
        surface.blit(self.block_set_image, ((tilemap_pos[0] * TILE_SIZE) + self.camera_position.x, (tilemap_pos[1] * TILE_SIZE) + self.camera_position.y))