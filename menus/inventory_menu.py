import pygame as pg
from game.color import *
from enum import Enum
from game.input_handlers import handle_main_menu
from game.render_function import draw_text, draw_panel
from game.text_align import TEXT_ALIGN
from game.equipment_slots import EQUIPMENT_SLOTS
from menus.menu import Menu
from menus.main_or_offhand_menu import MainOrOffHandMenu
from game.data_loaders import load_xml


class InventoryMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.xml = load_xml("inventory_menu.xml")
        self.option_index = 0
        self.main_off_menu = MainOrOffHandMenu(self.game)
        self.mouse_is_over_menu = False

    def display_menu(self):
       
        self.run_display = True        
        self.curent_item = None
        self.elements = self.render_from_xml(self.xml)
        while self.run_display:
            self.game.clock.tick(self.game.FPS)
            self.handle_manu()
            results = []
            if self.act_quit:
                self.game.running, self.game.playing, self.run_display = False, False, False  
            if self.act_esc:
                self.run_display = False
            if self.act_start_key:
               results.extend(self.use_item())
               return results
               
           
            for element in self.elements:   
                if element["element"].__type__ == "select": 
                    element["element"].create_options(self.get_items())                   
                    mx ,my =pg.mouse.get_pos()
                    index = element["element"].collidepoint(mx,my)
                    if index != None:
                        self.option_index = index
                        self.mouse_is_over_menu = True
                    element["element"].set_cur(self.option_index)
                
                element["element"].draw(self.game.display)

            self.move_cursor()      
            self.blit_screen()

    def use_item(self):
        results = []
        self.curent_item = self.game.player.inventory.items[self.option_index]
        if self.curent_item:
            if self.curent_item.equippable:
                self.use_equicable_item()
            else:
                results.extend(self.game.player.inventory.use(self.curent_item))
        return results
    
    def use_equicable_item(self):
        if self.curent_item.equippable.slot == EQUIPMENT_SLOTS.WEAPONS:
            if self.curent_item.equippable.equipped:
                if self.game.player.equipment.main_hand == self.curent_item.weapon:
                    self.game.player.equipment.toggle_equip_main_hand(self.curent_item)
                else:
                    self.game.player.equipment.toggle_equip_off_hand(self.curent_item)
            elif self.curent_item.weapon.two_hand:
                self.game.player.equipment.toggle_equip_main_hand(self.curent_item)
            else:
                
                op_index = self.main_off_menu.display_menu()
                if op_index == 0:
                    self.game.player.equipment.toggle_equip_main_hand(self.curent_item)
                elif op_index == 1:
                    self.game.player.equipment.toggle_equip_off_hand(self.curent_item)




    def get_items(self):
        items = []
        if self.game.player.inventory and len(self.game.player.inventory.items) != 0:
            for item in self.game.player.inventory.items:
                if self.game.player.equipment.main_hand == item:
                    items.append("{} [on main hand]".format(item.name))
                elif self.game.player.equipment.off_hand == item:
                    items.append("{} [on off hand]".format(item.name))
                else:
                    items.append(item.name)
        
        return items



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
