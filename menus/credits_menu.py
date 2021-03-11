import pygame as pg
from game.color import *
from enum import Enum
from game.input_handlers import handle_main_menu
from game.render_function import draw_text, draw_panel
from game.text_align import TEXT_ALIGN
from game.equipment_slots import EQUIPMENT_SLOTS
from menus.menu import Menu

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:            
            self.handle_manu()
            if self.act_quit:
                self.game.running , self.run_display = False, False  
            if self.act_start_key or self.act_esc or self.act_mouse_left:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(BLACK)
            draw_text(self.game.display,'Credits',40, self.game.font_name, self.mid_w, self.mid_h - 40)
            draw_text(self.game.display,'Mady by Norbert W.',20, self.game.font_name, self.mid_w, self.mid_h + 10)
            self.blit_screen()