import pygame

class Button():
    def __init__(self, screen, x, y, image, width, height):
        self.screen = screen
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))