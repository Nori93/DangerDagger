import pygame as pg
from enum import Enum
from game.color import *
from game.text_align import TEXT_ALIGN

class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4

def render_all(display, game_map, fov_map, fov_recompute, entities, message_log, font_name, player, spritesheet,mini_map=False):
    ts = game_map.tile_size

    player_to_mid_x =  (player.x *ts) - (game_map.width/2)
    player_to_mid_y =  (player.y *ts) - (game_map.height/2)

    mini_map_location_x = game_map.width/2
    mini_map_location_y = game_map.height/2

    mini_map_tile_size = 5
    if fov_recompute:
        #main map
        for y in range(game_map.map_height):
            for x in range(game_map.map_width):
                visable = fov_map.fov[y][x]                 
                wall = game_map.tiles[x][y].block_sight
                rect = (
                    (x * ts) - player_to_mid_x,
                    (y * ts) - player_to_mid_y, 
                    ts, ts
                    )
                if visable or (#game_map.tiles[x][y].bottom_mid and game_map.tiles[x][y].bottom_mid.__wall__ and
                  y != game_map.map_height -1 and fov_map.fov[y+1][x]):
                    if wall:                        
                        #pg.draw.rect(display, LIGHT_WALL, rect )
                        if game_map.tiles[x][y].image_name != None:
                            display.blit(spritesheet.get_image_by_name("0_{}".format(game_map.tiles[x][y].image_name),ts,ts),rect)
                       
                    else:                        
                        #pg.draw.rect(display, LIGHT_GROUND, rect )
                        if game_map.tiles[x][y].image_name != None:
                            display.blit(spritesheet.get_image_by_name("0_{}".format(game_map.tiles[x][y].image_name),ts,ts),rect)
                        
                        
                    game_map.tiles[x][y].explored = True
                    
                elif ((x != 0 and x != game_map.map_width-1 and
                    y!= 0 and y != game_map.map_height-1) and
                    (fov_map.fov[y-1][x-1] or fov_map.fov[y-1][x] or fov_map.fov[y-1][x+1] or
                    fov_map.fov[y][x-1] or fov_map.fov[y][x+1] or
                    fov_map.fov[y+1][x-1] or fov_map.fov[y+1][x] or fov_map.fov[y+1][x+1])):
                    if wall:                        
                        #pg.draw.rect(display, LIGHT_WALL, rect )
                        if game_map.tiles[x][y].image_name != None:
                            display.blit(spritesheet.get_image_by_name("2_{}".format(game_map.tiles[x][y].image_name),ts,ts),rect)
                    else:                        
                        #pg.draw.rect(display, ORANGE, rect )
                        if game_map.tiles[x][y].image_name != None:
                            display.blit(spritesheet.get_image_by_name("1_{}".format(game_map.tiles[x][y].image_name),ts,ts),rect)  

                elif game_map.tiles[x][y].explored:
                    if wall:
                        if game_map.tiles[x][y].image_name != None:
                            display.blit(spritesheet.get_image_by_name("2_{}".format(game_map.tiles[x][y].image_name),ts,ts),rect)
                    else:
                        #pg.draw.rect(display, DARK_GROUND, rect )
                        if game_map.tiles[x][y].image_name != None:
                            display.blit(spritesheet.get_image_by_name("2_{}".format(game_map.tiles[x][y].image_name),ts,ts),rect)
        #mini map 
        if mini_map:             
            for y in range(game_map.map_height):                
                for x in range(game_map.map_width):
                    visable = fov_map.fov[y][x]                 
                    wall = game_map.tiles[x][y].block_sight                
                    rect_min = (
                        (x * mini_map_tile_size) + mini_map_location_x,
                        (y * mini_map_tile_size) + mini_map_location_y,
                        mini_map_tile_size,mini_map_tile_size
                    )
                    if wall:
                        if visable or (y != game_map.map_height -1 and fov_map.fov[y+1][x]):
                            pg.draw.rect(display, WHITE, rect_min )
                        elif ((x != 0 and x != game_map.map_width-1 and
                            y!= 0 and y != game_map.map_height-1) and
                            (fov_map.fov[y-1][x-1] or fov_map.fov[y-1][x] or fov_map.fov[y-1][x+1] or
                            fov_map.fov[y][x-1] or fov_map.fov[y][x+1] or
                            fov_map.fov[y+1][x-1] or fov_map.fov[y+1][x] or fov_map.fov[y+1][x+1])):                    
                            pg.draw.rect(display, WHITE, rect_min )
                        elif game_map.tiles[x][y].explored:
                            pg.draw.rect(display, WHITE, rect_min )
                   
                                       
    entities_in_render_order = sorted(entities, key= lambda x: x.render_order.value)


    for entity in entities_in_render_order:
        if fov_map.fov[entity.y][entity.x] or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
            draw_entity(display, entity, ts, spritesheet,
             player_to_mid_x=player_to_mid_x, player_to_mid_y=player_to_mid_y,
             fov = fov_map.fov[entity.y][entity.x])
    
    if mini_map:
        for entity in entities_in_render_order:
            if fov_map.fov[entity.y][entity.x] or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
                draw_entity_mini_map(display, entity, mini_map_tile_size,mini_map_location_x, mini_map_location_y)

    render_bar(display, 50, 20, 200, 30, "HP", player.playable.hp, player.playable.max_hp,
        GREEN, DARK_RED, 14, font_name, half_color = ORANGE, quarter_coler = RED)

    render_bar(display, 50, 5, 200, 15, "EXP", player.level.current_xp, player.level.exprience_to_next_level,
        YELLOW, DARK_RED, 8, font_name,half_color=YELLOW, quarter_coler=YELLOW)

    y= game_map.height - 10
    x = 10
    for message_log in message_log.messages:
        draw_text(display, message_log.text, 15, font_name, x, y, message_log.color, text_align=TEXT_ALIGN.LEFT)
        y+= 20

def draw_entity_mini_map(display, entity,mini_map_size,mini_map_x,mini_map_y):    
    #libtcod.console_set_default_foreground(con, entity.color)
    #libtcod.console_put_char(con, entity.x, entity.y, entity.char,libtcod.BKGND_NONE)
    rect = (
        (entity.x * mini_map_size) + mini_map_x,
        (entity.y * mini_map_size) + mini_map_y, 
        mini_map_size, mini_map_size)      
    pg.draw.rect(display, entity.color, rect ) 
      
def draw_entity(display, entity, tile_size, spritesheet, player_to_mid_x = 0,player_to_mid_y = 0,fov=True):    
    #libtcod.console_set_default_foreground(con, entity.color)
    #libtcod.console_put_char(con, entity.x, entity.y, entity.char,libtcod.BKGND_NONE)
    rect = (
        (entity.x * tile_size) - player_to_mid_x,
        (entity.y * tile_size) - player_to_mid_y, 
        tile_size, tile_size)
    if fov:
        if entity.image_name != None:
            if entity.playable:
                rect = (
                    (entity.x * tile_size) - player_to_mid_x,
                    (entity.y * tile_size) - player_to_mid_y-tile_size, 
                    tile_size, tile_size)
                display.blit(spritesheet.get_image_by_name("0_{}".format(entity.image_name),tile_size,tile_size*2),rect)
            else:
                display.blit(spritesheet.get_image_by_name("0_{}".format(entity.image_name),tile_size,tile_size),rect)        
        else:
            pg.draw.rect(display, entity.color, rect)
    else:
        if entity.image_name != None:
            display.blit(spritesheet.get_image_by_name("2_{}".format(entity.image_name),tile_size,tile_size),rect)
        else:
            pg.draw.rect(display, entity.color, rect)

def draw_text(display, text,  size, font_name, x, y, color=WHITE,text_align=TEXT_ALIGN.CENTER):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if text_align == TEXT_ALIGN.CENTER:
        text_rect.center = (x,y)
    elif text_align == TEXT_ALIGN.LEFT:
        text_rect.midleft = (x, y)
    elif text_align == TEXT_ALIGN.RIGHT:
        text_rect.midright = (x,y)
    display.blit(text_surface,text_rect)
    return text_rect

def draw_panel(display, color, x, y, width, height):
    rect = (x, y, width, height)
    pg.draw.rect(display,color,rect)
    return rect

def render_bar(display, x, y, total_width, height, name, value, maximum, bar_color, back_color,font_size,font_name, half_color = None, quarter_coler= None):
    bar_width = int(float(value / maximum * total_width))
    if half_color == None:
        half_color = bar_color
    if quarter_coler == None:
        quarter_coler == bar_color

    draw_panel(display,back_color, x, y, total_width, height)
    if bar_width > int( total_width / 2 ):
        draw_panel(display, bar_color, x, y, bar_width, height)
    elif bar_width <= int( total_width / 2 ) and bar_width >= int( total_width / 4 ):
        draw_panel(display,half_color, x, y, bar_width, height)
    elif bar_width <= int( total_width / 4 ) and bar_width > 0:
        draw_panel(display, quarter_coler, x, y, bar_width, height) 
    
    
    
    draw_text(display, "{}: {}/{}".format(name, value, maximum),font_size,font_name,int(x+ total_width/2),y+12)