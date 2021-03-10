#Menu showed when play reach new level and can have better stats and new skills 
import pygame as pg
from color import *
from enum import Enum
from input_handlers import handle_main_menu
from render_function import draw_text, draw_panel
from text_align import TEXT_ALIGN
from equipment_slots import EQUIPMENT_SLOTS
from menus.menu import Menu

class SkillPointMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.pauze_offset_x = 30
        self.pauze_offset_y = 30
        self.curr_offset_x = 100

        self.strenght_x, self.strenght_y = self.pauze_offset_x, self.pauze_offset_y 
        self.dexterity_x, self.dexterity_y = self.pauze_offset_x, self.pauze_offset_y + (self.space_h * 1)
        self.constitution_x, self.constitution_y = self.pauze_offset_x, self.pauze_offset_y  + (self.space_h * 2)
        self.intelligence_x, self.intelligence_y = self.pauze_offset_x, self.pauze_offset_y + (self.space_h * 3)
        self.wisdom_x, self.wisdom_y = self.pauze_offset_x, self.pauze_offset_y  + (self.space_h * 4)
        self.charisma_x, self.charisma_y = self.pauze_offset_x, self.pauze_offset_y + (self.space_h * 5)

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
               self.use_item()
           
            panel_height = 40 + (len(self.game.player.inventory.items) * 25)
            draw_panel(self.game.display,INVENTORY_BG, 330, 200, 400, panel_height + 50)
            draw_panel(self.game.display,INVENTORY_INNER, 340, 240, 380, panel_height)
            draw_text(self.game.display,'Inventory',20, self.game.font_name, 440, 220)
            opt = self.draw_inventory()
            self.move_cursor()
            self.draw_cursor(opt)
            self.blit_screen()