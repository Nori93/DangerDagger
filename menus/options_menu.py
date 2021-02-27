import pygame as pg
from color import *
from enum import Enum
from input_handlers import handle_main_menu
from render_function import draw_text, draw_panel
from menus.menu import Menu
        
class OptionsMenu(Menu):
    
    class STATE(Enum):
        VOLUME = 0
        CONTROLS = 1
        SAVE = 2
        
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = OptionsMenu.STATE.VOLUME
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
            if self.act_quit:
                self.game.running , self.run_display = False, False    
            draw_text(self.game.display,"Options", 40, self.game.font_name, self.mid_w , self.mid_h - self.mid_h/3)
            self.vol_rect = draw_text(self.game.display,"Volume",  self.font_size, self.game.font_name, self.vol_x , self.vol_y)
            self.controls_rect =draw_text(self.game.display,"Controls",  self.font_size,  self.game.font_name, self.controls_x , self.controls_y)
            self.save_rect =draw_text(self.game.display,"Save",  self.font_size, self.game.font_name, self.save_x , self.save_y)
            self.check_input()
            self.draw_cursor()
            self.blit_screen()
    
    def check_input(self):
        self.move_cursor()
        self.move_mouse()
        if self.act_esc:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.act_start_key or (self.act_mouse_left and self.mouse_is_over_menu):
            if self.state == OptionsMenu.STATE.SAVE:
                #Save Options
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            else:                
                #TO-DO: Create a Volume Menu and Controle Menu
                pass


    def move_cursor(self):
        if self.act_down_key:
            if self.state == OptionsMenu.STATE.VOLUME:
                self.set_curr_controls()
            elif self.state == OptionsMenu.STATE.CONTROLS:
                self.set_curr_save()
            elif self.state == OptionsMenu.STATE.SAVE:
                self.set_curr_vol()
        if self.act_up_key:
            if self.state == OptionsMenu.STATE.VOLUME:
                self.set_curr_save()
            elif self.state == OptionsMenu.STATE.CONTROLS:
                self.set_curr_vol()
            elif self.state == OptionsMenu.STATE.SAVE:
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
        self.state = OptionsMenu.STATE.VOLUME
    
    def set_curr_controls(self):
        self.set_cur(self.controls_x,self.controls_y)
        self.state = OptionsMenu.STATE.CONTROLS

    def set_curr_save(self):
        self.set_cur(self.save_x,self.save_y)        
        self.state = OptionsMenu.STATE.SAVE
