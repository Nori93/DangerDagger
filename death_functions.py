import tcod as libtcod
from game_state import GameState
from render_function import RenderOrder
from game_message import Message

def kill_player(player):  
    player.color = libtcod.dark_red
    return Message("You died!",libtcod.red), GameState.PLAYER_DEAD

def kill_monster(monster):
    death_message = Message("{} is dead!".format(monster.name.capitalize()), libtcod.orange)
   
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.playable = None
    monster.ai = None
    monster.name = "remains of " + monster.name
    monster.render_order = RenderOrder.CORPSE
    monster.image_name = 'dead'

    return death_message