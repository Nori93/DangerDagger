from game.color import *

from components import Equipment, Equippable, Playable, Item, Stairs, Weapon, WEAPON_TYPE
from database import get_transaction, MonstersChances

from map_objects.tile import Tile
from map_objects.rectangle import Rect

from game.entity import Entity
from game.equipment_slots import EQUIPMENT_SLOTS

from game.item_funktion import *
from random import randint
from game.random_utils import random_choice_from_dict ,from_dungeon_level
from game.render_function import RenderOrder

from factories import MonsterFactory

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
        self.monster_factory = MonsterFactory()
        
    def initialize_tiles(self):
        tiles = [[Tile(True,x,y) for y in range(self.map_height)] for x in range(self.map_width)]
        return tiles

    def next_floor(self, player, message_log, max_rooms, room_min_size, room_max_size, map_width, map_height):
        self.dungeon_level += 1
        entities = [player]
        
        self.tiles = self.initialize_tiles()
        self.make_map(max_rooms, room_min_size,room_max_size, player, entities)
          
        player.playable.heal(player.playable.max_hp // 2)

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
                y.clean_neighbors()
        
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y,
            STAIRS, "Stairs", render_order= RenderOrder.STAIRS,
            stairs=stairs_component,image_name = 'flore_stars')
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
        db = get_transaction()
        max_monsers_per_room = from_dungeon_level([[2,1],[3,4],[5,6]],self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1,1],[2,4]],self.dungeon_level)
        number_of_monsters = randint(0, max_monsers_per_room)
        number_of_items = randint(0, max_items_per_room)
        monster_factory = MonsterFactory()
        
        monster_chances = {}
        _monsters = db.query(MonstersChances).filter(MonstersChances.id_dungeon_level <= self.dungeon_level)    
        for _monster in _monsters:
            monster_chances[_monster.monster.monster_name]=_monster.chances
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
                entities.append(monster_factory.create_monster(monster_choice,x,y))

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
           
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)              
                if item_choice == "healing_potion":
                    item_component = Item(use_funtion=heal, amount=3 )
                    item = Entity(x, y, VIOLET, "Healing Potion", render_order=RenderOrder.ITEM, 
                        item=item_component,image_name="potion")
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


            