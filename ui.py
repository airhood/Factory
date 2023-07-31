import pygame
import copy

class Button():
    def __init__(self, x, y, image, width, height, callback):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.callback = callback
    
    def draw(self, surface, parent_pos):
        pos = pygame.mouse.get_pos()
        world_rect = copy.deepcopy(self.rect)
        world_rect.topleft = (self.rect.topleft[0] + parent_pos[0], self.rect.topleft[1] + parent_pos[1])
        if world_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.callback()
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        
        surface.blit(self.image, (self.rect.x + parent_pos[0], self.rect.y + parent_pos[1]))

class Panel():
    def __init__(self, x, y, image, width, height, childs):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        if childs is not None:
            self.childs = childs
        else:
            self.childs = []
    
    def draw(self, surface, parent_pos):
        surface.blit(self.image, (self.rect.x + parent_pos[0], self.rect.y + parent_pos[1]))
        
        for child in self.childs:
            child.draw(surface, (parent_pos[0] + self.rect.x, parent_pos[1] + self.rect.y))