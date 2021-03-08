import pygame as pg
from data_loaders import load_sprite_sheet_json, load_sprite_sheet
class SpriteSheet:
     # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.filename = filename
        self.spritesheet = load_sprite_sheet('{}.png'.format(filename))
        self.json_file = load_sprite_sheet_json('{}.json'.format(filename))
    
    def get_image_by_name(self,name):
        tile_set = self.json_file['meta']['slices']
        for tile in tile_set:
            if tile['name'] == name:
                bounds = tile['keys'][0]['bounds']
                return self.get_image(bounds['x'],bounds['y'],bounds['w'],bounds['h'])
        raise Exception("Not found {} in {}".format(name, self.filename))


    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        #image = pg.transform.scale(image, (width // 2,height // 2))
        return image