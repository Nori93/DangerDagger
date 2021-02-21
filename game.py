import pygame as pg
from settings import Settings
from color import *
from menu import *
from init_new_game import get_game_variables
from render_function import render_all
from game_state import GameState
from input_handlers import handle_game
from fov_functions import intialize_fov, recompute_fov
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
        self.window = pg.display.set_mode((self.width, self.height))
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
        self.main_manu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_manu


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
    
        self.player, self.entities, self.game_map, self.game_state = get_game_variables(self)
      
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
                    
            self.display.fill(BLACK)
            self.player_turn_results =  []


            if self.act_move and self.game_state == GameState.PLAYERS_TURN:
                self.move()
               
            render_all(self.display,self.game_map,self.fov_map,self.fov_recompute,self.entities)           
            self.window.blit(self.display, (0, 0))
            pg.display.update()



            self.reset_keys()

    def move(self):
        dx,dy = self.act_move
        destination_x = self.player.x + dx
        destination_y = self.player.y + dy
        
        if not self.game_map.is_blocked(destination_x,destination_y):
            target = self.player.get_blocking_entities_at_location(self.entities, destination_x, destination_y)
            if target:
                #attack_results = player.fighter.attack(target)
                #player_turn_results.extend(attack_results)
                pass
            else:
                fov_recompute = True
                self.player.move(dx,dy)


    def draw_text(self, text, size, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

        return text_rect