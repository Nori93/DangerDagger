
import pygame as pg
from game.color import *
from enum import Enum
from game.input_handlers import handle_main_menu
from game.render_function import draw_text, draw_panel
from game.text_align import TEXT_ALIGN
from game.equipment_slots import EQUIPMENT_SLOTS
from menus.menu import Menu

class MainOrOffHandMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game    

    def display_menu(self):
        self.run_display = True
        self.option_index = 0        
        while self.run_display:
            self.handle_manu()
            if self.act_quit:
                self.game.running, self.game.playing, self.run_display = False, False, False  
            if self.act_esc:
                self.run_display = False
                return None
            if self.act_start_key:
                return self.option_index
           
            panel_height = 40 + (len(self.game.player.inventory.items) * 25)
            draw_panel(self.game.display,INVENTORY_BG, 330, 200, 400, panel_height + 50)
            draw_panel(self.game.display,INVENTORY_INNER, 340, 240, 380, panel_height)
            draw_text(self.game.display,'Inventory',20, self.game.font_name,440, 220)
          
            opt = self.draw_option()
            self.move_cursor()
            self.draw_cursor(opt)
            self.blit_screen()
            
    def draw_option(self):
        options = []    
        options.append(draw_text(self.game.display,"main hand",15, self.game.font_name, 370, 250,color= BLACK, text_align=TEXT_ALIGN.LEFT))
        options.append(draw_text(self.game.display,"off hand",15, self.game.font_name, 370, 270,color= BLACK, text_align=TEXT_ALIGN.LEFT))               
        return options

    def move_cursor(self):
        if self.act_down_key:
            if self.option_index == 0:
                self.option_index = len(self.game.player.inventory.items) - 1
            else:
                self.option_index -= 1
        if self.act_up_key:
            if self.option_index == len(self.game.player.inventory.items) - 1:
                self.option_index = 0
            else:
                self.option_index += 1
   

    def draw_cursor(self,options):
        rect = options[self.option_index]
        draw_text(self.game.display,"=>", 14, self.game.font_name, rect.x - 15, rect.y + 5, color=BLACK)
       

            