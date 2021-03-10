
from color import *
from entity import Entity
from components.playable import Playable
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from components.equippable import Equippable
from components.weapon import Weapon, WEAPON_TYPE
from map_objects.game_map import GameMap
from render_function import RenderOrder
from game_state import GameState
from equipment_slots import EQUIPMENT_SLOTS
from game_message import MessageLog

def get_game_variables(game):
    player = game.temp_player
    entities = [player]
    game_map = GameMap(game.width, game.height, game.tile_size)
    game_map.make_map(game.max_room,game.room_min_size,game.room_max_size,player,entities)
    message_log = MessageLog(game.message_x, game.message_width, game.message_height)
    game_state = GameState.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state, 