import pygame as pg
from color import *
from enum import Enum
from input_handlers import handle_main_menu
from render_function import draw_text, draw_panel
from text_align import TEXT_ALIGN
from menus.menu import Menu

class MainMenu(Menu):

    class STATE(Enum):
        START = 0
        LOAD = 1
        OPTIONS = 2
        CREDITS = 3
        EXIT = 4

    def __init__(self,game):
        Menu.__init__(self, game)
        self.space_h = 40
        self.text_offset = 30
        self.state = MainMenu.STATE.START
        self.start_x, self.start_y = self.mid_w, self.mid_h + self.text_offset
        self.load_x, self.load_y = self.mid_w, self.mid_h + self.text_offset + (self.space_h * 1)
        self.options_x, self.options_y = self.mid_w, self.mid_h + self.text_offset + (self.space_h * 2)
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + self.text_offset + (self.space_h * 3)
        self.exit_x, self.exit_y = self.mid_w, self.mid_h + self.text_offset + (self.space_h * 4)
        self.cursor_rect_l.midtop = (self.start_x + self.offset_l, self.start_y + self.offset_h)
        self.cursor_rect_r.midtop = (self.start_x + self.offset_r, self.start_y + self.offset_h)
        self.mouse_is_over_menu = False

    def display_menu(self):
        self.run_display = True
      
        while self.run_display:            
            self.game.clock.tick(self.game.FPS)
            self.handle_manu() 
            if self.act_quit:
                self.game.running , self.run_display = False, False         
            self.game.display.fill(BLACK)
            draw_text(self.game.display,self.game.title,  40, self.game.font_name,self.mid_w , self.mid_h - self.mid_h/3)
            self.start_game_rect = draw_text(self.game.display,"Start Game",  self.font_size, self.game.font_name, self.start_x , self.start_y)
            self.load_game_rect = draw_text(self.game.display,"Load Game",  self.font_size, self.game.font_name, self.load_x , self.load_y)
            self.options_rect = draw_text(self.game.display,"Options",  self.font_size, self.game.font_name, self.options_x , self.options_y)
            self.credist_rect = draw_text(self.game.display,"Credits",  self.font_size, self.game.font_name, self.credits_x , self.credits_y)
            self.exit_rect = draw_text(self.game.display,"Exit",  self.font_size, self.game.font_name, self.exit_x , self.exit_y)
            if self.game.error:
                draw_text(self.game.display,self.game.load_message,  15, self.game.font_name,  self.game.width / 2,self.game.height - 10, text_align= TEXT_ALIGN.CENTER)
            self.check_input()           
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.act_down_key:
            if self.state == MainMenu.STATE.START:
                self.set_cur_load()

            elif self.state == MainMenu.STATE.LOAD:
                self.set_cur_options()

            elif self.state == MainMenu.STATE.OPTIONS:
                self.set_cur_credits()
                
            elif self.state == MainMenu.STATE.CREDITS:
                self.set_cur_exit()
                
            elif self.state == MainMenu.STATE.EXIT:
                self.set_cur_start()
                
        if self.act_up_key:
            if self.state == MainMenu.STATE.START:
                self.set_cur_exit()
                
            elif self.state == MainMenu.STATE.LOAD:
                self.set_cur_start()

            elif self.state == MainMenu.STATE.OPTIONS:
                self.set_cur_load()
                
            elif self.state == MainMenu.STATE.CREDITS:
                self.set_cur_options()

            elif self.state == MainMenu.STATE.EXIT:
                self.set_cur_credits()
                
        
    def check_input(self):
        self.move_cursor()
        self.move_mouse()
        if self.act_start_key or (self.act_mouse_left and self.mouse_is_over_menu):
            if self.state == MainMenu.STATE.START:
                self.game.curr_menu = self.game.create_char                
            elif self.state == MainMenu.STATE.LOAD:
                self.game.playing = True
                self.game.load_game = True
            elif self.state == MainMenu.STATE.OPTIONS:
                self.game.curr_menu = self.game.options
            elif self.state == MainMenu.STATE.CREDITS:
                self.game.curr_menu = self.game.credits
            elif self.state == MainMenu.STATE.EXIT:
                self.game.playing ,self.game.running = False, False
            self.run_display = False
        
   

    def move_mouse(self):
        mx ,my =pg.mouse.get_pos()
        self.mouse_is_over_menu = False
        if self.start_game_rect.collidepoint((mx ,my)):
            self.set_cur_start()
            self.mouse_is_over_menu = True
        
        elif self.load_game_rect.collidepoint((mx ,my)):
            self.set_cur_load()
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
        self.state = MainMenu.STATE.START
    
    def set_cur_load(self):
        self.set_cur(self.load_x,self.load_y)        
        self.state = MainMenu.STATE.LOAD

    def set_cur_options(self):
        self.set_cur(self.options_x,self.options_y)        
        self.state = MainMenu.STATE.OPTIONS
    
    def set_cur_credits(self):
        self.set_cur(self.credits_x,self.credits_y)
        self.state = MainMenu.STATE.CREDITS

    def set_cur_exit(self):
        self.set_cur(self.exit_x,self.exit_y)        
        self.state = MainMenu.STATE.EXIT