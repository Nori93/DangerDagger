import pygame as pg
import numpy as np
from color import *
from enum import Enum
from input_handlers import handle_main_menu
from render_function import draw_text, draw_panel
from text_align import TEXT_ALIGN
from menus.menu import Menu
from data_loaders import load_race, load_class, load_name_for_race
from race_enum import RACE
from class_enum import CLASS
from random import randint


class CreateCharacterMenu(Menu):
    class STATE(Enum):
        SELECT_RACE = 0
        SELECT_CLASSE = 1
        CHOICE_SET = 2
        ROLL_DICE = 3
        SET_ROLLS = 4
        CHARACTER_DESC = 5

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

        self._set = [
            "First Set",
            "Secend Set"
        ]

        self._stats = [
            "Strenght",
            "Dexterity",
            "Constitution",
            "Intelligence",
            "Wisdom",
            "Charisma"
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

        self.sel_weapon_index = -1
        self.sel_armor_index = -1
        self.sel_items_index = -1

        self.rolls = []

        self.player_name = None

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

            self.display_eq()

            if self.state == CreateCharacterMenu.STATE.SELECT_RACE:
                self.display_race_menu()
            elif self.state == CreateCharacterMenu.STATE.SELECT_CLASSE:
                self.display_class_menu()
            elif self.state == CreateCharacterMenu.STATE.CHOICE_SET:
                self.display_choise_set_menu()
            elif self.state == CreateCharacterMenu.STATE.ROLL_DICE:
                self.display_roll_dices()
            elif self.state == CreateCharacterMenu.STATE.SET_ROLLS:
                self.display_set_roll_menu()
            elif self.state == CreateCharacterMenu.STATE.CHARACTER_DESC:
                self.display_set_name_menu()
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

    def display_eq(self):
        if self.sel_weapon_index != -1:
            weapon_choice = self.loadet_class["equipment"]["weapon_choice"][self.sel_weapon_index] 
            if "main_hand" in weapon_choice and "off_hand" in weapon_choice:
                draw_text(self.game.display,"Main:{},Off:{}".format(weapon_choice["main_hand"],weapon_choice["off_hand"]), self.font_size_low, self.game.font_name,
                    500, 20, text_align=TEXT_ALIGN.LEFT)
            elif "main_hand" in weapon_choice and "off_hand" not in weapon_choice:
                draw_text(self.game.display,"Main:{},Off:{}".format(weapon_choice["main_hand"],"Empty"), self.font_size_low, self.game.font_name,
                    500, 20, text_align=TEXT_ALIGN.LEFT)
            elif "main_hand" not in weapon_choice and "off_hand" in weapon_choice:
                draw_text(self.game.display,"Main:{},Off:{}".format("Empty",weapon_choice["off_hand"]), self.font_size_low, self.game.font_name,
                    500, 20, text_align=TEXT_ALIGN.LEFT)
        
        if self.sel_armor_index != -1:
            armor_choice = self.loadet_class["equipment"]["armor_choice"][self.sel_armor_index]
            draw_text(self.game.display,"Armor:{}".format(armor_choice["armor"]), self.font_size_low, self.game.font_name,
                    500, 40, text_align=TEXT_ALIGN.LEFT)

        if self.sel_items_index != -1:
            draw_text(self.game.display,"Items:", self.font_size_low, self.game.font_name,
            500, 70, text_align=TEXT_ALIGN.LEFT)
            items_choice =  self.loadet_class["equipment"]["items_choice"]
            if "items" in items_choice[self.sel_items_index]:
              
                items_list = []

                for item in items_choice[self.sel_items_index]["items"]:
                    add = True
                    for i in items_list:
                        if i["item"] == item:
                            i["count"] += 1
                            add = False
                            break
                    if add:
                        items_list.append({"item":item,"count":1}) 
                _ya = 20
                for it in items_list:
                    draw_text(self.game.display, "x{} {}".format(it["count"],it["item"]), self.font_size_low, self.game.font_name,
                        500, 70 + _ya, text_align=TEXT_ALIGN.LEFT)
                    _ya += 20

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

       

        if self.option_index != self.loadet_index:
            self.loadet_class = load_class(self._class[self.option_index])
            self.loadet_index = self.option_index
            self.reset_temp_stats()
            

        if self.loadet_class:
            self.display_class_desc()

        if self.act_start_key and self.loadet_class:
            self.selected_class = self._class[self.option_index]
            self.option_index = 0
            self.loadet_index = -1
            if self.multi_weapons or self.multi_armor or self.multi_items:
                self.state = CreateCharacterMenu.STATE.CHOICE_SET
            else:
                if "weapon_choice" in self.loadet_class["equipment"]:
                    self.sel_weapon_index = 0
                if "armor_choice" in self.loadet_class["equipment"] and len(self.loadet_class["equipment"]["armor_choice"]) > 0:
                    self.sel_armor_index = 0
                if "items_choice" in self.loadet_class["equipment"]:
                    self.sel_items_index = 0
                self.state = CreateCharacterMenu.STATE.ROLL_DICE
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
        
        self.multi_weapons = False
        self.multi_armor = False
        self.multi_items = False
        
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
                self.multi_weapons = True
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
                self.multi_armor = True
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
                self.multi_items = True
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

    def display_choise_set_menu(self):
        self.choise_set_option = []
        for i in range(0, len(self._set)):
            self.choise_set_option.append(draw_text(self.game.display, self._set[i], self.font_size, self.game.font_name,
             self.select_panel_x + self.offset_x,
             self.select_panel_y + self.offset_y * i,
             text_align=TEXT_ALIGN.LEFT))
        
        self.set_cur(
            self.choise_set_option[self.option_index].x + 100,
            self.choise_set_option[self.option_index].y + 10,
            )

        if self.multi_armor:
            self.armor_index = self.option_index
        else:
            self.armor_index = 0
        
        if self.multi_weapons:
            self.weapons_index = self.option_index
        else:
            self.weapons_index = 0

        if self.multi_items:
            self.items_index = self.option_index
        else:
            self.items_index = 0

        draw_text(self.game.display,"Weapons:", self.font_size, self.game.font_name,
            300, 260, text_align=TEXT_ALIGN.LEFT)

        if "weapon_choice" in self.loadet_class["equipment"]:  
            weapon_choice = self.loadet_class["equipment"]["weapon_choice"][self.weapons_index]            

            if "main_hand" in weapon_choice and "off_hand" in weapon_choice:
                draw_text(self.game.display,"Main:{},Off:{}".format(weapon_choice["main_hand"],weapon_choice["off_hand"]), self.font_size_low, self.game.font_name,
                    300, 290, text_align=TEXT_ALIGN.LEFT)
            elif "main_hand" in weapon_choice and "off_hand" not in weapon_choice:
                draw_text(self.game.display,"Main:{},Off:{}".format(weapon_choice["main_hand"],"Empty"), self.font_size_low, self.game.font_name,
                    300, 290, text_align=TEXT_ALIGN.LEFT)
            elif "main_hand" not in weapon_choice and "off_hand" in weapon_choice:
                draw_text(self.game.display,"Main:{},Off:{}".format("Empty",weapon_choice["off_hand"]), self.font_size_low, self.game.font_name,
                    300, 290, text_align=TEXT_ALIGN.LEFT)
        

        draw_text(self.game.display,"Equipment:", self.font_size, self.game.font_name,
            300, 320, text_align=TEXT_ALIGN.LEFT)
        
        if "armor_choice" in self.loadet_class["equipment"] and  len(self.loadet_class["equipment"]["armor_choice"]) > 0:
            armor_choice = self.loadet_class["equipment"]["armor_choice"][self.armor_index]

            draw_text(self.game.display,"Armor:{}".format(armor_choice["armor"]), self.font_size_low, self.game.font_name,
                    300, 340, text_align=TEXT_ALIGN.LEFT)

        draw_text(self.game.display, "Items:", self.font_size, self.game.font_name,
            300, 370, text_align=TEXT_ALIGN.LEFT)

        if "items_choice" in self.loadet_class["equipment"]:  
            items_choice =  self.loadet_class["equipment"]["items_choice"]
            if "items" in items_choice[self.items_index]:
              
                items_list = []

                for item in items_choice[self.items_index]["items"]:
                    add = True
                    for i in items_list:
                        if i["item"] == item:
                            i["count"] += 1
                            add = False
                            break
                    if add:
                        items_list.append({"item":item,"count":1}) 
                _ya = 20
                for it in items_list:
                    draw_text(self.game.display, "x{} {}".format(it["count"],it["item"]), self.font_size, self.game.font_name,
                        300, 370 + _ya, text_align=TEXT_ALIGN.LEFT)
                    _ya += 20
        
        if self.act_start_key:
            if "weapon_choice" in self.loadet_class["equipment"]:
                self.sel_weapon_index = self.weapons_index
            if "armor_choice" in self.loadet_class["equipment"] and len(self.loadet_class["equipment"]["armor_choice"]) > 0:
                self.sel_armor_index = self.armor_index
            if "items_choice" in self.loadet_class["equipment"]:
                self.sel_items_index = self.items_index
            self.state = CreateCharacterMenu.STATE.ROLL_DICE


        self.move_cursor(self._set)
        self.draw_cursor()
    

    def display_roll_dices(self):
        
        if self.act_start_key:
            if len(self.rolls) < 6:
                row = [4]
                for i in  range(0,3):
                    row.append(randint(1, 6))          
                self.rolls.append(row)
            else:
                self.state = CreateCharacterMenu.STATE.SET_ROLLS
                self.loadet_index = 0
                self.option_index = 0
                #self.sort_rolls()
                

        if len(self.rolls) < 6:
            draw_text(self.game.display, "press enter to roll.", self.font_size, self.game.font_name,
                    self.game.width/2, self.game.height - 20, text_align=TEXT_ALIGN.CENTER)
        else:
            draw_text(self.game.display, "press enter set stats.", self.font_size, self.game.font_name,
                self.game.width/2, self.game.height - 20, text_align=TEXT_ALIGN.CENTER)

        _y = 0   
        for row in self.rolls:
            draw_text(self.game.display,
                "({} + {} + {} + {})max 3 = {}".format(
                    row[0],row[1],row[2],row[3],self.max_roll_sum(row) 
                ),
                25, self.game.font_name,
                self.game.width/2, 340 + _y, text_align=TEXT_ALIGN.CENTER)
            _y += 40

    def max_roll_sum(self,rolls):
        arr = np.array(rolls)
        sorted_index_array = np.argsort(arr)
        sorted_array = arr[sorted_index_array]
        return sum(sorted_array[-3: ])
    
    def sort_rolls(self):
        arr = np.array(self.rolls)
        sorted_index_array = np.argsort(arr)
        sorted_array = arr[sorted_index_array]
        self.rolls = sorted_array[-6: ]

    def display_set_roll_menu(self):
        self.set_roll_option = []
        for i in range(0, len(self._stats)):
            self.set_roll_option.append(draw_text(self.game.display, self._stats[i], self.font_size, self.game.font_name,
             self.select_panel_x + self.offset_x,
             self.select_panel_y + self.offset_y * i,
             text_align=TEXT_ALIGN.LEFT))
        
        self.set_cur(
            self.set_roll_option[self.option_index].x + 100,
            self.set_roll_option[self.option_index].y + 10,offset_r= 150
            )

        _y = 0   
        for idx,row in enumerate(self.rolls):
            if idx == self.loadet_index:
                draw_text(self.game.display,
                    "({} + {} + {} + {})max 3 =[{}]".format(
                        row[0],row[1],row[2],row[3],self.max_roll_sum(row) 
                    ),
                    25, self.game.font_name,
                    self.game.width/2+ 100, 300 + _y, text_align=TEXT_ALIGN.CENTER)
            else:
                draw_text(self.game.display,
                    "({} + {} + {} + {})max 3 = {}".format(
                        row[0],row[1],row[2],row[3],self.max_roll_sum(row) 
                    ),
                    25, self.game.font_name,
                    self.game.width/2 + 100, 300 + _y, text_align=TEXT_ALIGN.CENTER)
            _y += 40
        
        if self.act_start_key:
            if self.option_index == 0 and self.t_strenght == 0:
                self.t_strenght = self.max_roll_sum(self.rolls[self.loadet_index])
                self.loadet_index +=1
            if self.option_index == 1 and self.t_dexterity == 0:
                self.t_dexterity = self.max_roll_sum(self.rolls[self.loadet_index])
                self.loadet_index +=1
            if self.option_index == 2 and self.t_constitution == 0:
                self.t_constitution = self.max_roll_sum(self.rolls[self.loadet_index])
                self.loadet_index +=1
            if self.option_index == 3 and self.t_intelligence == 0:
                self.t_intelligence = self.max_roll_sum(self.rolls[self.loadet_index])
                self.loadet_index +=1
            if self.option_index == 4 and self.t_wisdom == 0:
                self.t_wisdom = self.max_roll_sum(self.rolls[self.loadet_index])
                self.loadet_index +=1
            if self.option_index == 5 and self.t_charisma == 0:
                self.t_charisma = self.max_roll_sum(self.rolls[self.loadet_index])
                self.loadet_index +=1
            if  self.loadet_index  < 6:
                pass
            else:
                self.state = CreateCharacterMenu.STATE.CHARACTER_DESC
                self.strenght +=self.t_strenght
                self.dexterity +=self.t_dexterity
                self.constitution +=self.t_constitution
                self.intelligence +=self.t_intelligence
                self.wisdom += self.t_wisdom
                self.charisma += self.t_charisma
                self.reset_temp_stats()
                self.option_index = 0
                self.loadet_index = 0



        self.move_cursor(self._stats)
        self.draw_cursor()
    
    def display_set_name_menu(self):
        self._names = load_name_for_race(self.selected_race)
        self.set_name_option = []
        for i,name in enumerate(self._names["names"]):
            self.set_name_option.append(draw_text(self.game.display, name, self.font_size, self.game.font_name,
             self.select_panel_x + self.offset_x,
             self.select_panel_y + self.offset_y * i,
             text_align=TEXT_ALIGN.LEFT))
        
        self.set_cur(
            self.set_name_option[self.option_index].x + 100,
            self.set_name_option[self.option_index].y + 10,offset_r= 430
            )

        if self.act_start_key:
            self.set_game_player()
            self.run_display = False
            self.game.playing = True
            self.game.new_game = True

        self.move_cursor(self._names["names"])
        self.draw_cursor()

    def set_game_player(self):
        player_name = self._names["names"][self.option_index]
       

        w_main, w_off, armor_choice, w_choise, items_choice = None, None, None, None, None
        
        if self.sel_weapon_index != -1:
            w_choise = self.loadet_class["equipment"]["weapon_choice"][self.sel_weapon_index]
            if "main_hand" in w_choise:
                w_main = w_choise["main_hand"]
            
            if "off_hand" in w_choise:
                w_off = w_choise["off_hand"]
        
        if self.sel_armor_index != -1:
            armor_choice = self.loadet_class["equipment"]["armor_choice"][self.sel_armor_index]
        
        if self.sel_items_index != -1:
            items_choice =  self.loadet_class["equipment"]["items_choice"][self.sel_items_index]
        
        self.game.set_player(
            name=player_name,
            weapon_main=w_main,
            weapon_off=w_off,
            armor= armor_choice,
            items= items_choice,
            race= self.loadet_race,
            class_name= self.loadet_class['class'],
            strenght = self.strenght,
            dexterity = self.dexterity,
            constitution = self.constitution,
            intelligence = self.intelligence,
            wisdom = self.wisdom,
            charisma = self.charisma,
            )