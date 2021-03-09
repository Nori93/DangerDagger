import math
import tcod as libtcod
from components.item import Item
from render_function import RenderOrder
class Entity:
    def __init__(
        self,
        x,
        y,
        color,
        name,
        blocks=False,
        render_order=RenderOrder.CORPSE,
        fighter=None,
        ai=None,
        item=None, 
        inventory=None, 
        stairs=None, 
        level=None,
        equipment=None, 
        equippable=None, 
        weapon=None,
        ability=None,
        image_name=None,
        preficiencies=None):
        self.x = x
        self.y = y       
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai
        self.render_order = render_order
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable
        self.weapon = weapon
        self.ability = ability
        self.image_name = image_name
        self.preficiencies = preficiencies
        
        if self.fighter:
            self.fighter.owner = self
        if self.ai:
            self.ai.owner = self
        if self.item:
            self.item.owner = self
        if self.inventory:
            self.inventory.owner = self
        if self.stairs:
            self.stairs.owner = self
        if self.level:
            self.level.owner = self
        if self.equipment:
            self.equipment.owner = self
        if self.equippable:
            self.equippable.owner = self
            if not self.item:
                item = Item()
                self.item =item
                self.item.owner = self
        if self.weapon:
            self.weapon.owner = self
        
        if self.ability:
            self.ability.owner = self
        if self.preficiencies:
            self.preficiencies.owner = self

    def move(self, dx, dy):
        self.update_image(dx,dy)
        self.x += dx
        self.y += dy

    def update_image(self,dx,dy):
        image_name_array = self.image_name.split("_")
        if dy > 0:
            self.image_name = "{}_{}".format(image_name_array[0],"bottom")
        elif dy < 0:
            self.image_name = "{}_{}".format(image_name_array[0],"top")
        elif dx > 0:
            self.image_name = "{}_{}".format(image_name_array[0],"right")
        elif dx < 0:
            self.image_name = "{}_{}".format(image_name_array[0],"left")
        else:
            self.image_name = self.image_name

    def get_blocking_entities_at_location(self,entities, destination_x, destination_y):
        for entity in entities:
            if entity.blocks and entity.x == destination_x and entity.y == destination_y:
                return entity
        return None

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
            self.get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def move_astar(self, target,  game_map, entities):
        fov = libtcod.map_new(game_map.map_width, game_map.map_height)

        for y1 in range(game_map.map_height):
            for x1 in range(game_map.map_width):
                fov.transparent[y1][x1]= not game_map.tiles[x1][y1].block_sight
                fov.walkable[y1][x1]= not game_map.tiles[x1][y1].blocked
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                fov.transparent[entity.y][entity.x] = True
                fov.walkable[entity.y][entity.x] = False

        my_path = libtcod.path_new_using_map(fov, 1.41)

        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            x,y = libtcod.path_walk(my_path, True)
            if x or y:
                self.update_image(x-self.x,y-self.y)
                self.x = x
                self.y = y
        else:
            self.move_towards(target.x, target.y, game_map, entities)
        
        libtcod.path_delete(my_path)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)