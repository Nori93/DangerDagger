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
        self.image_name = None
        self.wall = False
        self.flore = False

    '''
    Round 1
    [top_left(x-1,y-1)]    [top_min(x,y-1)]    [top_right(x-1,y+1)]
    [mid_left(x,y-1)]      [mid_mid(x,y)]      [mid_right(x,y+1)]
    [bottom_left(x+1,y-1)] [bottom_mid(x+1,y)] [bottom_right(x+1,y+1)]
    '''
    
    '''
    Round 2
    [top_left(x-1,y+1)]    [top_min(x,y+1)]    [top_right(x+1,y+1)]
    [mid_left(x-1,y)]      [mid_mid(x,y)]      [mid_right(x+1,y)]
    [bottom_left(x-1,y-1)] [bottom_mid(x,y-1)] [bottom_right(x+1,y-1)]
    '''

    '''
    Round 3
    [top_left(x-1,y-1)]    [top_min(x,y-1)]    [top_right(x+1,y-1)]
    [mid_left(x-1,y)]      [mid_mid(x,y)]      [mid_right(x+1,y)]
    [bottom_left(x-1,y+1)] [bottom_mid(x,y+1)] [bottom_right(x+1,y+1)]
    '''

    def check_neighbors(self,tiles):
        #Top Row
        if self.y != 0 and self.x != 0:
            self.top_left = tiles[self.x - 1][self.y - 1]

        if self.y != 0:
            self.top_mid = tiles[self.x][self.y-1]

        if self.y != 0 and self.x != (len(tiles) - 1):
            self.top_right = tiles[self.x + 1][self.y - 1]
        #Mid Row
        if self.x != 0:
            self.mid_left = tiles[self.x-1][self.y]    
       
        self.mid_mid = self
       
        if self.x != (len(tiles) - 1):
            self.mid_right = tiles[self.x+1][self.y
            ]
        #Bottom Row
        if self.y != (len(tiles[self.x])-1) and self.x != 0:
            self.bottom_left = tiles[self.x - 1][self.y + 1]
        if self.y != (len(tiles[self.x])-1):
            self.bottom_mid = tiles[self.x][self.y+1]
        if self.y != (len(tiles[self.x])-1) and self.x != (len(tiles) - 1) :
            self.bottom_right = tiles[self.x + 1][self.y + 1]

    @property
    def __wall__(self):
        if self.wall:
            return True
        elif ((self.top_left and self.top_left.block_sight == False) or  
            (self.top_mid and self.top_mid.block_sight == False) or 
            (self.top_right and self.top_right.block_sight == False) or
            (self.mid_left and self.mid_left.block_sight == False) or 
            (self.mid_right and self.mid_right.block_sight == False) or
            (self.bottom_left and self.bottom_left.block_sight == False) or 
            (self.bottom_mid and self.bottom_mid.block_sight == False) or 
            (self.bottom_right and self.bottom_right.block_sight == False)) and self.block_sight == True:
            return True
        elif self.block_sight == False:
            return False
        else:
            return None 
    
    
    def set_wall_type(self):
        if self.__wall__:
            self.wall = True
            # Corner
            if (self.bottom_right and self.bottom_right.__wall__ == False and 
                self.bottom_mid and self.bottom_mid.__wall__ == True and 
                self.mid_right and self.mid_right.__wall__ == True):
                if self.top_mid:
                    if self.top_mid.__wall__ == False:
                       self.top_mid.image_name = self.bind_flore()
                    else:
                        self.top_mid.image_name = 'wall_corner_right_bottom'
                if self.mid_left and self.mid_left.__wall__:
                    self.image_name == 'wall_left_right'
                else:
                    self.image_name = 'wall_left'            

            elif (self.bottom_left and self.bottom_left.__wall__ == False and
                self.bottom_mid and self.bottom_mid.__wall__ == True and
                self.mid_left and self.mid_left.__wall__ == True):
                if self.top_mid:
                    if self.top_mid.__wall__ == False:
                           self.top_mid.image_name = self.bind_flore()
                    else:
                        self.top_mid.image_name = 'wall_corner_left_bottom'
                if self.mid_right and self.mid_right.__wall__:
                    self.image_name == 'wall_left_right'
                else:
                    self.image_name = 'wall_right'                

            elif (self.top_left and self.top_left.__wall__ == False and 
                self.top_mid and self.top_mid.__wall__ == True and
                self.mid_left and self.mid_left.__wall__ == True):
                if self.bottom_mid and self.bottom_mid.__wall__ == False:
                    self.image_name =self.bind_wall()
                else:
                    if self.mid_right and self.mid_right.__wall__ == False:
                        self.image_name = 'wall_corner_left_top' 

            elif (self.top_right and self.top_right.__wall__ == False and 
                self.top_mid and self.top_mid.__wall__ == True and
                self.mid_right and self.mid_right.__wall__ == True):
                if self.bottom_mid and self.bottom_mid.__wall__ == False:
                    self.image_name =self.bind_wall()
                else:
                    self.image_name = 'wall_corner_right_top'
            
            # Inner corner
            elif (self.bottom_mid and self.bottom_mid.__wall__ == False and
                self.mid_right and self.mid_right.__wall__ == False and
                self.top_mid and self.top_mid.__wall__ == True and
                self.mid_left and self.mid_left.__wall__ == True):
                if self.top_mid:
                    if self.top_mid and self.top_mid.__wall__ == False:
                        self.top_mid.image_name = 'wall_inner_corner_mid_left'
                    else:
                        self.top_mid.block_sight = True
                        self.top_mid.image_name = 'wall_inner_corner_right_top'
                self.image_name = 'wall_inner_right'

            elif (self.bottom_mid and self.bottom_mid.__wall__ == False and
                self.mid_left and self.mid_left.__wall__ == False and
                self.top_mid and self.top_mid.__wall__ == True and
                self.mid_right and self.mid_right.__wall__ == True):
                if self.top_mid:
                    if self.top_mid.top_mid and self.top_mid.top_mid.__wall__ == False:
                        self.top_mid.image_name = 'wall_inner_corner_mid_right'
                    else:
                        #self.top_mid.block_sight = True
                        self.top_mid.image_name = 'wall_inner_corner_left_top'
                self.image_name = 'wall_inner_left'              

            elif (self.top_mid and self.top_mid.__wall__ == False and
                self.mid_right and self.mid_right.__wall__ == False and
                self.bottom_mid and self.bottom_mid.__wall__ == True and
                self.mid_left and self.mid_left.__wall__ == True):
                self.image_name = 'wall_inner_corner_right_bottom'

            elif (self.top_mid and self.top_mid.__wall__ == False and
                self.mid_left and self.mid_left.__wall__ == False and
                self.bottom_mid and self.bottom_mid.__wall__ == True and
                self.mid_right and self.mid_right.__wall__ == True):
                self.image_name = 'wall_inner_corner_left_bottom'          

            # Normal walls
            elif self.bottom_mid and self.bottom_mid.__wall__ == False:
                if (self.top_mid and self.top_mid.__wall__ == False):
                        self.top_mid.image_name = self.bind_flore()
                        self.image_name = self.bind_wall()
                elif self.top_mid and self.top_mid.top_mid:
                    if self.top_mid.top_mid.__wall__ == False:
                        self.top_mid.image_name = 'wall_top_bottom'
                        self.image_name = self.bind_wall()             
                elif (self.mid_left and self.mid_left.__wall__ == False and
                    self.mid_right and self.mid_left.__wall__ == False):
                    if self.top_mid:
                        self.top_mid.image_name = 'wall_inner_corner_mid_top'
                    self.image_name = 'wall_inner_mid'
                else:
                    if self.top_mid:
                        self.top_mid.image_name = 'wall_top'
                    self.image_name = self.bind_wall()
            elif (self.mid_right and self.mid_right.__wall__ == False and
                 self.mid_left and self.mid_left.__wall__ == False):
                if self.top_mid and self.top_mid.__wall__ == False:
                    self.image_name = 'wall_inner_corner_mid_bottom'
                elif self.bottom_mid and self.bottom_mid.__wall__ == False:
                    self.image_name = 'wall_inner_corner_mid_top'
                else:
                    self.image_name = 'wall_left_right'
            elif self.mid_right and self.mid_right.__wall__ == False: 
                if (self.top_right and self.top_right.__wall__ == False and self.bottom_mid
                    and self.bottom_mid.bottom_mid and self.bottom_mid.bottom_mid.__wall__ == False):
                    self.image_name = 'wall_inner_corner_right_top'
                else:     
                    self.image_name = 'wall_left'

            elif self.top_mid and self.top_mid.__wall__ == False:
                self.image_name = 'wall_bottom'

            elif self.mid_left and self.mid_left.__wall__ == False:
                self.image_name = 'wall_right'
        elif self.__wall__ == False:
            self.flore = True
            self.image_name = self.bind_flore()
            if (self.bottom_mid and self.bottom_mid.__wall__ == None and
            self.bottom_mid.bottom_mid and self.bottom_mid.bottom_mid.__wall__ == True):
                self.bottom_mid.image_name = 'wall_top_bottom'
            

    def bind_wall(self):
        rnd = randint(1,100)
        if rnd > 80:
            return 'wall_inner_1' 
        if rnd > 60:
            return 'wall_inner_2' 
        if rnd > 40:
            return 'wall_inner_3'
        else:
            return 'wall_inner_4'

    def bind_flore(self):
        rnd = randint(1,100)
        if rnd > 95:
            return 'flore_craked_5' 
        elif rnd > 90:
            return 'flore_craked_4' 
        elif rnd > 85:
            return 'flore_craked_3'
        elif rnd > 80:
            return 'flore_craked_2'
        elif rnd > 75:
            return 'flore_craked_1'
        else:
            return 'flore_clean'

    def clean_neighbors(self):
        self.top_left = None
        self.top_mid = None
        self.top_right = None

        self.mid_left = None
        self.mid_mid = None
        self.mid_right = None

        self.bottom_left = None
        self.bottom_mid = None
        self.bottom_right = None