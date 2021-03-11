import pygame as pg

from game.settings import Settings
from game.color import *
from menus import *
from components import *
from factories import WeaponFactory
from game.equipment_slots import EQUIPMENT_SLOTS
from game.entity import Entity
from game.init_new_game import get_game_variables
from game.render_function import render_all
from game.death_functions import *
from game.game_state import GameState
from game.input_handlers import handle_game, handle_mouse
from game.fov_functions import intialize_fov, recompute_fov
from game.data_loaders import main_dir, load_icon, save_game, load_game, load_race
from game.race_enum import RACE
from game.text_align import TEXT_ALIGN
from database import *


from map_objects.sprite_sheet import SpriteSheet

class Game:   

    def __init__(self,dir):
        main_dir = dir
        #Get the standard settings
        self.settings = Settings()
        
        self.clock = pg.time.Clock()
        self.FPS = self.settings.get["FPS"]

        self.width = self.settings.get["screen_width"]
        self.height = self.settings.get["screen_height"]


        self.tile_size = self.settings.get["tile_size"]
        self.map_width = int(self.width  / 10)
        self.map_height= int(self.height / 10)  

        self.message_x = self.settings.get["message_x"]
        self.message_width = self.settings.get["message_width"]
        self.message_height = self.settings.get["message_height"]

        # get title from settings
        self.title = self.settings.get["window_title"]



        self.fov_radius = self.settings.get["fov_radius"]
        self.fov_algorithm = self.settings.get["fov_algorithm"]
        self.fov_light_walls = self.settings.get["fov_light_walls"]

        #initalize game window.
        pg.init()
        #initalize game sounds
        pg.mixer.init()
        self.display = pg.Surface((self.width, self.height + 100))
        icon_path = load_icon()
        self.icon = pg.image.load(icon_path)
        pg.display.set_icon(self.icon)
        #set screen 
        self.window = pg.display.set_mode((self.width, self.height + 100))
        #set title of game
        pg.display.set_caption(self.title)
        #set clock for FPS
        self.clock = pg.time.Clock()
        #set Main Bool if is Game running
        self.running = True
        self.playing = False
        #find font in the client computer
        self.font_name = self.settings.get["font"]
        
        self.max_room = self.settings.get["max_room"]
        self.room_min_size = self.settings.get["room_min_size"]
        self.room_max_size = self.settings.get["room_max_size"]
        

        self.load_data()

        #Main Manu
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)       
        self.create_char = CreateCharacterMenu(self) 
        self.curr_menu = self.main_menu
        #Sub Menu
        self.inventory = InventoryMenu(self)
        self.sub_menu = None
        self.pauze_menu = PauzeMenu(self)

        #NewGame or Load Game
        self.new_game = False
        self.load_game = False
        self.error = False

        self.temp_player = None
        self.config = {}

        self.sprite_sheet = SpriteSheet('TILE_SPRITE_SHEAT')
        self.show_mini_map = False

        self.weapon_factory = WeaponFactory()

    def set_player(
        self, 
        name="Player",
        weapon_main=None,
        weapon_off=None,
        armor=None, 
        items=None,
        race=None,
        class_name=None,
        strenght=None,
        dexterity=None,
        constitution=None,
        intelligence=None,
        wisdom=None,
        charisma=None
        ):
        db = get_transaction()

        db.query()
        ability_component = Ability(
            strenght=strenght,
            dexterity=dexterity,
            constitution=constitution,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma
        )

        hit_points = 1
        armor_class = 1
        preficientcies_component = None

        if class_name != None:
            _class:Classes = db.query(Classes).filter(Classes.class_name == class_name).one()
            hit_points = 8 + ability_component.modifaier_constitution 
            preficientcies_component = Preficiencies(weapons =_class.preficiencies_weapons)

        if armor != None: 
            _armor = db.query(Armors).filter(Armors.armor_name == armor).one()
            armor_class = _armor.armor_class + (ability_component.dexterity * _armor.dex_modifier)
              
        
        
        playable_component = Playable(hp=hit_points, ac=armor_class, xp=0)
        inventory_component = Inventory(26)
        level_component = Level()
        equipment_component = Equipment()
        self.temp_player = Entity(int(self.width/2), int(self.height /2),BLUE, name, blocks=True, 
            render_order=RenderOrder.ACTOR, playable = playable_component,
            inventory=inventory_component,  level=level_component,
            equipment=equipment_component,
            ability=ability_component,
            preficiencies= preficientcies_component,
            image_name="player_left",class_name=class_name,race_name=race)
     
        if weapon_main:
            w_main = db.query(Weapons).filter(Weapons.weapon_name == weapon_main).one()
            item = self.weapon_factory.create_weapon(w_main)
            self.temp_player.inventory.add_item(item)
            self.temp_player.equipment.toggle_equip_main_hand(item)

        if weapon_off:
            w_off = db.query(Weapons).filter(Weapons.weapon_name == weapon_off).one()
            item = self.weapon_factory.create_weapon(w_main)
            self.temp_player.inventory.add_item(item)
            self.temp_player.equipment.toggle_equip_off_hand(item)
    
        #For Making Level memu
        self.temp_player.level.add_xp(340)
    

    def load_data(self):
        pass
    
    def handle_game_keys(self):
        action = handle_game(self.game_state)
        mouse_action = handle_mouse()
        self.act_move = action.get("move")
        self.act_pickup = action.get("pickup")
        self.act_show_inv = action.get("show_inventory")
        self.act_drop_inv = action.get("drop_inventory")
        self.act_char_scr = action.get("show_character_screen")
        self.act_full = action.get("fullscreen")
        self.act_stairs = action.get("take_stairs")
        self.act_exit = action.get("exit")
        self.act_level_up = action.get("level_up")
        self.act_quit = action.get("quit")
        self.act_mini_map = action.get("mini_map")
       

        self.act_left_click = mouse_action.get("left_click")
        self.act_right_click = mouse_action.get("right_click")

    def save_game(self):
        save_game(self.player, self.entities,self.game_map, self.message_log, self.game_state)

    def start_new_game(self):
        self.player, self.entities, self.game_map, self.message_log, self.game_state = get_game_variables(self)
        self.fov_map = intialize_fov(self.game_map)
        self.display.fill(BLACK)

    def load_last_game(self):
        self.player, self.entities, self.game_map, self.message_log, self.game_state = load_game()
        self.fov_map = intialize_fov(self.game_map)
        self.display.fill(BLACK)

    def game_loop(self):
        self.player = None
        self.entities = []
        self.game_map = None
        self.message_log = None
        self.game_state = None
    
        if self.new_game:
           self.start_new_game()
        elif self.load_game:
            try:
                self.load_last_game()
            except:
                self.error = True
                self.load_message = "Save file not found"
                return
        
        self.previous_game_state = self.game_state
        self.player_turn_result =  []
                
        self.fov_recompute = True

        self.targeting_item = None

        while self.playing:
            if self.fov_recompute:
                recompute_fov(self.fov_map, self.player.x, self.player.y, self.fov_radius,
                    self.fov_light_walls, self.fov_algorithm)

            self.handle_game_keys()
            self.player_turn_results =  []

            if self.act_level_up:
                pass
                
            if self.act_quit:
                
                self.playing , self.running = False, False

            if self.act_exit:
                #Pause Menu
                #TODO: Pause Menu with save, load,exit , newgame, options,
                # In future some nice illustration of flors and starrs 
                self.pauze_menu.display_menu()
            
            if self.act_mini_map:
                self.show_mini_map = not self.show_mini_map

            if self.act_stairs and self.game_state == GameState.PLAYERS_TURN:
                #Taking stairs to lower level of dunguan 
                self.taking_stairs()                

            if self.act_move and self.game_state == GameState.PLAYERS_TURN:
                #Make a move
                self.move()
                #Give Ai a move
                self.game_state = GameState.ENEMY_TURN
            
            if self.act_pickup:
                #PickUp staff
                self.pickup()

            if self.act_show_inv:
                inventory_results = self.inventory.display_menu()
                if inventory_results != None:
                    self.player_turn_results.extend(inventory_results)

            if self.game_state == GameState.TARGETING:
                self.targeting_stage()
            
            if self.game_state == GameState.LEVEL_UP:
                #Check if need a menu or message player about something                
                db = get_transaction()
                
                level_ups = db.query(LevelUps).join(Classes,LevelUps.classes).filter(
                    Classes.class_name == self.player.class_name)
                for level_up in level_ups:
                    if level_up.level == self.player.level.current_level:
                        if level_up.proficiency_bonus:
                            self.player.level.proficiency_bonus += 1
                        if level_up.id_spells != None:
                            #add spell to spellbook of player
                            pass
                        if level_up.id_class_ability != None:
                            #add class ability to player
                            pass
                        if level_up.ability_increase:
                            #Show levelUp menu
                            pass
                
                self.game_state = GameState.PLAYERS_TURN

            if self.player_turn_results:
                self.handling_player_turn_result()
            
            self.display.fill(BLACK)
            render_all(self.display,self.game_map,self.fov_map,self.fov_recompute,self.entities,
            self.message_log,self.font_name,self.player,self.sprite_sheet,mini_map=self.show_mini_map)           
            self.window.blit(self.display, (0, 0))
            pg.display.update()

            if self.game_state == GameState.ENEMY_TURN:
                self.enemy_move()

    def taking_stairs(self):
        for entity in self.entities:
            if entity.stairs and entity.x == self.player.x and entity.y == self.player.y:
                self.entities = self.game_map.next_floor(self.player,self.message_log,self.max_room, self.room_min_size,
                     self.room_max_size, self.map_width, self.map_height)
                self.fov_map = intialize_fov(self.game_map)
                self.fov_recompute = True,
                self.display.fill(BLACK)
                    
                break
            else:
                self.message_log.add_message(Message("The are no stairs here.", libtcod.yellow))
    def targeting_stage(self):
        if self.act_left_click:
                target_x, target_y = self.act_left_click

                item_use_results = self.player.inventory.use(
                    self.targeting_item,
                    entities = self.entities,
                    fov_map = self.fov_map,
                    target_x = target_x, target_y = target_y
                )

                self.player_turn_results.extend(item_use_results)
        elif self.act_right_click:
            self.player_turn_results.append({"targeting_cancelled":True})

    def handling_player_turn_result(self):
        for player_turn_result in self.player_turn_results:
            message = player_turn_result.get("message")
            dead_entity = player_turn_result.get("dead")
            item_added = player_turn_result.get("item_added")
            item_component = player_turn_result.get("consumed")
            item_dropped = player_turn_result.get("item_dropped")
            equip = player_turn_result.get("equip")
            targeting = player_turn_result.get("targeting")
            targeting_cancelled = player_turn_result.get("targeting_canceled")
            xp = player_turn_result.get("xp")
            if message:
                self.message_log.add_message(message)
            if dead_entity:
                if dead_entity == self.player:
                    message , self.game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)
                self.message_log.add_message(message)
            if item_added:
                self.entities.remove(item_added)
                self.game_state = GameState.ENEMY_TURN
            if item_component:
                self.game_state = GameState.ENEMY_TURN
            if item_dropped:
                self.entities.append(item_dropped)
                self.game_state = GameState.ENEMY_TURN
            if equip:
                equip_results = self.player.equipment.toggle_equip(equip)
                for equip_result in  equip_results:
                    equipped = equip_result.get("equipped")
                    dequipped = equip_result.get("dequipped")
                    
                    if equipped:
                        self.message_log.add_message(Message("You equipped the {}".format(equipped.name)))
                    if dequipped:
                        self.message_log.add_message(Message("You dequipped the {}".format(dequipped.name)))
                self.game_state = GameState.ENEMY_TURN
            if targeting:
                self.previous_game_state = GameState.PLAYERS_TURN
                self.game_state = GameState.TARGETING
                targeting_item = targeting
                self.message_log.add_message(targeting_item.item.targeting_message)
            if targeting_cancelled:
                self.game_state = self.previous_game_state
                self.message_log.add_message(Message("Targeting cancelled"))
            if xp:
                leveled_up =self.player.level.add_xp(xp)
                self.message_log.add_message(Message("You gain {} experience points.".format(xp), WHITE))
                if leveled_up:
                    self.message_log.add_message(Message(
                        "You battle skills grow stronger! You reached level {}.".format(
                        self.player.level.current_level),YELLOW))
                    self.previous_game_state = self.game_state
                    self.game_state = GameState.LEVEL_UP
    
    def pickup(self):
        for entity in self.entities:
            if entity.item and entity.x == self.player.x and entity.y == self.player.y:
                pickup_results = self.player.inventory.add_item(entity)
                self.player_turn_results.extend(pickup_results)
                break
        else:
            self.message_log.add_message(Message("There is nothing here to pick up.", YELLOW))

           
    def enemy_move(self):
        for entity in self.entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(self.player, self.fov_map, self.game_map, self.entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get("message")
                        dead_entity = enemy_turn_result.get("dead")

                        if message:
                            self.message_log.add_message(message)
                        if dead_entity:
                            if dead_entity == self.player:
                                message , self.game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)
                            self.message_log .add_message(message)
                        if self.game_state == GameState.PLAYER_DEAD:
                            break
                    if self.game_state == GameState.PLAYER_DEAD:
                        break
        else:
            self.game_state = GameState.PLAYERS_TURN
    def move(self):
        dx,dy = self.act_move
        destination_x = self.player.x + dx
        destination_y = self.player.y + dy
        
        if not self.game_map.is_blocked(destination_x,destination_y):
            target = self.player.get_blocking_entities_at_location(self.entities, destination_x, destination_y)
            if target:
                attack_results = self.player.playable.attack(target)
                self.player_turn_results.extend(attack_results)                
            else:
                self.fov_recompute = True
                self.player.move(dx,dy)