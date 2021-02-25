import pygame as pg
from game_state import GameState

def handle_main_menu():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return {"quit": True}
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                return {"start_key":True}
            if event.key == pg.K_BACKSPACE:
                return {"back_key":True}
            if event.key == pg.K_DOWN:
               return {"down_key":True}
            if event.key == pg.K_UP:
                return {"up_key":True}
            if event.key == pg.K_ESCAPE:
                return {"esc":True}
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                return {"mouse_left":True}
    return {}

def handle_game(game_state):
    if game_state == GameState.PLAYERS_TURN:
        return handle_player_turn_keys()

    return {}

def handle_player_turn_keys():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return {"quit": True}
        if event.type == pg.KEYDOWN:
            #movement keys
            if (event.key == pg.K_UP and event.key == pg.K_LEFT) or event.key == pg.K_q:
                return {"move": (-1,-1)}
            elif (event.key == pg.K_UP and event.key == pg.K_RIGHT) or event.key == pg.K_e:
                return {"move": ( 1,-1)}
            elif (event.key == pg.K_DOWN and event.key == pg.K_LEFT) or event.key == pg.K_z:
                return {"move": (-1, 1)}
            elif (event.key == pg.K_DOWN and event.key == pg.K_RIGHT) or event.key == pg.K_c:
                return {"move": ( 1, 1)}
            elif event.key == pg.K_UP or event.key == pg.K_w:
                return {"move": ( 0,-1)}
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                return {"move": ( 0, 1)}
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                return {"move": (-1, 0)}
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                return {"move": ( 1, 0)}
            if event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT or event.key == pg.K_g:
                return {"pickup": True}
            if event.key == pg.K_i:
                return {"show_inventory": True}
            if event.key == pg.K_h:
                return {"drop_inventory": True}
            if event.key == pg.K_j:
                return {"show_character_screen": True}
            if event.key == pg.K_KP_ENTER and event.key == pg.K_LALT:
                return {"fullscreen": True}
            if event.key == pg.K_KP_ENTER:
                return {'take_stairs': True}
            if event.key == pg.K_ESCAPE:
                return {"exit": True}
    return {}   
    