import pygame
from tiles import *
from spritesheet import Spritesheet
from player import Player
from ui import Button
from ui import Panel
from conveyor import ItemEntity
from config import *

class SceneManager():
    def __init__(self, window, clock):
        self.running = True
        self.window = window
        self.clock = clock
        self.current_scene = None
        self.scenes = [TitleScene(window, self.load_scene), GameScene(window, self.load_scene)]

    def load_scene(self, scene_id):
        self.current_scene = scene_id
    
    def run(self):
        while self.running:
            # delta tile 계산
            dt = self.clock.tick(60) * .001 * TARGET_FPS
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            self.scenes[self.current_scene].run(dt, events)
            pygame.display.update()

class TitleScene():
    def __init__(self, window, load_scene):
        self.window = window
        self.load_scene = load_scene

        # font
        self.I_AM_A_PLAYER_Title = pygame.font.Font("Fonts/I AM A PLAYER.ttf", 100)
        self.title_text = self.I_AM_A_PLAYER_Title.render(TITLE, True, (88, 114, 227))
        self.TitleScreen_background = pygame.image.load('TitleScreen_background.png')

        # 이미지 로드
        self.game_start_button_image = pygame.image.load('button_start.png').convert_alpha()
        
        # UI
        self.game_start_button = Button(870, 535, self.game_start_button_image, self.game_start_button_image.get_rect().width * 0.15, self.game_start_button_image.get_rect().height * 0.15, lambda:load_scene(1))
    
    def run(self, dt, events):
        self.window.blit(get_colored_surf([DISPLAY_W, DISPLAY_H], (208, 252, 92)), (0, 0))
        self.window.blit(self.TitleScreen_background, [0, 0])
        self.game_start_button.draw(self.window, (0, 0))
        self.window.blit(self.title_text, [90, 100])

class GameScene():
    def __init__(self, window, load_scene):
        self.window = window
        self.load_scene = load_scene

        self.background = pygame.Surface((10000, 10000))
        self.canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
        self.canvas.set_colorkey((0, 0, 0))

        # 배경
        self.grid = pygame.image.load("Background Grid.png").convert_alpha()
        self.grid = pygame.transform.scale(self.grid, (2400 * 1.5, 1376 * 1.5))

        # fonts
        self.KCC_Ganpan_Number = pygame.font.Font("Fonts/KCC-Ganpan.ttf", 15)

        # 이미지 로드
        self.number_icon = pygame.image.load('number_icon.png').convert_alpha()
        self.number_icon.set_colorkey((0, 0, 0))
        self.block_spritesheet = Spritesheet('block_spritesheet')
        self.block_delete_ui = pygame.image.load('block_delete_ui.png')

        # 월드
        self.world = pygame.Surface((10000, 10000))
        self.world.set_colorkey((0, 0, 0))
        
        # UI
        self.ui_elements = []

        self.ui_elements.append(Panel(0, 630, get_colored_surf([1, 1], (130, 130, 130)), 1200, 70, [Button(15, 15, self.block_spritesheet.parse_sprite(1-1), 40, 40, lambda: self.set_player_holding_block(1))]))

        # Player
        self.player = Player(self.block_spritesheet, self.ui_elements[0])

        # Tilemap 생성
        self.tilemap = TileMap(self.block_spritesheet, self.player)
        self.tilemap.set_tile(1, 2, "1-1")

        self.player.tilemap = self.tilemap


        self.items = []
        self.items.append(ItemEntity(1, 2, 1, self.tilemap, self.block_spritesheet, self.number_icon, self.KCC_Ganpan_Number))

        self.t = 0
    
    def tick(self): # 게임 시스템 Tick
        for item in self.items:
            item.tick()
    
    def set_player_holding_block(self, id): # 플레이어가 선택한 블럭 id 저장
        self.player.holding_block = id
        # 블럭 설치 미리보기 이미지 업데이트
        self.player.block_set_image = pygame.transform.scale(self.block_spritesheet.parse_sprite(id - 1), (TILE_SIZE, TILE_SIZE))
        self.player.block_set_image.set_alpha(100)
    
    def run(self, dt, events):
        # key input
        for event in events:
            print("dd")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.LEFT_KEY = True
                elif event.key == pygame.K_d:
                    self.player.RIGHT_KEY = True
                elif event.key == pygame.K_w:
                    self.player.UP_KEY = True
                elif event.key == pygame.K_s:
                    self.player.DOWN_KEY = True
                elif event.key == pygame.K_r:
                    if self.player.holding_block is not None:
                        if self.block_spritesheet.get_rotated(self.player.holding_block - 1) and self.player.holding_block != 0:
                            self.player.block_set_rotation = self.player.block_set_rotation + 1
                            if self.player.block_set_rotation > 3:
                                self.player.block_set_rotation = self.player.block_set_rotation - 4
                            self.player.block_set_image = pygame.transform.rotate(pygame.transform.scale(self.block_spritesheet.parse_sprite(self.player.holding_block - 1), (TILE_SIZE, TILE_SIZE)), 360 - self.player.block_set_rotation * 90)
                            self.player.block_set_image.set_alpha(100)
                elif event.key == pygame.K_x:
                    self.player.block_set_rotation = 0
                    self.player.holding_block = 0
                    self.player.block_set_image = pygame.transform.scale(self.block_delete_ui, (TILE_SIZE, TILE_SIZE))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.LEFT_KEY = False
                elif event.key == pygame.K_d:
                    self.player.RIGHT_KEY = False
                elif event.key == pygame.K_w:
                    self.player.UP_KEY = False
                elif event.key == pygame.K_s:
                    self.player.DOWN_KEY = False
    
        # draw
        self.background.fill((226, 226, 226))
        self.window.blit(self.background, (-5000, -5000))
        self.window.blit(self.grid, (self.player.camera_position.x, self.player.camera_position.y))
        self.window.blit(self.grid, (self.player.camera_position.x, -self.grid.get_size()[1] + self.player.camera_position.y))
        self.window.blit(self.grid, (-self.grid.get_size()[0] + self.player.camera_position.x, -self.grid.get_size()[1] + self.player.camera_position.y))
        self.window.blit(self.grid, (-self.grid.get_size()[0] + self.player.camera_position.x, self.player.camera_position.y))
        self.tilemap.draw(self.world)
        for item in self.items:
            item.draw(self.world)
        self.window.blit(self.canvas, (0,0))
        self.window.blit(self.world, (0 + self.player.camera_position.x, 0 + self.player.camera_position.y))
        self.player.update(dt, self.window)
        self.t = self.t + 1
        if self.t == 2:
            self.t = 0
            self.tick()
        for ui_element in self.ui_elements:
            ui_element.draw(self.window, (0, 0))

def get_colored_surf(size, color):
    surf = pygame.Surface(size)
    surf.fill(color)
    return surf