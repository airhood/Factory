import pygame
from Tiles import TileMap
from Spritesheet import Spritesheet
from Player import Player
from UI import Button, Panel, Text
from Conveyor import ItemEntity
from config import *
from LevelManager import LevelManager
import ChipLoader
from OutChip import OutChip

TITLESCENE_IDX = 0
LEVELSELECTSCENE_IDX = 1
GAMESCENE_IDX = 2

class SceneManager():
    def __init__(self, window, clock):
        self.running = True
        self.window = window
        self.clock = clock
        self.current_scene = None
        self.global_var = {
            "current_level": None
        }
        self.scenes = []
    
    def init(self):
        self.scenes = [TitleScene(self.window, self.load_scene, self.global_var),
                       LevelSelectScene(self.window, self.load_scene, self.global_var),
                       GameScene(self.window, self.load_scene, self.global_var)]

    def load_scene(self, scene_id):
        if self.current_scene is not None:
            self.scenes[self.current_scene].stop()
        self.current_scene = scene_id
        self.scenes[self.current_scene].start()
    
    def run(self):
        while self.running:
            # delta time 계산
            dt = self.clock.tick(60) * .001 * TARGET_FPS
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            self.scenes[self.current_scene].run(dt, events)
            pygame.display.update()

class TitleScene():
    def __init__(self, window, load_scene, global_var):
        self.window = window
        self.load_scene = load_scene
        self.global_var = global_var

        # font
        self.I_AM_A_PLAYER_100 = pygame.font.Font("Fonts/I AM A PLAYER.ttf", 100)
        self.I_AM_A_PLAYER_35 = pygame.font.Font("Fonts/I AM A PLAYER.ttf", 35)
        self.I_AM_A_PLAYER_25 = pygame.font.Font("Fonts/I AM A PLAYER.ttf", 25)
        # self.title_text = self.I_AM_A_PLAYER_100.render(TITLE, True, (88, 114, 227))

        self.TitleScreen_background = pygame.transform.scale(pygame.image.load('Images/TitleScreen.jpg'), (DISPLAY_W, DISPLAY_H))

        # 이미지 로드
        self.button_image = pygame.image.load('Images/button.png').convert_alpha()
        
        # UI
        self.ui_elements = []
        self.ui_elements.append(Button(870, 570, self.button_image, self.button_image.get_rect().width * 0.15, self.button_image.get_rect().height * 0.15, lambda: load_scene(LEVELSELECTSCENE_IDX), [
            Text(70, 13, "START", self.I_AM_A_PLAYER_35, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(50, 30, get_colored_surf([1, 1], (130, 130, 130)), self.button_image.get_rect().width * 0.11, self.button_image.get_rect().height * 0.11, lambda: load_scene(2), [
            Text(30, 9, "Settings", self.I_AM_A_PLAYER_25, (255, 255, 255), 400, 250, None)
        ]))

    def start(self):
        pass

    def stop(self):
        pass
    
    def run(self, dt, events):
        # self.window.blit(get_colored_surf([DISPLAY_W, DISPLAY_H], (208, 252, 92)), (0, 0))
        self.window.blit(self.TitleScreen_background, [0, 0])
        for ui_element in self.ui_elements:
            ui_element.draw(self.window, (0, 0))
        # self.window.blit(self.title_text, [90, 100])

class LevelSelectScene():
    def __init__(self, window, load_scene, global_var):
        self.window = window
        self.load_scene = load_scene
        self.global_var = global_var

        #font
        self.I_AM_A_PLAYER_30 = pygame.font.Font("Fonts/I AM A PLAYER.ttf", 30)

        # UI
        self.ui_elements = []
        self.ui_elements.append(Button(100, 100, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(0, 0), [
            Text(34, 33, "1-1", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(250, 100, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(0, 1), [
            Text(33, 33, "1-2", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(400, 100, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(0, 2), [
            Text(32, 33, "1-3", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(550, 100, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(0, 3), [
            Text(32, 33, "1-4", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(700, 100, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(0, 4), [
            Text(32, 33, "1-5", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(850, 100, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(0, 5), [
            Text(32, 33, "1-6", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(1000, 100, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(0, 6), [
            Text(32, 33, "1-7", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))

        self.ui_elements.append(Button(100, 250, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(1, 0), [
            Text(32, 33, "2-1", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(250, 250, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(1, 1), [
            Text(29, 33, "2-2", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(400, 250, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(1, 2), [
            Text(29, 33, "2-3", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(550, 250, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(1, 3), [
            Text(29, 33, "2-4", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(700, 250, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(1, 4), [
            Text(29, 33, "2-5", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(850, 250, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(1, 5), [
            Text(29, 33, "2-6", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
        self.ui_elements.append(Button(1000, 250, get_colored_surf([1, 1], (130, 130, 130)), 100, 100, lambda: self.load_level(1, 6), [
            Text(29, 33, "2-7", self.I_AM_A_PLAYER_30, (255, 255, 255), 400, 250, None)
        ]))
    
    def start(self):
        pass

    def stop(self):
        pass

    def run(self, dt, events):
        self.window.blit(get_colored_surf([DISPLAY_W, DISPLAY_H], (180, 156, 119)), (0, 0))
        for ui_element in self.ui_elements:
            ui_element.draw(self.window, (0, 0))

    def load_level(self, theme, level):
        self.global_var['theme'] = theme
        self.global_var['level'] = level
        self.load_scene(GAMESCENE_IDX)

class GameScene():
    def __init__(self, window, load_scene, global_var):
        self.window = window
        self.load_scene = load_scene
        self.global_var = global_var

        self.background = pygame.Surface((10000, 10000))
        self.canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
        self.canvas.set_colorkey((0, 0, 0))

        # 배경
        self.grid = pygame.image.load("Images/Background Grid.png").convert_alpha()
        self.grid = pygame.transform.scale(self.grid, (2400 * 1.5, 1376 * 1.5))

        # fonts
        self.KCC_Ganpan_15 = pygame.font.Font("Fonts/KCC-Ganpan.ttf", 15)
        self.KCC_Ganpan_20 = pygame.font.Font("Fonts/KCC-Ganpan.ttf", 20)
        self.KCC_Ganpan_80 = pygame.font.Font("Fonts/KCC-Ganpan.ttf", 80)
        self.Consolas = pygame.font.SysFont("Consolas", 14)

        # 이미지 로드
        self.number_icon = pygame.image.load('Images/number_icon.png').convert_alpha()
        self.number_icon.set_colorkey((0, 0, 0))
        self.block_spritesheet = Spritesheet('Images/block_spritesheet')
        self.block_delete_ui = pygame.image.load('Images/block_delete_ui.png')

        # 월드
        self.world = pygame.Surface((10000, 10000))
        self.world.set_colorkey((0, 0, 0))

        # 게임 클리어
        self.is_game_clear = False
        
        # UI
        self.ui_elements = []

        self.description = ""

        self.ui_elements.append(Panel(0, 630, get_colored_surf([1, 1], (130, 130, 130)), 1200, 70, [
            Button(15, 15, self.block_spritesheet.parse_sprite(1-1), 40, 40, lambda: self.set_player_holding_block(1), None),
            *[Button(15 + 60 * i, 15, self.block_spritesheet.parse_sprite((5+i-1)-1), 40, 40, lambda x=i: self.set_player_holding_block(-x), None) for i in range(1, 19)]
        ]))
        self.ui_elements.append(Panel(0, 0, get_colored_surf([1, 1], (170, 170, 170)), 1200, 40, [
            Button(1095, 5, lambda: get_colored_surf([1, 1], (255, 99, 100)) if self.conveyor_run else get_colored_surf([1, 1], (60, 179, 113)), 100, 30, lambda: self.toggle_conveyor(), [
                lambda: Text(27, 0, "STOP", self.KCC_Ganpan_20, (255, 255, 255), 100, 30, None) if self.conveyor_run else Text(21, 0, "START", self.KCC_Ganpan_20, (255, 255, 255), 100, 30, None)
            ])
        ]))
        self.ui_elements.append(Text(360, 270, lambda: (f"LEVEL CLEAR" if self.is_game_clear else ""), self.KCC_Ganpan_80, (0, 0, 0), 300, 100, None))
        self.ui_elements.append(Text(100, 50, lambda: self.description, self.KCC_Ganpan_20, (0, 0, 0), 300, 100, None))

        # Chip
        self.chip_list = ChipLoader.load_chip("chip.json")
        self.chip_instances = []

        # Player
        self.player = Player(self, self.block_spritesheet, self.ui_elements[0], self.chip_list)

        # Tilemap 생성
        self.tilemap = TileMap(self.block_spritesheet, self.player, self.chip_list, self.chip_instances)
        self.player.tilemap = self.tilemap

        # Tick Status
        self.t = 0

        # Sound
        self.bgm = pygame.mixer.Sound('Sounds/＂Fun Puzzle Quest!＂ Calm Puzzle Game Music by HeatleyBros.wav')

        self.level_manager = LevelManager(self)
        self.level_manager.load_levels()
        
        # Item
        self.items = []

        self.item_spawn_tick_t = 0

        self.item_in = None
        self.item_out = None
        self.out_chip_list = {}

        # Conveyor Items
        # self.items.append(ItemEntity(1, 2, 1, self.tilemap, self.block_spritesheet, self.number_icon, self.KCC_Ganpan_15, self.out_chip_list))
        # self.items.append(ItemEntity(1, 4, 1, self.tilemap, self.block_spritesheet, self.number_icon, self.KCC_Ganpan_15, self.out_chip_list))
        self.items_copy = self.copy_items(self.items)

        self.conveyor_run = False

        self.shift = False
    
    def start(self):
        self.is_game_clear = False
        self.conveyor_run = False

        theme, level = self.global_var['theme'], self.global_var['level']
        self.level_manager.load_level(theme, level)
        self.reset_items()

        level_data = self.level_manager.get_level_data(theme, level)

        self.item_in = level_data['in']
        self.item_out = level_data['out']
        self.description = level_data['description']
        for item in self.item_out:
            position = item['position']
            number = item['number']
            out_chip = OutChip(position[0], position[1], number)
            self.out_chip_list[f"{position[0]}-{position[1]}"] = out_chip
        
        self.bgm.play(-1)
    
    def stop(self):
        self.bgm.stop()
    
    def tick(self):
        if self.conveyor_run:
            self.conveyor_tick()

    def conveyor_tick(self):
        self.item_spawn_tick_t += 1
        self.item_spawn_tick_t %= 8
        for item in self.items:
            item.tick()
        if self.item_spawn_tick_t == 0:
            self.item_spawn_tick()
            self.level_clear_check_tick()

    def item_spawn_tick(self):
        for item in self.item_in:
            position = item['position']
            number = item['number']
            item_entity = ItemEntity(position[0]+1, position[1], number, self.tilemap, self.block_spritesheet, self.number_icon, self.KCC_Ganpan_15, self.out_chip_list)
            self.items.append(item_entity)

    def level_clear_check_tick(self):
        for _, out_chip in self.out_chip_list.items():
            if out_chip.state != 2:
                return
        self.game_clear()
    
    def game_clear(self):
        self.is_game_clear = True
    
    def set_player_holding_block(self, id): # 플레이어가 선택한 블럭 id 저장
        if id == None:
            self.player.holding_block = None
            self.player.block_set_image = None
        else:
            self.player.holding_block = id
            if id < 0: id = self.chip_list[-id - 1].tile
            # 블럭 설치 미리보기 이미지 업데이트
            self.player.block_set_image = pygame.transform.scale(self.block_spritesheet.parse_sprite(id - 1), (TILE_SIZE, TILE_SIZE))
            self.player.block_set_image.set_alpha(100)

    def toggle_conveyor(self):
        if self.conveyor_run:
            self.reset_items()
        self.conveyor_run = not self.conveyor_run
    
    def reset_items(self):
        self.items = self.copy_items(self.items_copy)

    def reset_out(self):
        for _, out_chip in self.out_chip_list.items():
            out_chip.reset()
    
    def run(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.shift = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.shift = False
        
        # key input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.shift:
                    if event.key == pygame.K_1:
                        self.player.block_set_rotation = 0
                        self.set_player_holding_block(-12)
                    elif event.key == pygame.K_2:
                        self.player.block_set_rotation = 0
                        self.set_player_holding_block(-13)
                    elif event.key == pygame.K_3:
                        self.player.block_set_rotation = 0
                        self.set_player_holding_block(-14)
                    elif event.key == pygame.K_4:
                        self.player.block_set_rotation = 0
                        self.set_player_holding_block(-15)
                    elif event.key == pygame.K_5:
                        self.player.block_set_rotation = 0
                        self.set_player_holding_block(-16)
                    elif event.key == pygame.K_6:
                        self.player.block_set_rotation = 0
                        self.set_player_holding_block(-17)
                elif event.key == pygame.K_SPACE and self.is_game_clear:
                    self.load_scene(LEVELSELECTSCENE_IDX)
                elif event.key == pygame.K_a:
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
                            holding_block = self.player.holding_block
                            if holding_block == -1: holding_block = 5
                            self.player.block_set_image = pygame.transform.rotate(pygame.transform.scale(self.block_spritesheet.parse_sprite(holding_block - 1), (TILE_SIZE, TILE_SIZE)), 360 - self.player.block_set_rotation * 90)
                            self.player.block_set_image.set_alpha(100)
                elif event.key == pygame.K_x:
                    self.player.block_set_rotation = 0
                    self.player.holding_block = 0
                    self.player.block_set_image = pygame.transform.scale(self.block_delete_ui, (TILE_SIZE, TILE_SIZE))
                elif event.key == pygame.K_ESCAPE:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(None)
                elif event.key == pygame.K_1:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(1)
                elif event.key == pygame.K_2:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(-1)
                elif event.key == pygame.K_3:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(-2)
                elif event.key == pygame.K_4:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(-3)
                elif event.key == pygame.K_5:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(-4)
                elif event.key == pygame.K_6:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(-5)
                elif event.key == pygame.K_7:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(-6)
                elif event.key == pygame.K_8:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(-7)
                elif event.key == pygame.K_9:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(-8)
                elif event.key == pygame.K_0:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(-9)
                elif event.key == pygame.K_MINUS:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(-10)
                elif event.key == pygame.K_EQUALS:
                    self.player.block_set_rotation = 0
                    self.set_player_holding_block(-11)
                
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

        for chip_instance in self.chip_instances:
            if chip_instance.can_calculate():
                return_A, return_B, return_C, return_D = chip_instance.calculate()
                chip_x, chip_y = chip_instance.x, chip_instance.y
                
                if return_A is not None:
                    if self.tilemap.tiles[chip_x][chip_y+1] is not None:
                        self.items.append(ItemEntity(chip_x, chip_y+1, return_A, self.tilemap, self.block_spritesheet, self.number_icon, self.KCC_Ganpan_15, self.out_chip_list))
                if return_B is not None:
                    if self.tilemap.tiles[chip_x-1][chip_y] is not None:
                        self.items.append(ItemEntity(chip_x-1, chip_y, return_B, self.tilemap, self.block_spritesheet, self.number_icon, self.KCC_Ganpan_15, self.out_chip_list))
                if return_C is not None:
                    if self.tilemap.tiles[chip_x][chip_y-1] is not None:
                        self.items.append(ItemEntity(chip_x, chip_y-1, return_C, self.tilemap, self.block_spritesheet, self.number_icon, self.KCC_Ganpan_15, self.out_chip_list))
                if return_D is not None:
                    if self.tilemap.tiles[chip_x+1][chip_y] is not None:
                        self.items.append(ItemEntity(chip_x+1, chip_y, return_D, self.tilemap, self.block_spritesheet, self.number_icon, self.KCC_Ganpan_15, self.out_chip_list))

        for item in self.items:
            if item.remove_this == True:
                self.items.remove(item)
            else:
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

    def copy_items(self, items):
        item_list_copy = []
        for item in items:
            item_list_copy.append(self.copy_item(item))
        return item_list_copy

    def copy_item(self, item):
        item_copy = ItemEntity(item.x, item.y, item.number, item.tilemap, item.block_spritesheet, item.number_icon, item.font, item.out_chip_list)
        return item_copy

def get_colored_surf(size, color):
    surf = pygame.Surface(size)
    surf.fill(color)
    return surf

def get_blit_surf(surf, source, position):
    surf.blit(source, position)