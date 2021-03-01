import pygame as pg
from color import *
from input_handlers import handle_main_menu
from render_function import draw_text, draw_panel

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
        draw_text(self.game.display,"[",  self.font_size, self.game.font_name, self.cursor_rect_l.x, self.cursor_rect_l.y)
        draw_text(self.game.display,"]",  self.font_size, self.game.font_name, self.cursor_rect_r.x, self.cursor_rect_r.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pg.display.update()      

    def set_cur(self, x, y, offset_r=115,offset_l = -100,offset_h = 0):
        self.cursor_rect_l.midtop =(x + offset_l, y + offset_h)
        self.cursor_rect_r.midtop =(x + offset_r, y + offset_h)

    def handle_manu(self):
        action = handle_main_menu()
        self.act_start_key = action.get("start_key")
        self.act_back_key = action.get("back_key")
        self.act_down_key = action.get("down_key")
        self.act_up_key = action.get("up_key")
        self.act_esc = action.get("esc")
        self.act_mouse_left = action.get("mouse_left")
        self.act_quit = action.get("quit")

    
