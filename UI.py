import pygame
import copy

class Button():
    def __init__(self, x, y, image, width, height, callback, childs):
        if width is not None and height is not None:
            self.image = pygame.transform.scale(image, (width, height))
        elif width is not None and height is None:
            self.image = pygame.transform.scale(image, (width, image.get_rect().height))
        elif width is None and height is not None:
            self.image = pygame.transform.scale(image, (image.get_rect().width, height))
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.world_rect = None
        self.clicked = False
        self.callback = callback
        if childs is not None:
            self.childs = childs
        else:
            self.childs = []
    
    def draw(self, surface, parent_pos):
        pos = pygame.mouse.get_pos()
        self.world_rect = copy.deepcopy(self.rect)
        self.world_rect.topleft = (self.rect.topleft[0] + parent_pos[0], self.rect.topleft[1] + parent_pos[1])
        if self.world_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                if self.callback is not None:
                    self.callback()
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        
        surface.blit(self.image, (self.rect.x + parent_pos[0], self.rect.y + parent_pos[1]))

        for child in self.childs:
            child.draw(surface, (parent_pos[0] + self.rect.x, parent_pos[1] + self.rect.y))

class Panel():
    def __init__(self, x, y, image, width, height, childs):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.world_rect = None
        if childs is not None:
            self.childs = childs
        else:
            self.childs = []
    
    def draw(self, surface, parent_pos):
        self.world_rect = copy.deepcopy(self.rect)
        self.world_rect.topleft = (self.rect.topleft[0] + parent_pos[0], self.rect.topleft[1] + parent_pos[1])
        surface.blit(self.image, (self.rect.x + parent_pos[0], self.rect.y + parent_pos[1]))
        
        for child in self.childs:
            child.draw(surface, (parent_pos[0] + self.rect.x, parent_pos[1] + self.rect.y))

class Text():
    def __init__(self, x, y, text, font, color, width, height, childs):
        self.surface = font.render(text, True, color)
        self.rect = self.surface.get_rect()
        self.rect.width = width
        self.rect.height = height
        self.rect.x = x
        self.rect.y = y
        self.rect.topleft = (x, y)
        self.world_rect = None
        if childs is not None:
            self.childs = childs
        else:
            self.childs = []
    
    def draw(self, surface, parent_pos):
        self.world_rect = copy.deepcopy(self.rect)
        self.world_rect.topleft = (self.rect.topleft[0] + parent_pos[0], self.rect.topleft[1] + parent_pos[1])
        surface.blit(self.surface, (self.rect.x + parent_pos[0], self.rect.y + parent_pos[1]))

        for child in self.childs:
            child.draw(surface, (parent_pos[0] + self.rect.x, parent_pos[1] + self.rect))