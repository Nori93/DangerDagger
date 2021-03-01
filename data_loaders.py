from os import path
import pickle
import json
from race_enum import RACE
from class_enum import CLASS

SAVE_FILE = "savegame.dat"


def save_game(player, entities, game_map, message_log, game_state):
	data_file = {}
	data_file["player_index"] = entities.index(player)
	data_file["entities"] = entities
	data_file["game_map"] = game_map
	data_file["message_log"] = message_log
	data_file["game_state"] = game_state
	
	pickle.dump(data_file, open(SAVE_FILE, "wb"))
		
		
def load_game():
	if not os.path.isfile(SAVE_FILE):
		raise FileNotFoundError
		
	data_file = pickle.load(open(SAVE_FILE, "rb"))
	
	player_index = data_file["player_index"]
	entities = data_file["entities"]
	game_map = data_file["game_map"]
	message_log = data_file["message_log"]
	game_state = data_file["game_state"]
	
	player = entities[player_index]
	
	return player, entities, game_map, message_log, game_state

ASSETS_DIR = "Assets"
DATA_DIR = "Data"

RACES_FILE = 'races.jsonc'

def load_race(type: RACE): 
	dir = path.dirname(__file__)
	dir = path.join(dir,ASSETS_DIR,DATA_DIR,RACES_FILE)
	with open(dir) as json_file:
		data = json.load(json_file)
		for d in data:
			if d['race'].upper() == str(type.name).replace("_","-"):
				return d

CLASS_FILE = 'classes.jsonc'

def load_class(type: CLASS): 
	dir = path.dirname(__file__)
	dir = path.join(dir,ASSETS_DIR,DATA_DIR,CLASS_FILE)
	with open(dir) as json_file:
		data = json.load(json_file)
		for d in data:
			if d['class'].upper() == str(type.name).replace("_","-"):
				return d
		