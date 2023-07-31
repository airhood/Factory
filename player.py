import pygame
from spritesheet import Spritesheet
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY, self.DOWN_KEY, self.FACING_LEFT = False, False, False, False, False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .35, -.12
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.camera_position = pygame.math.Vector2(0, 0)

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt):
        self.horizontal_movement(dt)
        self.vertical_movement(dt)

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x += PLAYER_SPEED
        elif self.RIGHT_KEY:
            self.acceleration.x -= PLAYER_SPEED
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.camera_position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        #self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.acceleration.y = 0
        if self.UP_KEY:
            self.acceleration.y += PLAYER_SPEED
        elif self.DOWN_KEY:
            self.acceleration.y -= PLAYER_SPEED
        self.acceleration.y += self.velocity.y * self.friction
        self.velocity.y += self.acceleration.y * dt
        self.limit_velocity(4)
        self.camera_position.y += self.velocity.y * dt + (self.acceleration.x * .5) * (dt * dt)
        #self.rect.y = self.position.y

    def limit_velocity(self, max_vel):
        min(-max_vel, max(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 8
            self.on_ground = False




















