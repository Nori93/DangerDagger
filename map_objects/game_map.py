from color import *
from components.ai import BasicMonster
from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs
from components.weapon import Weapon,WEAPON_TYPE

from map_objects.tile import Tile
from map_objects.rectangle import Rect

from entity import Entity
from equipment_slots import EQUIPMENT_SLOTS

from item_funktion import *
from random import randint
from random_utils import random_choice_from_dict ,from_dungeon_level
from render_function import RenderOrder

class GameMap:
    def __init__(self, width, height, tile_size,dungeon_level=1):
        # width and hight in pixels
        self.width = width
        self.height = height

        self.tile_size = tile_size
        # width and hight in tiles
        self.map_width = int(self.width/10)
        self.map_height= int(self.height/10)    

        self.tiles = self.initialize_tiles()
        self.unique_id = 0
        self.dungeon_level = dungeon_level
        
    def initialize_tiles(self):
        tiles = [[Tile(True,x,y) for y in range(self.map_height)] for x in range(self.map_width)]
        return tiles

    def next_floor(self, player, message_log, max_rooms, room_min_size, room_max_size, map_width, map_height):
        self.dungeon_level += 1
        entities = [player]
        
        self.tiles = self.initialize_tiles()
        self.make_map(max_rooms, room_min_size,room_max_size, player, entities)
          
        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message("You take a moment to rest, and rocover your strength.", 
            libtcod.light_violet))
        
        return entities

    def make_map(self,max_rooms, room_min_size, room_max_size,
     player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, self.map_width - w - 1)
            y = randint(0, self.map_height - h - 1)

            new_room = Rect(x, y, w, h)
            
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                #did not break, means no intersect
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x , prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)
                rooms.append(new_room)
                num_rooms += 1

        for x in self.tiles:
            for y in x:
                y.check_neighbors(self.tiles)
        
        for x in self.tiles:
            for y in x:
                y.set_wall_type()
        
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y,
            STAIRS, "Stairs", render_order= RenderOrder.STAIRS,
            stairs=stairs_component)
        entities.append(down_stairs)


    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel (self, x1,x2, y):
        for x in range(min(x1, x2), max(x1,x2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
    
    def create_v_tunnel (self, y1,y2, x):
        for y in range(min(y1, y2), max(y1,y2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

     
    def place_entities(self, room, entities):
        max_monsers_per_room = from_dungeon_level([[2,1],[3,4],[5,6]],self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1,1],[2,4]],self.dungeon_level)
        number_of_monsters = randint(0, max_monsers_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {
            "orc": 80,
            "troll": from_dungeon_level([[15,3],[30,5],[60,7]],self.dungeon_level)
            }
        item_chances = {
            "healing_potion":70,
            "lightinh_scroll":from_dungeon_level([[25,4]],self.dungeon_level),
            "fireball_scroll":from_dungeon_level([[25,6]],self.dungeon_level),
            "confusion_scroll":from_dungeon_level([[26,2]],self.dungeon_level),
            "sword":from_dungeon_level([[5,4]],self.dungeon_level),
            "shield":from_dungeon_level([[15,8]],self.dungeon_level)
            }

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
                if monster_choice == "orc":
                    ai_component = BasicMonster()
                    fighter_component = Fighter(hp=20, defense =0, power=4, xp=35)
                    monster = Entity(x, y, DESATURED_GREEN,"Orc_" + str(self.unique_id), blocks=True,
                    render_order = RenderOrder.ACTOR ,fighter = fighter_component, ai = ai_component)
                else:
                    ai_component = BasicMonster()
                    fighter_component = Fighter(hp=30, defense =2, power=8, xp=100)
                    monster = Entity(x, y, DESATURED_BROWN,"Troll_" + str(self.unique_id), blocks=True,
                    render_order = RenderOrder.ACTOR ,fighter = fighter_component, ai = ai_component)
                
                entities.append(monster)
                self.unique_id +=1

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
           
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)              
                if item_choice == "healing_potion":
                    item_component = Item(use_funtion=heal, amount=40 )
                    item = Entity(x, y, VIOLET, "Healing Potion", render_order=RenderOrder.ITEM, 
                        item=item_component)
                elif item_choice == "fireball_scroll":
                    item_component = Item(use_funtion=cast_fireball, targeting=True,
                     targeting_message=Message("Left-click a target tile for the fireball, or right-click to cancel", libtcod.light_cyan),
                     damage=25, radius=3)
                    item = Entity(x, y,  RED, "Fireball Scroll", render_order=RenderOrder.ITEM, 
                        item=item_component)
                elif item_choice == "confusion_scroll":
                    item_component = Item(use_funtion=cast_confuse, targeting=True,
                     targeting_message=Message("Left-click an enemy to confuse it, or right-click to cancel", libtcod.light_cyan),
                     damage=25, radius=3)
                    item = Entity(x, y, ORANGE, "Confuion Scroll", render_order=RenderOrder.ITEM, 
                        item=item_component)
                elif item_choice == "sword":
                    equippable_component = Equippable(EQUIPMENT_SLOTS.WEAPONS, power_bonus=3)
                    weapon_component = Weapon(3, 5, 20, WEAPON_TYPE.SHORTSWORD)
                    item = Entity(x, y, SKY, "Sword", render_order=RenderOrder.ITEM, 
                        equippable=equippable_component,weapon= weapon_component)
                elif item_choice == "shield":
                    equippable_component = Equippable(EQUIPMENT_SLOTS.WEAPONS, defense_bonus=1)
                    weapon_component = Weapon(0, 1,50, WEAPON_TYPE.SHIELD)
                    item = Entity(x, y, ORANGE, "Shield", render_order=RenderOrder.ITEM, 
                        equippable=equippable_component, weapon= weapon_component)
                else:
                    item_component = Item(use_funtion=cast_lightning, damage=20, maximum_range=5)
                    item = Entity(x, y, YELLOW, "Lightning Scroll", render_order=RenderOrder.ITEM, 
                        item=item_component)

                entities.append(item)


            