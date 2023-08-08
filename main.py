import pygame
from config import *
from scene import SceneManager

# 초기화
pygame.init()
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
pygame.display.set_caption(TITLE)
icon = pygame.image.load("Cubic.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

scene_manager = SceneManager(window, clock)
scene_manager.load_scene(0)
scene_manager.run()