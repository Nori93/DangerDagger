import pygame as pg
from enum import Enum
from color import *


class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4

def render_all(display,game_map,fov_map,fov_recompute,entities):
    ts = game_map.tile_size
    if fov_recompute:
        for y in range(game_map.map_height):
            for x in range(game_map.map_width):
                visable = fov_map.fov[y][x]                 
                wall = game_map.tiles[x][y].block_sight
                rect = (x * ts, y * ts, ts, ts)                
                if visable:
                    if wall:
                        #libtcod.console_set_char_background(con, x, y, colors.get("light_wall"), libtcod.BKGND_SET)
                        pg.draw.rect(display, LIGHT_WALL, rect )
                    else:
                        #libtcod.console_set_char_background(con, x, y, colors.get("light_ground"), libtcod.BKGND_SET)
                        pg.draw.rect(display, LIGHT_GROUND, rect )
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        pg.draw.rect(display, DARK_WALL, rect )
                    else:
                        pg.draw.rect(display, DARK_GROUND, rect )
                

    for entity in entities:
        draw_entity(display, entity, ts)

def draw_entity(display, entity, tile_size):    
    #libtcod.console_set_default_foreground(con, entity.color)
    #libtcod.console_put_char(con, entity.x, entity.y, entity.char,libtcod.BKGND_NONE)
    rect = (entity.x * tile_size, entity.y * tile_size, tile_size, tile_size)     
    pg.draw.rect(display, entity.color, rect )