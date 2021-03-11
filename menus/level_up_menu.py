#Menu showed when play reach new level and can have better stats and new skills 
import pygame as pg
from game.color import *
from enum import Enum
from menus.menu import Menu

class LevelUpMenu(Menu):
    
    class STATE(Enum):
        STR = 0,


    def __init__(self, game):
        Menu.__init__(self, game)
        self.xml = load_xml("main_menu.xml")  
        self.state = MainMenu.STATE.START.value 
        self.mouse_is_over_menu = False
   
    def display_menu(self):
        self.run_display = True
        self.option_index = 0
        self.curent_item = None
        while self.run_display:
            self.game.clock.tick(self.game.FPS)
            self.handle_manu() 
            self.game.display.fill(BLACK)
            self.mouse_is_over_menu = False

            if self.act_quit:
                self.game.running, self.game.playing, self.run_display = False, False, False  
            if self.act_esc:
                self.run_display = False
            if self.act_start_key:
               self.use_item()
           
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
        if self.act_start_key or (self.act_mouse_left and self.mouse_is_over_menu):
            if self.state == MainMenu.STATE.START.value:
                self.game.curr_menu = self.game.create_char                
            elif self.state == MainMenu.STATE.LOAD.value:
                self.game.playing = True
                self.game.load_game = True
            elif self.state == MainMenu.STATE.OPTIONS.value:
                self.game.curr_menu = self.game.options
            elif self.state == MainMenu.STATE.CREDITS.value:
                self.game.curr_menu = self.game.credits
            elif self.state == MainMenu.STATE.EXIT.value:
                self.game.playing ,self.game.running = False, False
            self.run_display = False
        
    def move_cursor(self):
        if self.act_down_key:
            if self.state == MainMenu.STATE.EXIT.value:
                self.state = MainMenu.STATE.START.value
            else:
                self.state += 1
                
        if self.act_up_key:
            if self.state == MainMenu.STATE.START.value:
                self.state = MainMenu.STATE.EXIT.value
            else:
                self.state -= 1
