import pygame as pg
from settings import Settings
from color import *
from menu import *
from init_new_game import get_game_variables
from render_function import render_all
from death_functions import *
from game_state import GameState
from input_handlers import handle_game
from fov_functions import intialize_fov, recompute_fov
from text_align import TEXT_ALIGN
class Game:   

    def __init__(self):
        #Get the standard settings
        self.settings = Settings()
        
        self.clock = pg.time.Clock()
        self.FPS = self.settings.get["FPS"]

        self.width = self.settings.get["screen_width"]
        self.height = self.settings.get["screen_height"]


        self.tile_size = self.settings.get["tile_size"]
        self.map_width = int(self.width / self.tile_size)
        self.map_height= int(self.height/ self.tile_size)  

        self.message_x = self.settings.get["message_x"]
        self.message_width = self.settings.get["message_width"]
        self.message_height = self.settings.get["message_height"]

        # get title from settings
        self.title = self.settings.get["window_title"]



        self.fov_radius = self.settings.get["fov_radius"]
        self.fov_algorithm = self.settings.get["fov_algorithm"]
        self.fov_light_walls = self.settings.get["fov_light_walls"]

        #initalize game window.
        pg.init()
        #initalize game sounds
        pg.mixer.init()
        self.display = pg.Surface((self.width, self.height))

        #set screen 
        self.window = pg.display.set_mode((self.width, self.height + 100))
        #set title of game
        pg.display.set_caption(self.title)
        #set clock for FPS
        self.clock = pg.time.Clock()
        #set Main Bool if is Game running
        self.running = True
        self.playing = False
        #find font in the client computer
        self.font_name = self.settings.get["font"]
        
        self.max_room = self.settings.get["max_room"]
        self.room_min_size = self.settings.get["room_min_size"]
        self.room_max_size = self.settings.get["room_max_size"]
        

        self.load_data()

        #keys
        self.reset_keys()
        #Main Manu
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)        
        self.curr_menu = self.main_menu
        #Sub Menu
        self.inventory = InventoryMenu(self)
        self.sub_menu = None

    def load_data(self):
        pass
    

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing  = False, False
                self.curr_menu.run_display = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.START_KEY = True
                if event.key == pg.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pg.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pg.K_UP:
                    self.UP_KEY = True
                if event.key == pg.K_ESCAPE:
                    self.ESC = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.L_MOUSE_BUTTON_DOWN = True
    

    def reset_keys(self):
         self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY ,self.L_MOUSE_BUTTON_DOWN, self.ESC = False, False, False, False, False, False

    def handle_game_keys(self):
        action = handle_game(self.game_state)
        self.act_move = action.get("move")
        self.act_pickup = action.get("pickup")
        self.act_show_inv = action.get("show_inventory")
        self.act_drop_inv = action.get("drop_inventory")
        self.act_char_scr = action.get("show_character_screen")
        self.act_full = action.get("fullscreen")
        self.act_stairs = action.get("take_stairs")
        self.act_exit = action.get("exit")
        self.act_quit = action.get("quit")


    def game_loop(self):
        self.player = None
        self.entities = []
        self.game_map = None
        self.message_log = None
        self.game_state = None
    
        self.player, self.entities, self.game_map, self.game_state, self.message_log = get_game_variables(self)
      
        self.fov_map = intialize_fov(self.game_map)
        self.fov_recompute = True
        while self.playing:
            if self.fov_recompute:
                recompute_fov(self.fov_map, self.player.x, self.player.y, self.fov_radius,
                    self.fov_light_walls, self.fov_algorithm)

            self.handle_game_keys()
            if self.act_quit:
                self.playing , self.running = False, False
            if self.act_exit:
                self.playing = False    
            if self.act_show_inv:
                self.inventory.display_menu()

            self.display.fill(BLACK)
            self.player_turn_results =  []


            if self.act_move and self.game_state == GameState.PLAYERS_TURN:
                self.move()
                self.game_state = GameState.ENEMY_TURN
               
            render_all(self.display,self.game_map,self.fov_map,self.fov_recompute,self.entities)           
            self.window.blit(self.display, (0, 0))
            pg.display.update()
            if self.game_state == GameState.ENEMY_TURN:
                self.enemy_move()


           
    def enemy_move(self):
        for entity in self.entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(self.player, self.fov_map, self.game_map, self.entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get("message")
                        dead_entity = enemy_turn_result.get("dead")

                        if message:
                            self.message_log.add_message(message)
                        if dead_entity:
                            if dead_entity == self.player:
                                message , self.game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)
                            self.message_log .add_message(message)
                        if self.game_state == GameState.PLAYER_DEAD:
                            break
                    if self.game_state == GameState.PLAYER_DEAD:
                        break
        else:
            self.game_state = GameState.PLAYERS_TURN
    def move(self):
        dx,dy = self.act_move
        destination_x = self.player.x + dx
        destination_y = self.player.y + dy
        
        if not self.game_map.is_blocked(destination_x,destination_y):
            target = self.player.get_blocking_entities_at_location(self.entities, destination_x, destination_y)
            if target:
                attack_results = self.player.fighter.attack(target)
                player_turn_results.extend(attack_results)                
            else:
                fov_recompute = True
                self.player.move(dx,dy)


    def draw_text(self, text, size, x, y, color=WHITE,text_align=TEXT_ALIGN.CENTER):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if text_align == TEXT_ALIGN.CENTER:
            text_rect.center = (x,y)
        elif text_align == TEXT_ALIGN.LEFT:
            text_rect.midleft = (x, y)
        elif text_align == TEXT_ALIGN.RIGHT:
            text_rect.midright = (x,y)
        self.display.blit(text_surface,text_rect)

        return text_rect

    def draw_panel(self, color, x, y, width, height):
        rect = (x, y, width, height)
        pg.draw.rect(self.display,color,rect)
        return rect