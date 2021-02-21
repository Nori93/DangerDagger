from map_objects.tile import Tile
from map_objects.rectangle import Rect
from random import randint

class GameMap:
    def __init__(self, width, height, tile_size,dungeon_level=1):
        # width and hight in pixels
        self.width = width
        self.height = height

        self.tile_size = tile_size
        # width and hight in tiles
        self.map_width = int(self.width / self.tile_size)
        self.map_height= int(self.height/ self.tile_size)    

        self.tiles = self.initialize_tiles()
        self.unique_id = 0
        self.dungeon_level = dungeon_level
        
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.map_height)] for x in range(self.map_width)]
        return tiles

    def make_map(self,max_rooms, room_min_size, room_max_size, map_width, map_height,
     player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

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

                #self.place_entities(new_room, entities)
                rooms.append(new_room)
                num_rooms += 1
        #stairs_component = Stairs(self.dungeon_level + 1)
        #down_stairs = Entity(center_of_last_room_x, center_of_last_room_y,
        #    '>', libtcod.white, "Stairs", render_order= RenderOrder.STAIRS,
        #    stairs=stairs_component)
        #entities.append(down_stairs)


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