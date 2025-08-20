import pygame
import copy
import types

def conditional_render(obj):
    if isinstance(obj, types.FunctionType):
        return obj()
    return obj

class Button():
    def __init__(self, x, y, image, width, height, callback, childs):
        self.x = x
        self.y = y
        self.image = image
        self.width = width
        self.height = height
        self.clicked = False
        self.callback = callback
        self.childs = []
        if childs is not None:
            self.childs = childs

        self.world_rect = None
    
    def draw(self, surface_p, parent_pos):
        pos = pygame.mouse.get_pos()
        
        x_result = conditional_render(self.x)
        y_result = conditional_render(self.y)
        image_result = conditional_render(self.image)
        width_result = conditional_render(self.width)
        height_result = conditional_render(self.height)

        if width_result is not None and height_result is not None:
            image_scaled = pygame.transform.scale(image_result, (width_result, height_result))
        elif width_result is not None and height_result is None:
            height_result = image_result.get_rect().height
            image_scaled = pygame.transform.scale(image_result, (width_result, image_result.get_rect().height))
        elif width_result is None and height_result is not None:
            width_result = image_result.get_rect().width
            image_scaled = pygame.transform.scale(image_result, (image_result.get_rect().width, height_result))
        else:
            width_result = image_result.get_rect().width
            height_result = image_result.get_rect().height
            image_scaled = image_result

        rect = image_scaled.get_rect()
        rect.topleft = (x_result, y_result)
        
        self.world_rect = copy.deepcopy(rect)
        self.world_rect.topleft = (rect.topleft[0] + parent_pos[0], rect.topleft[1] + parent_pos[1])
        
        if self.world_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                if self.callback is not None:
                    self.callback()
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        
        surface_p.blit(image_scaled, (rect.x + parent_pos[0], rect.y + parent_pos[1]))

        for child in self.childs:
            child_result = conditional_render(child)
            child_result.draw(surface_p, (parent_pos[0] + rect.x, parent_pos[1] + rect.y))

class Panel():
    def __init__(self, x, y, image, width, height, childs):
        self.x = x
        self.y = y
        self.image = image
        self.width = width
        self.height = height
        if childs is not None:
            self.childs = childs
        else:
            self.childs = []

        self.world_rect = None
    
    def draw(self, surface_p, parent_pos):
        x_result = conditional_render(self.x)
        y_result = conditional_render(self.y)
        image_result = conditional_render(self.image)
        width_result = conditional_render(self.width)
        height_result = conditional_render(self.height)
        
        if width_result is not None and height_result is not None:
            image_scaled = pygame.transform.scale(image_result, (width_result, height_result))
        elif width_result is not None and height_result is None:
            height_result = image_result.get_rect().height
            image_scaled = pygame.transform.scale(image_result, (width_result, image_result.get_rect().height))
        elif width_result is None and height_result is not None:
            width_result = image_result.get_rect().width
            image_scaled = pygame.transform.scale(image_result, (image_result.get_rect().width, height_result))
        else:
            width_result = image_result.get_rect().width
            height_result = image_result.get_rect().height
            image_scaled = image_result

        rect = image_scaled.get_rect()
        rect.topleft = (x_result, y_result)

        self.world_rect = copy.deepcopy(rect)
        self.world_rect.topleft = (rect.topleft[0] + parent_pos[0], rect.topleft[1] + parent_pos[1])
        
        surface_p.blit(image_scaled, (rect.x + parent_pos[0], rect.y + parent_pos[1]))
        
        for child in self.childs:
            child_result = conditional_render(child)
            child_result.draw(surface_p, (parent_pos[0] + rect.x, parent_pos[1] + rect.y))

class Text():
    def __init__(self, x, y, text, font, color, width, height, childs):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.width = width
        self.height = height
        if childs is not None:
            self.childs = childs
        else:
            self.childs = []

        self.world_rect = None
    
    def draw(self, surface_p, parent_pos):
        x_result = conditional_render(self.x)
        y_result = conditional_render(self.y)
        text_result = conditional_render(self.text)
        color_result = conditional_render(self.color)
        width_result = conditional_render(self.width)
        height_result = conditional_render(self.height)

        surface = self.font.render(text_result, True, color_result)

        rect = surface.get_rect()
        rect.width = width_result
        rect.height = height_result
        rect.x = x_result
        rect.y = y_result
        rect.topleft = (x_result, y_result)
        
        surface_p.blit(surface, (rect.x + parent_pos[0], rect.y + parent_pos[1]))

        self.world_rect = copy.deepcopy(rect)
        self.world_rect.topleft = (rect.topleft[0] + parent_pos[0], rect.topleft[1] + parent_pos[1])

        for child in self.childs:
            child_result = conditional_render(child)
            child_result.draw(surface_p, (parent_pos[0] + rect.x, parent_pos[1] + rect.y))