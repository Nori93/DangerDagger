from os import path
import pickle
import json
import xml.etree.ElementTree as ET
from game.race_enum import RACE
from game.class_enum import CLASS
import pygame as pg

main_dir = ""

ICON = 'icon.png'
SAVE_FILE = "savegame.dat"

ASSETS_DIR = "Assets"
DATA_DIR = "Data"
SPRITES_DIR = 'Sprites'
MAP_DIR = 'Map'

DATA_UI = 'ui_data'

RACES_FILE = 'races.jsonc'
CLASS_FILE = 'classes.jsonc'
NAME_FILE = 'names.jsonc'
NAME_FILE = 'names.jsonc'

def load_icon():
	dir = path.dirname(main_dir)
	return path.join(dir,ASSETS_DIR,SPRITES_DIR,ICON)

def save_game(player, entities, game_map, message_log, game_state):
	data_file = {}
	data_file["player_index"] = entities.index(player)
	data_file["entities"] = entities
	data_file["game_map"] = game_map
	data_file["message_log"] = message_log
	data_file["game_state"] = game_state
	
	pickle.dump(data_file, open(SAVE_FILE, "wb"))
		
		
def load_game():
	if not path.isfile(SAVE_FILE):
		raise FileNotFoundError
		
	data_file = pickle.load(open(SAVE_FILE, "rb"))
	
	player_index = data_file["player_index"]
	entities = data_file["entities"]
	game_map = data_file["game_map"]
	message_log = data_file["message_log"]
	game_state = data_file["game_state"]
	
	player = entities[player_index]
	
	return player, entities, game_map, message_log, game_state


def load_race(type: RACE): 
	dir = path.dirname(main_dir)
	dir = path.join(dir,ASSETS_DIR,DATA_DIR,RACES_FILE)
	with open(dir) as json_file:
		data = json.load(json_file)
		for d in data:
			if d['race'].upper() == str(type.name).replace("_","-"):
				return d


def load_class(type: CLASS): 
	dir = path.dirname(main_dir)
	dir = path.join(dir,ASSETS_DIR,DATA_DIR,CLASS_FILE)
	with open(dir) as json_file:
		data = json.load(json_file)
		for d in data:
			if d['class'].upper() == str(type.name).replace("_","-"):
				return d


def load_name_for_race(type: RACE): 
	dir = path.dirname(main_dir)
	dir = path.join(dir,ASSETS_DIR,DATA_DIR,NAME_FILE)
	with open(dir) as json_file:
		data = json.load(json_file)
		for d in data:
			if d['race'].upper() == str(type.name).replace("_","-"):
				return d


def load_xml(file_name:str):
	dir = path.dirname(main_dir)
	dir = path.join(dir,DATA_UI,file_name)
	tree = ET.parse(dir)
	return tree.getroot()

def load_sprite_sheet_json(file_name:str):
	dir = path.dirname(main_dir)
	dir = path.join(dir, ASSETS_DIR,SPRITES_DIR,MAP_DIR,file_name)
	with open(dir) as json_file:
		data = json.load(json_file)
		return data

def load_sprite_sheet(file_name:str):
	dir = path.dirname(main_dir)
	dir = path.join(dir, ASSETS_DIR,SPRITES_DIR,MAP_DIR,file_name)
	return pg.image.load(dir).convert()