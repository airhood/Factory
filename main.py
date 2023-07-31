from tiles import *
from spritesheet import Spritesheet
from player import Player
from ui import Button
from ui import Panel
import math

pygame.init()
DISPLAY_W, DISPLAY_H = 1200, 700
background = pygame.Surface((10000, 10000))
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
canvas.set_colorkey((0, 0, 0))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 60

spritesheet = Spritesheet('spritesheet.png')
player = Player()

world = pygame.Surface((10000, 10000))
world.set_colorkey((0, 0, 0))

ui_elements = []

ui_elements.append(Button(100, 200, spritesheet.parse_sprite('grass.png'), 80, 80, lambda: print("hi")))
ui_elements.append(Panel(400, 100, spritesheet.parse_sprite('grass2.png'), 300, 400, [Button(50, 50, spritesheet.parse_sprite('chick.png'), 100, 100, lambda: print("wee"))]))

gameObjects = []

gameObjects.append(TileMap('test_level.csv', spritesheet, player))
player.position.x, player.position.y = gameObjects[0].start_x, gameObjects[0].start_y

gameObjects[0].set_tile(1, 1, '1')

while running:
    dt = clock.tick(60) * .001 * TARGET_FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.LEFT_KEY = True
            elif event.key == pygame.K_d:
                player.RIGHT_KEY = True
            elif event.key == pygame.K_w:
                player.UP_KEY = True
            elif event.key == pygame.K_s:
                player.DOWN_KEY = True
            elif event.key == pygame.K_SPACE:
                player.jump()


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.LEFT_KEY = False
            elif event.key == pygame.K_d:
                player.RIGHT_KEY = False
            elif event.key == pygame.K_w:
                player.UP_KEY = False
            elif event.key == pygame.K_s:
                player.DOWN_KEY = False
            elif event.key == pygame.K_SPACE:
                if player.is_jumping:
                    player.velocity.y *= .25
                    player.is_jumping = False


    player.update(dt)
    background.fill((0, 180, 240))
    window.blit(background, (-5000, -5000))
    for gameObject in gameObjects:
        gameObject.draw(world, (0, 0))
    player.draw(canvas)
    window.blit(canvas, (0,0))
    if pygame.mouse.get_pressed()[0] == 1:
        pos = pygame.mouse.get_pos()
        calculated_pos = (pos[0] - player.camera_position.x, pos[1] - player.camera_position.y)
        tilemap_pos = (math.floor(calculated_pos[0] / TILE_SIZE), math.floor(calculated_pos[1] / TILE_SIZE))
        #print(tilemap_pos)
    window.blit(world, (0 + player.camera_position.x, 0 + player.camera_position.y))
    for ui_element in ui_elements:
        ui_element.draw(window, (0, 0))
    pygame.display.update()