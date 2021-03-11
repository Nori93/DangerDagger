
import pygame as pg
from game.color import *
from enum import Enum
from game.input_handlers import handle_main_menu
from game.render_function import draw_text, draw_panel
from game.text_align import TEXT_ALIGN
from game.equipment_slots import EQUIPMENT_SLOTS
from menus.menu import Menu

class PauzeMenu(Menu):

    class STATE(Enum):
        START_NEW_GAME = 0
        SAVE_GAME = 1
        LOAD_GAME = 2
        OPTIONS = 3
        CREDITS = 4
        EXIT = 5


    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.state = PauzeMenu.STATE.START_NEW_GAME
        self.space_h = 40
        self.pauze_offset_x = 30
        self.pauze_offset_y = 30
        self.curr_offset_x = 100

        self.start_x, self.start_y = self.pauze_offset_x, self.pauze_offset_y 
        self.save_x, self.save_y = self.pauze_offset_x, self.pauze_offset_y + (self.space_h * 1)
        self.load_x, self.load_y = self.pauze_offset_x, self.pauze_offset_y  + (self.space_h * 2)
        self.options_x, self.options_y = self.pauze_offset_x, self.pauze_offset_y + (self.space_h * 3)
        self.credits_x, self.credits_y = self.pauze_offset_x, self.pauze_offset_y  + (self.space_h * 4)
        self.exit_x, self.exit_y = self.pauze_offset_x, self.pauze_offset_y + (self.space_h * 5)

        self.cursor_rect_l.midtop = (self.start_x + self.offset_l + self.curr_offset_x, self.start_y + self.offset_h)
        self.cursor_rect_r.midtop = (self.start_x + self.offset_r + self.curr_offset_x, self.start_y + self.offset_h)
        self.mouse_is_over_menu = False

    def display_menu(self):
        self.run_display = True
        self.option_index = 0
        self.curent_item = None
        while self.run_display:
            self.handle_manu()
            if self.act_quit:
                self.game.running, self.game.playing, self.run_display = False, False, False  
            if self.act_esc:
                self.run_display = False
            if self.act_start_key:
               pass
                      
            draw_panel( self.game.display, BLACK, 0, 0, 300, self.game.height )
            draw_panel( self.game.display, DARK_RED, 10, 10, 280, self.game.height - 20)
            self.start_game_rect = draw_text(self.game.display,"New Game",  self.font_size, self.game.font_name, self.start_x , self.start_y,text_align=TEXT_ALIGN.LEFT,color=BLACK)
            self.save_game_rect = draw_text(self.game.display,"Save Game",  self.font_size, self.game.font_name, self.save_x , self.save_y,text_align=TEXT_ALIGN.LEFT,color=BLACK)
            self.load_game_rect = draw_text(self.game.display,"Load Game",  self.font_size, self.game.font_name, self.load_x , self.load_y,text_align=TEXT_ALIGN.LEFT,color=BLACK)
            self.options_rect = draw_text(self.game.display,"Options",  self.font_size, self.game.font_name, self.options_x , self.options_y,text_align=TEXT_ALIGN.LEFT,color=BLACK)
            self.credist_rect = draw_text(self.game.display,"Credits",  self.font_size, self.game.font_name, self.credits_x , self.credits_y,text_align=TEXT_ALIGN.LEFT,color=BLACK)
            self.exit_rect = draw_text(self.game.display,"Exit",  self.font_size, self.game.font_name, self.exit_x , self.exit_y,text_align=TEXT_ALIGN.LEFT,color=BLACK)
         
            self.check_input()           
            self.draw_cursor()
            self.blit_screen()   

    def move_cursor(self):
        if self.act_down_key:
            if self.state == PauzeMenu.STATE.START_NEW_GAME:
                self.set_cur_save()

            elif self.state == PauzeMenu.STATE.SAVE_GAME:
                self.set_cur_load()

            elif self.state == PauzeMenu.STATE.LOAD_GAME:
                self.set_cur_options()

            elif self.state == PauzeMenu.STATE.OPTIONS:
                self.set_cur_credits()
                
            elif self.state == PauzeMenu.STATE.CREDITS:
                self.set_cur_exit()
                
            elif self.state == PauzeMenu.STATE.EXIT:
                self.set_cur_start()
                
        if self.act_up_key:
            if self.state == PauzeMenu.STATE.START_NEW_GAME:
                self.set_cur_exit()
                
            elif self.state == PauzeMenu.STATE.SAVE_GAME:
                self.set_cur_start()
            
            elif self.state == PauzeMenu.STATE.LOAD_GAME:
                self.set_cur_save()

            elif self.state == PauzeMenu.STATE.OPTIONS:
                self.set_cur_load()
                
            elif self.state == PauzeMenu.STATE.CREDITS:
                self.set_cur_options()

            elif self.state == PauzeMenu.STATE.EXIT:
                self.set_cur_credits()
                
        
    def check_input(self):
        self.move_cursor()
        self.move_mouse()
        if self.act_start_key or (self.act_mouse_left and self.mouse_is_over_menu):
            if self.state == PauzeMenu.STATE.START_NEW_GAME:
                #start new game 
                self.game.start_new_game()
                self.run_display = False
            
            elif self.state == PauzeMenu.STATE.SAVE_GAME:
                #save game
                self.game.save_game()
                self.run_display = False
            
            elif self.state == PauzeMenu.STATE.LOAD_GAME:
                #load last saved game
                self.game.load_last_game()
                self.run_display = False

            elif self.state == PauzeMenu.STATE.OPTIONS:
                #load last save
                pass
            elif self.state == PauzeMenu.STATE.CREDITS:
                #credits
                pass
            elif self.state == PauzeMenu.STATE.EXIT:
                self.game.playing ,self.game.running, self.run_display = False, False, False
               
        
   

    def move_mouse(self):
        mx ,my =pg.mouse.get_pos()
        self.mouse_is_over_menu = False
        if self.start_game_rect.collidepoint((mx ,my)):
            self.set_cur_start()
            self.mouse_is_over_menu = True
        
        elif self.save_game_rect.collidepoint((mx ,my)):
            self.set_cur_save()
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
        self.set_cur(self.start_x + self.curr_offset_x,self.start_y)               
        self.state = PauzeMenu.STATE.START_NEW_GAME

    def set_cur_save(self):
        self.set_cur(self.save_x + self.curr_offset_x,self.save_y)               
        self.state = PauzeMenu.STATE.SAVE_GAME
    
    def set_cur_load(self):
        self.set_cur(self.load_x + self.curr_offset_x,self.load_y)        
        self.state = PauzeMenu.STATE.LOAD_GAME

    def set_cur_options(self):
        self.set_cur(self.options_x + self.curr_offset_x,self.options_y)        
        self.state = PauzeMenu.STATE.OPTIONS
    
    def set_cur_credits(self):
        self.set_cur(self.credits_x + self.curr_offset_x,self.credits_y)
        self.state = PauzeMenu.STATE.CREDITS

    def set_cur_exit(self):
        self.set_cur(self.exit_x + self.curr_offset_x,self.exit_y)        
        self.state = PauzeMenu.STATE.EXIT

      
