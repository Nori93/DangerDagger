from random import randint
class Tile:
    def __init__(self, blocked, x, y, block_sight=None):
        self.blocked = blocked
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = False

        self.x = x
        self.y = y
       
        self.top_left = None
        self.top_mid = None
        self.top_right = None

        self.mid_left = None
        self.mid_mid = None
        self.mid_right = None

        self.bottom_left = None
        self.bottom_mid = None
        self.bottom_right = None

        self.tile_id = None


    def set_tile_index(tiles):
        if self.x != 0 and self.y != 0:
            pass