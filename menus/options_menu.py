import pygame as pg
from color import *
from enum import Enum
from input_handlers import handle_main_menu
from render_function import draw_text, draw_panel
from menus.menu import Menu
from data_loaders import load_xml
        
class OptionsMenu(Menu):
    
    class STATE(Enum):
        VOLUME = 0
        CONTROLS = 1
        SAVE = 2
        BACK = 3
        
    def __init__(self, game):
        Menu.__init__(self, game)
        self.xml = load_xml("option_menu.xml")
        self.state = OptionsMenu.STATE.VOLUME.value       
        self.mouse_is_over_menu = False

    def display_menu(self):
        self.run_display = True
        self.elements = self.render_from_xml(self.xml)
        while self.run_display:
            self.game.clock.tick(self.game.FPS)
            self.handle_manu()  
            self.game.display.fill(BLACK)
            self.mouse_is_over_menu = False
            
            if self.act_quit:
                self.game.running , self.run_display = False, False    
            
            for element in self.elements:   
                if element["element"].__type__ == "select":                    
                    mx ,my =pg.mouse.get_pos()
                    index = element["element"].collidepoint(mx,my)
                    if index != None:
                        self.state = index
                        self.mouse_is_over_menu = True
                    element["element"].set_cur(self.state)
                
                element["element"].draw(self.game.display)
             
            if self.game.error:
                draw_text(self.game.display,self.game.load_message,  15, self.game.font_name,  self.game.width / 2,self.game.height - 10, text_align= TEXT_ALIGN.CENTER)
            
            self.check_input()
            self.draw_cursor()
            self.blit_screen()
    
    def check_input(self):
        self.move_cursor()
        if self.act_esc:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.act_start_key or (self.act_mouse_left and self.mouse_is_over_menu):
            if self.state == OptionsMenu.STATE.BACK.value:
                #Save Options
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            else:                
                #TO-DO: Create a Volume Menu and Controle Menu
                pass

    def move_cursor(self):
        if self.act_right_key:
            if self.state == OptionsMenu.STATE.BACK.value:
                self.state = OptionsMenu.STATE.VOLUME.value
            else:
                self.state += 1
                
        if self.act_left_key:
            if self.state == OptionsMenu.STATE.VOLUME.value:
                self.state = OptionsMenu.STATE.BACK.value
            else:
                self.state -= 1

