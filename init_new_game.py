
from color import *
from entity import Entity
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from components.equippable import Equippable
from map_objects.game_map import GameMap
from render_function import RenderOrder
from game_state import GameState
from equipment_slots import EquipmentSlots

def get_game_variables(game):
    fighter_component = Fighter(hp=100, defense=1, power=2)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(int(game.width/2), int(game.height /2),WHITE, "Player", blocks=True, 
        render_order=RenderOrder.ACTOR, fighter = fighter_component,
        inventory=inventory_component,  level=level_component,
        equipment=equipment_component)

    entities = [player]

    equippable_component = Equippable(EquipmentSlots.WEAPONS, power_bonus=2)
    dagger = Entity(0,0, SKY, "Dagger",equippable= equippable_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip_main_hand(dagger)

    
    game_map = GameMap(game.width, game.height, game.tile_size)
    game_map.make_map(game.max_room,game.room_min_size,game.room_max_size,game.map_width,game.map_height,player,entities)
    game_state = GameState.PLAYERS_TURN

    return player, entities, game_map, game_state