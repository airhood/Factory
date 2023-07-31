import pygame

class Button():
    def __init__(self, screen, x, y, image, width, height, callback):
        self.screen = screen
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.callback = callback
    
    def draw(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.callback()
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        
        self.screen.blit(self.image, (self.rect.x, self.rect.y))