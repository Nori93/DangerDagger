import pygame as pg
from color import *
from enum import Enum
from input_handlers import handle_main_menu
from render_function import draw_text, draw_panel
from text_align import TEXT_ALIGN
from equipment_slots import EQUIPMENT_SLOTS
from menus.menu import Menu
from menus.main_or_offhand_menu import MainOrOffHandMenu


class InventoryMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.main_off_menu = MainOrOffHandMenu(self.game)

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

    def use_item(self):
         if self.curent_item:
            if self.curent_item.equippable:
                self.use_equicable_item()
    
    def use_equicable_item(self):
        if self.curent_item.equippable.slot == EQUIPMENT_SLOTS.WEAPONS:
            if self.curent_item.equippable.equipped:
                if self.curent_item.weapon.main:
                    self.game.player.equipment.toggle_equip_main_hand(self.curent_item)
                else:
                    self.game.player.equipment.toggle_equip_off_hand(self.curent_item)
            elif self.curent_item.weapon.two_hand:
                self.game.player.equipment.toggle_equip_main_hand(self.curent_item)
            elif self.curent_item.weapon.only_off_hand:
                self.game.player.equipment.toggle_equip_off_hand(self.curent_item)
            else:
                
                op_index = self.main_off_menu.display_menu()
                if op_index == 0:
                    self.game.player.equipment.toggle_equip_main_hand(self.curent_item)
                elif op_index == 1:
                    self.game.player.equipment.toggle_equip_off_hand(self.curent_item)





    def draw_inventory(self):
        options = []        
        if self.game.player.inventory and len(self.game.player.inventory.items) != 0:
            item_y = 250
            item_x = 370
            font_size = 15
            
            for item in self.game.player.inventory.items:
                if self.game.player.equipment.main_hand == item:
                    rect = draw_text(self.game.display,"{} [on main hand]".format(item.name), font_size, self.game.font_name, item_x, item_y,color= BLACK, text_align=TEXT_ALIGN.LEFT)
                    options.append((rect,item))
                elif self.game.player.equipment.off_hand == item:
                    rect =draw_text(self.game.display,"{} [on off hand]".format(item.name), font_size, self.game.font_name, item_x, item_y,color= BLACK, text_align=TEXT_ALIGN.LEFT)
                    options.append((rect,item))
                else:
                    rect = draw_text(self.game.display, item.name, font_size, self.game.font_name, item_x, item_y,color=BLACK, text_align=TEXT_ALIGN.LEFT)
                    options.append((rect,item))
                
                item_y += 20
        return options

    def move_cursor(self):
        if self.act_up_key:
            if self.option_index == 0:
                self.option_index = len(self.game.player.inventory.items) - 1
            else:
                self.option_index -= 1
        if self.act_down_key:
            if self.option_index == len(self.game.player.inventory.items) - 1:
                self.option_index = 0
            else:
                self.option_index += 1

    

    def draw_cursor(self,options):
        rect, item = options[self.option_index]
        draw_text(self.game.display,"=>", 14, self.game.font_name, rect.x - 15, rect.y + 5, color=BLACK)
        self.curent_item = item
