import pygame as pg
from game.settings import Settings
from game.color import *
from game.menu import *

class Game:
    
    def __init__(self):
        #Get the standard settings
        self.settings = Settings()

        self.width = self.settings.get["screen_width"]
        self.height = self.settings.get["screen_height"]

        # get title from settings
        self.title = self.settings.get["window_title"]

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

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.ESC:
                self.playing = False           
            self.display.fill(BLACK)
            self.draw_text("Thanks for playing", 20, self.width/2 ,self.height/2)
            self.window.blit(self.display, (0, 0))
            pg.display.update()
            self.reset_keys()

   

    def draw_text(self, text, size, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

        return text_rect