from tiles import *
from spritesheet import Spritesheet
from player import Player
from ui import Button

pygame.init()
DISPLAY_W, DISPLAY_H = 1200, 700
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 60

spritesheet = Spritesheet('spritesheet.png')
player = Player()

map = TileMap('test_level.csv', spritesheet, player)
player.position.x, player.position.y = map.start_x, map.start_y

result = map.set_tile(1, 1, '1')

print({'result':result})

ui_elements = []

ui_elements.append(Button(window, 100, 200, spritesheet.parse_sprite('grass.png'), 80, 80, lambda: print("hi")))

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
    canvas.fill((0, 180, 240))
    map.draw_map(canvas)
    player.draw(canvas)
    window.blit(canvas, (0,0))
    for ui_element in ui_elements:
        ui_element.draw()
    pygame.display.update()