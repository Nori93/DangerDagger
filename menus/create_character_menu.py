import pygame as pg
from color import *
from enum import Enum
from input_handlers import handle_main_menu
from render_function import draw_text, draw_panel
from text_align import TEXT_ALIGN
from menus.menu import Menu
from data_loaders import load_race, load_class
from race_enum import RACE
from class_enum import CLASS


class CreateCharacterMenu(Menu):
    class STATE(Enum):
        SELECT_RACE = 0
        SELECT_CLASSE = 1
        ROLL_DICE = 2
        SET_ROLLS = 3
        CHARACTER_DESC = 4

    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.state = CreateCharacterMenu.STATE.SELECT_RACE
       
        self.selected_race = None       
        self.selected_class = None
        
        self.loadet_race = None
        self.loadet_class = None

        self.select_panel_x = 0
        self.select_panel_y = 300
        self.offset_x = 30
        self.offset_y = 30
                
        self.option_index = 0    
        self.loadet_index = -1

        self.race = [
            RACE.DRAGONBORN,
            RACE.DWARF,
            RACE.ELF,
            RACE.GNOME,
            RACE.HALF_ELF,
            RACE.HALFLING,
            RACE.HALF_ORC,
            RACE.HUMAN,
            RACE.TIEFLING
        ]

        self._class = [
            CLASS.BARBARIAN,
            CLASS.BARD,
            CLASS.CLERIC,
            CLASS.DRUID,
            CLASS.FIGHTER,
            CLASS.MONK,
            CLASS.PALADIN,
            CLASS.RANGER,
            CLASS.ROGUE,
            CLASS.SORCERER,
            CLASS.WARLOCK,
            CLASS.WIZARD
        ]

        self.strenght = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0

        self.t_strenght = 0
        self.t_dexterity = 0
        self.t_constitution = 0
        self.t_intelligence = 0
        self.t_wisdom = 0
        self.t_charisma = 0

    def display_menu(self):
        self.run_display = True        
        while self.run_display:
            self.handle_manu()
            #Handle guid and exit action
            if self.act_quit:
                self.game.running, self.game.playing, self.run_display = False, False, False  
            if self.act_esc:
                self.run_display = False
            #clear screen
            self.game.display.fill(BLACK)
            draw_text(self.game.display, "Race:{}".format(self.selected_race), self.font_size, self.game.font_name,
            20, 20, text_align=TEXT_ALIGN.LEFT)
            draw_text(self.game.display, "Class:{}".format(self.selected_class), self.font_size, self.game.font_name,
            20, 40, text_align=TEXT_ALIGN.LEFT)
            
            self.display_stats()

            if self.state == CreateCharacterMenu.STATE.SELECT_RACE:
                self.display_race_menu()

            if self.state == CreateCharacterMenu.STATE.SELECT_CLASSE:
                self.display_class_menu()

            self.blit_screen()

    def display_stats(self):
        draw_text(self.game.display, "Strenght:     {}+{}".format(self.strenght,self.t_strenght,), self.font_size, self.game.font_name,
            20, 70, text_align=TEXT_ALIGN.LEFT)
        draw_text(self.game.display, "Dexterity:    {}+{}".format(self.dexterity,self.t_dexterity), self.font_size, self.game.font_name,
            20, 92, text_align=TEXT_ALIGN.LEFT)
        draw_text(self.game.display, "Constitution: {}+{}".format(self.constitution,self.t_constitution), self.font_size, self.game.font_name,
            20, 114, text_align=TEXT_ALIGN.LEFT)
        draw_text(self.game.display, "Intelligence: {}+{}".format(self.intelligence,self.t_intelligence), self.font_size, self.game.font_name,
            20, 136, text_align=TEXT_ALIGN.LEFT)
        draw_text(self.game.display, "Wisdom:       {}+{}".format(self.wisdom,self.t_wisdom), self.font_size, self.game.font_name,
            22, 158, text_align=TEXT_ALIGN.LEFT)
        draw_text(self.game.display, "Charisma:     {}+{}".format(self.charisma,self.t_charisma), self.font_size, self.game.font_name,
            20, 180, text_align=TEXT_ALIGN.LEFT)

    def reset_temp_stats(self):
        self.t_strenght = 0
        self.t_dexterity = 0
        self.t_constitution = 0
        self.t_intelligence = 0
        self.t_wisdom = 0
        self.t_charisma = 0

    def display_race_menu(self):
        self.race_option = []
        for i in range(0, len(self.race)):
            self.race_option.append(draw_text(self.game.display, self.race[i].name, self.font_size, self.game.font_name,
             self.select_panel_x + self.offset_x,
             self.select_panel_y + self.offset_y * i,
             text_align=TEXT_ALIGN.LEFT))
        
        self.set_cur(
            self.race_option[self.option_index].x + 100,
            self.race_option[self.option_index].y + 10,
            )

      

        if self.option_index != self.loadet_index:
            self.loadet_race = load_race(self.race[self.option_index])
            self.loadet_index = self.option_index
            self.reset_temp_stats()
            self.set_race_stats()

        if self.loadet_race:
            self.display_race_desc()
        
        if self.act_start_key:
            self.selected_race = self.race[self.option_index]
            self.strenght +=self.t_strenght
            self.dexterity +=self.t_dexterity
            self.constitution +=self.t_constitution
            self.intelligence +=self.t_intelligence
            self.wisdom += self.t_wisdom
            self.charisma += self.t_charisma
            self.reset_temp_stats()
            self.option_index = 0
            self.loadet_index = -1
            self.state = CreateCharacterMenu.STATE.SELECT_CLASSE

        self.move_cursor(self.race)
        self.draw_cursor()

    
    def display_race_desc(self):
        draw_text(self.game.display, "Name:{}".format(self.loadet_race["race"]), self.font_size, self.game.font_name,
            300, 290, text_align=TEXT_ALIGN.LEFT)
        
        draw_text(self.game.display, "Description:", self.font_size, self.game.font_name,
            300, 330, text_align=TEXT_ALIGN.LEFT)
        
        _y = 22
        for desc in self.loadet_race["desc"].split('\n'):
            draw_text(self.game.display, desc, self.font_size, self.game.font_name,
            300, 330 + _y, text_align=TEXT_ALIGN.LEFT)
            _y += 22

        draw_text(self.game.display, "Aditional:", self.font_size, self.game.font_name,
            300, 350 + _y, text_align=TEXT_ALIGN.LEFT)
        
        for adition in self.loadet_race["aditional"]:
            draw_text(self.game.display, adition, self.font_size, self.game.font_name,
            300, 370 + _y, text_align=TEXT_ALIGN.LEFT)
            _y += 22

    def set_race_stats(self):
        if "strenght" in self.loadet_race:
            self.t_strenght = self.loadet_race["strenght"]
        if "dexterity" in self.loadet_race:
            self.t_dexterity = self.loadet_race["dexterity"]
        if "constitution" in self.loadet_race:
            self.t_constitution = self.loadet_race["constitution"]
        if "intelligence" in self.loadet_race:
            self.t_intelligence = self.loadet_race["intelligence"]
        if "wisdom" in self.loadet_race:
            self.t_wisdom = self.loadet_race["wisdom"]
        if "charisma" in self.loadet_race:
            self.t_charisma = self.loadet_race["charisma"]


    def display_class_menu(self):
        self.class_option = []
        for i in range(0, len(self._class)):
            self.class_option.append(draw_text(self.game.display, self._class[i].name, self.font_size, self.game.font_name,
             self.select_panel_x + self.offset_x,
             self.select_panel_y + self.offset_y * i,
             text_align=TEXT_ALIGN.LEFT))
        
        self.set_cur(
            self.class_option[self.option_index].x + 100,
            self.class_option[self.option_index].y + 10,
            )

        if self.act_start_key:
            pass

        if self.option_index != self.loadet_index:
            self.loadet_class = load_class(self._class[self.option_index])
            self.loadet_index = self.option_index
            self.reset_temp_stats()
            

        if self.loadet_class:
            self.display_class_desc()

        self.move_cursor(self._class)
        self.draw_cursor()

    def move_cursor(self,array):
        if self.act_down_key:
            if len(array) - 1 == self.option_index:
                self.option_index = 0
            else:
                self.option_index += 1
        if self.act_up_key:
            if 0 == self.option_index:
                self.option_index = len(array) - 1
            else:
                self.option_index -=1
    
    def display_class_desc(self):
        
        self.font_size_low = 16
        self.top_panel_x = self.game.width-20

        draw_text(self.game.display,"Weapons:", self.font_size, self.game.font_name,
            self.top_panel_x, 40, text_align=TEXT_ALIGN.RIGHT)
        
        
        if "weapon_choice" in self.loadet_class["equipment"]:  
            weapon_choice = self.loadet_class["equipment"]["weapon_choice"]            

            if "main_hand" in weapon_choice[0] and "off_hand" in weapon_choice[0]:
                draw_text(self.game.display,"Main:{},Off:{}".format(weapon_choice[0]["main_hand"],weapon_choice[0]["off_hand"]), self.font_size_low, self.game.font_name,
                    self.top_panel_x, 62, text_align=TEXT_ALIGN.RIGHT)
            elif "main_hand" in weapon_choice[0] and "off_hand" not in weapon_choice[0]:
                draw_text(self.game.display,"Main:{},Off:{}".format(weapon_choice[0]["main_hand"],"Empty"), self.font_size_low, self.game.font_name,
                    self.top_panel_x, 62, text_align=TEXT_ALIGN.RIGHT)
            elif "main_hand" not in weapon_choice[0] and "off_hand" in weapon_choice[0]:
                draw_text(self.game.display,"Main:{},Off:{}".format("Empty",weapon_choice[0]["off_hand"]), self.font_size_low, self.game.font_name,
                    self.top_panel_x, 62, text_align=TEXT_ALIGN.RIGHT)

            if len(self.loadet_class["equipment"]["weapon_choice"]) > 1:
            
                draw_text(self.game.display,"Or", self.font_size_low, self.game.font_name,
                    self.top_panel_x, 84, text_align=TEXT_ALIGN.RIGHT)

                if "main_hand" in weapon_choice[1] and "off_hand" in weapon_choice[1]:
                    draw_text(self.game.display,"Main:{},Off:{}".format(weapon_choice[1]["main_hand"],weapon_choice[1]["off_hand"]), self.font_size_low, self.game.font_name,
                        self.top_panel_x, 106, text_align=TEXT_ALIGN.RIGHT)
                elif "main_hand" in weapon_choice[1] and "off_hand" not in weapon_choice[1]:
                    draw_text(self.game.display,"Main:{},Off:{}".format(weapon_choice[1]["main_hand"],"Empty"), self.font_size_low, self.game.font_name,
                        self.top_panel_x, 106, text_align=TEXT_ALIGN.RIGHT)
                elif "main_hand" not in weapon_choice[1] and "off_hand" in weapon_choice[1]:
                    draw_text(self.game.display,"Main:{},Off:{}".format("Empty",weapon_choice[1]["off_hand"]), self.font_size_low, self.game.font_name,
                        self.top_panel_x, 106, text_align=TEXT_ALIGN.RIGHT)

        draw_text(self.game.display,"Equipment:", self.font_size, self.game.font_name,
            self.top_panel_x, 133, text_align=TEXT_ALIGN.RIGHT)
        
        if "armor_choice" in self.loadet_class["equipment"]:
            armor_choice = self.loadet_class["equipment"]["armor_choice"]

            if len(armor_choice) > 0:
                draw_text(self.game.display,"Armor:{}".format(armor_choice[0]["armor"]), self.font_size_low, self.game.font_name,
                    self.top_panel_x, 155, text_align=TEXT_ALIGN.RIGHT)
            if len(armor_choice) > 1:
                draw_text(self.game.display,"Or", self.font_size_low, self.game.font_name,
                    self.top_panel_x, 177, text_align=TEXT_ALIGN.RIGHT)
                draw_text(self.game.display,"Armor:{}".format(armor_choice[1]["armor"]), self.font_size_low, self.game.font_name,
                    self.top_panel_x, 199, text_align=TEXT_ALIGN.RIGHT)

        
        draw_text(self.game.display, "Name:{}".format(self.loadet_class["class"]), self.font_size, self.game.font_name,
            300, 220, text_align=TEXT_ALIGN.LEFT)
        
        draw_text(self.game.display, "Description:", self.font_size, self.game.font_name,
            300, 260, text_align=TEXT_ALIGN.LEFT)
        
        _y = 22
        for desc in self.loadet_class["desc"].split('\n'):
            draw_text(self.game.display, desc, self.font_size, self.game.font_name,
            300, 260 + _y, text_align=TEXT_ALIGN.LEFT)
            _y += 22

        draw_text(self.game.display, "Hit Die: {}".format(self.loadet_class["hit_die"]), self.font_size, self.game.font_name,
            300, 280 + _y, text_align=TEXT_ALIGN.LEFT)
        
        draw_text(self.game.display, "Primary Ability:", self.font_size, self.game.font_name,
            300, 300 + _y, text_align=TEXT_ALIGN.LEFT)

        for pri_abil in self.loadet_class["primary_ability"]:
            draw_text(self.game.display, pri_abil, self.font_size, self.game.font_name,
            300, 320 + _y, text_align=TEXT_ALIGN.LEFT)
            _y += 22

        draw_text(self.game.display, "Saves:", self.font_size, self.game.font_name,
            300, 340 + _y, text_align=TEXT_ALIGN.LEFT)

        for saves in self.loadet_class["saves"]:
            draw_text(self.game.display, saves, self.font_size, self.game.font_name,
            300, 360 + _y, text_align=TEXT_ALIGN.LEFT)
            _y += 22

        if "items_choice" in self.loadet_class["equipment"]:  
            items_choice =  self.loadet_class["equipment"]["items_choice"]
            if "items" in items_choice[0]:
                draw_text(self.game.display, "Items:", self.font_size, self.game.font_name,
                        300, 380 + _y, text_align=TEXT_ALIGN.LEFT)
                items_list = []

                for item in items_choice[0]["items"]:
                    add = True
                    for i in items_list:
                        if i["item"] == item:
                            i["count"] += 1
                            add = False
                            break
                    if add:
                        items_list.append({"item":item,"count":1}) 

                for it in items_list:
                    draw_text(self.game.display, "x{} {}".format(it["count"],it["item"]), self.font_size, self.game.font_name,
                        300, 400 + _y, text_align=TEXT_ALIGN.LEFT)
                    _y += 22
            
            if len(items_choice) > 1 and "items" in items_choice[1]:
                draw_text(self.game.display, "Items:", self.font_size, self.game.font_name,
                        300, 420 + _y, text_align=TEXT_ALIGN.LEFT)
                items_list = []

                for item in items_choice[1]["items"]:
                    add = True
                    for i in items_list:
                        if i["item"] == item:
                            i["count"] += 1
                            add = False
                            break
                    if add:
                        items_list.append({"item":item,"count":1}) 

                for it in items_list:
                    draw_text(self.game.display, "x{} {}".format(it["count"],it["item"]), self.font_size, self.game.font_name,
                        300, 440 + _y, text_align=TEXT_ALIGN.LEFT)
                    _y += 22



    
  