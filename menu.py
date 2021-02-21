import pygame as pg
from color import *
from enum import Enum
from input_handlers import handle_main_manu
class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.width / 2, self.game.height / 2
        self.run_display = True

        self.font_size = 20 
        
        self.cursor_rect_l = pg.Rect(0, 0, self.font_size , self.font_size)
        self.cursor_rect_r = pg.Rect(0, 0, self.font_size, self.font_size)
        
        self.offset_l = -100
        self.offset_r = 115
        self.offset_h = -0

    def draw_cursor(self):
        self.game.draw_text("[",  self.font_size, self.cursor_rect_l.x, self.cursor_rect_l.y)
        self.game.draw_text("]",  self.font_size, self.cursor_rect_r.x, self.cursor_rect_r.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pg.display.update()
        self.game.reset_keys()

    def set_cur(self, x, y):
        self.cursor_rect_l.midtop =(x + self.offset_l, y + self.offset_h)
        self.cursor_rect_r.midtop =(x + self.offset_r, y + self.offset_h)

    def handle_manu(self):
        action = handle_main_manu()
        self.start_key = action.get("start_key")
        self.back_key = action.get("back_key")
        self.down_key = action.get("down_key")
        self.up_key = action.get("up_key")
        self.esc = action.get("esc")
        self.mouse_left = action.get("mouse_left")
        self.quit = action.get("quit")

    

class MainMenu(Menu):

    class State(Enum):
        START = 0
        OPTIONS = 1
        CREDITS = 2
        EXIT = 3

    def __init__(self,game):
        Menu.__init__(self, game)
        self.space_h = 40
        self.text_offset = 30
        self.state = MainMenu.State.START
        self.start_x, self.start_y = self.mid_w, self.mid_h + self.text_offset
        self.options_x, self.options_y = self.mid_w, self.mid_h + self.text_offset + (self.space_h * 1)
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + self.text_offset + (self.space_h * 2)
        self.exit_x, self.exit_y = self.mid_w, self.mid_h + self.text_offset + (self.space_h * 3)
        self.cursor_rect_l.midtop = (self.start_x + self.offset_l, self.start_y + self.offset_h)
        self.cursor_rect_r.midtop = (self.start_x + self.offset_r, self.start_y + self.offset_h)
        self.mouse_is_over_menu = False

    def display_menu(self):
        self.run_display = True
      
        while self.run_display:            
            self.game.clock.tick(self.game.FPS)
            self.handle_manu() 
            if self.quit:
                self.game.running , self.run_display = False, False         
            self.game.display.fill(BLACK)
            self.game.draw_text(self.game.title, 40, self.mid_w , self.mid_h - self.mid_h/3)
            self.start_game_rect = self.game.draw_text("Start Game",  self.font_size, self.start_x , self.start_y)
            self.options_rect =self.game.draw_text("Options",  self.font_size, self.options_x , self.options_y)
            self.credist_rect =self.game.draw_text("Credits",  self.font_size, self.credits_x , self.credits_y)
            self.exit_rect =self.game.draw_text("Exit",  self.font_size, self.exit_x , self.exit_y)
            self.check_input()           
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.down_key:
            if self.state == MainMenu.State.START:
                self.set_cur_options()
                
            elif self.state == MainMenu.State.OPTIONS:
                self.set_cur_credits()
                
            elif self.state == MainMenu.State.CREDITS:
                self.set_cur_exit()
                
            elif self.state == MainMenu.State.EXIT:
                self.set_cur_start()
                
        if self.up_key:
            if self.state == MainMenu.State.START:
                self.set_cur_exit()
                
            elif self.state == MainMenu.State.OPTIONS:
                self.set_cur_start()
                
            elif self.state == MainMenu.State.CREDITS:
                self.set_cur_options()

            elif self.state == MainMenu.State.EXIT:
                self.set_cur_credits()
                
        
    def check_input(self):
        self.move_cursor()
        self.move_mouse()
        if self.start_key or (self.mouse_left and self.mouse_is_over_menu):
            if self.state == MainMenu.State.START:
                self.game.playing = True
            elif self.state == MainMenu.State.OPTIONS:
                self.game.curr_menu = self.game.options
            elif self.state == MainMenu.State.CREDITS:
                self.game.curr_menu = self.game.credits
            elif self.state == MainMenu.State.EXIT:
                self.game.playing ,self.game.running = False, False
            self.run_display = False
        
   

    def move_mouse(self):
        mx ,my =pg.mouse.get_pos()
        self.mouse_is_over_menu = False
        if self.start_game_rect.collidepoint((mx ,my)):
            self.set_cur_start()
            self.mouse_is_over_menu = True

        elif self.options_rect.collidepoint((mx ,my)):
            self.set_cur_options()
            self.mouse_is_over_menu = True
        
        elif self.credist_rect.collidepoint((mx ,my)):
            self.set_cur_credits()
            self.mouse_is_over_menu = True

        elif self.exit_rect.collidepoint((mx ,my)):
            self.set_cur_exit()
            self.mouse_is_over_menu = True

     
    def set_cur_start(self):
        self.set_cur(self.start_x,self.start_y)               
        self.state = MainMenu.State.START

    def set_cur_options(self):
        self.set_cur(self.options_x,self.options_y)        
        self.state = MainMenu.State.OPTIONS
    
    def set_cur_credits(self):
        self.set_cur(self.credits_x,self.credits_y)
        self.state = MainMenu.State.CREDITS

    def set_cur_exit(self):
        self.set_cur(self.exit_x,self.exit_y)        
        self.state = MainMenu.State.EXIT
        
   

class OptionsMenu(Menu):
    
    class State(Enum):
        VOLUME = 0
        CONTROLS = 1
        SAVE = 2
        
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = OptionsMenu.State.VOLUME
        self.space_h = 40
        self.text_offset = 30
        self.vol_x , self.vol_y = self.mid_w, self.mid_h + self.text_offset
        self.controls_x, self.controls_y = self.mid_w, self.mid_h + self.text_offset + (self.space_h * 1)
        self.save_x, self.save_y = self.mid_w, self.mid_h + self.text_offset + (self.space_h * 2)
        self.cursor_rect_l.midtop = (self.vol_x + self.offset_l, self.vol_y + self.offset_h)
        self.cursor_rect_r.midtop = (self.vol_x + self.offset_r, self.vol_y + self.offset_h)
        self.mouse_is_over_menu = False


    def display_menu(self):
        self.run_display = True
        while self.run_display:            
            self.game.display.fill(BLACK)
            self.handle_manu()
            if self.quit:
                self.game.running , self.run_display = False, False    
            self.game.draw_text("Options", 40, self.mid_w , self.mid_h - self.mid_h/3)
            self.vol_rect = self.game.draw_text("Volume",  self.font_size, self.vol_x , self.vol_y)
            self.controls_rect =self.game.draw_text("Controls",  self.font_size, self.controls_x , self.controls_y)
            self.save_rect =self.game.draw_text("Save",  self.font_size, self.save_x , self.save_y)
            self.check_input()
            self.draw_cursor()
            self.blit_screen()
    
    def check_input(self):
        self.move_cursor()
        self.move_mouse()
        if self.esc:
            self.game.curr_menu = self.game.main_manu
            self.run_display = False
        elif self.start_key or (self.mouse_left and self.mouse_is_over_menu):
            if self.state == OptionsMenu.State.SAVE:
                #Save Options
                self.game.curr_menu = self.game.main_manu
                self.run_display = False
            else:                
                #TO-DO: Create a Volume Menu and Controle Menu
                pass


    def move_cursor(self):
        if self.down_key:
            if self.state == OptionsMenu.State.VOLUME:
                self.set_curr_controls()
            elif self.state == OptionsMenu.State.CONTROLS:
                self.set_curr_save()
            elif self.state == OptionsMenu.State.SAVE:
                self.set_curr_vol()
        if self.up_key:
            if self.state == OptionsMenu.State.VOLUME:
                self.set_curr_save()
            elif self.state == OptionsMenu.State.CONTROLS:
                self.set_curr_vol()
            elif self.state == OptionsMenu.State.SAVE:
                self.set_curr_controls()

    def move_mouse(self):
        mx ,my =pg.mouse.get_pos()
        self.mouse_is_over_menu = False
        if self.vol_rect.collidepoint((mx ,my)):
            self.set_curr_vol()
            self.mouse_is_over_menu = True

        elif self.controls_rect.collidepoint((mx ,my)):
            self.set_curr_controls()
            self.mouse_is_over_menu = True
        
        elif self.save_rect.collidepoint((mx ,my)):
            self.set_curr_save()
            self.mouse_is_over_menu = True

    def set_curr_vol(self):
        self.set_cur(self.vol_x,self.vol_y)        
        self.state = OptionsMenu.State.VOLUME
    
    def set_curr_controls(self):
        self.set_cur(self.controls_x,self.controls_y)        
        self.state = OptionsMenu.State.CONTROLS

    def set_curr_save(self):
        self.set_cur(self.save_x,self.save_y)        
        self.state = OptionsMenu.State.SAVE

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:            
            self.handle_manu()
            if self.start_key or self.esc or self.mouse_left:
                self.game.curr_menu = self.game.main_manu
                self.run_display = False
            self.game.display.fill(BLACK)
            self.game.draw_text('Credits',40, self.mid_w,self.mid_h - 40)
            self.game.draw_text('Mady by Norbert W.',20, self.mid_w, self.mid_h + 10)
            self.blit_screen()
