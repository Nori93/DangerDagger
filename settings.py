class Settings:
    def __init__(self):
        self.window_title = "Danger Dagger"

        self.screen_width = 1024
        self.screen_height = 680

        self.tile_size = 50
        self.FPS = 60

        self.bar_width = 20 
        self.panel_height = 7
        self.panel_y = self.screen_height - self.panel_height

        self.message_x = self.bar_width + 2
        self.message_width = self.screen_width - self.bar_width - 2
        self.message_height = self.panel_height - 1

        self.map_width = 80
        self.map_height = 43

        self.room_max_size = 10
        self.room_min_size = 6

        self.max_room = 30

        self.fov_algorithm = 0
        self.fov_light_walls = True
        self.fov_radius = 5

        
        self.font = '.\Assets\dogicabold.ttf'


    @property
    def get(self):
        constants = {
            "window_title":self.window_title,
            "screen_width":self.screen_width,
            "screen_height":self.screen_height,
            "tile_size":self.tile_size,
            "bar_width":self.bar_width,
            "panel_height":self.panel_height,
            "panel_y":self.panel_y,
            "message_x":self.message_x,
            "message_width":self.message_width,
            "message_height":self.message_height,
            "map_width":self.map_width,
            "map_height":self.map_height,
            "room_max_size":self.room_max_size,
            "room_min_size":self.room_min_size,
            "max_room":self.max_room,
            "fov_algorithm":self.fov_algorithm,
            "fov_light_walls":self.fov_light_walls,
            "fov_radius":self.fov_radius,
            "font":self.font,
            "FPS":self.FPS
        }
        return constants