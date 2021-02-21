import tcod as libtcod

from random import randint
from game_messages import Message

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner
        results = []
        if fov_map.fov[monster.y][monster.x]:
            if monster.distance_to(target ) >= 2:
                monster.move_astar(target, game_map, entities)
            
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
        
        return results

class CofusedMonster:
    def __init__(self, previus_ai, number_of_turns=10):
        self.previus_ai = previus_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, targer, fov_map, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)
            
            self.number_of_turns -=1
        else:
            self.owner.ai = self.previus_ai
            results.append({"message":Message("The {} is no longer confuse".format(self.owner.name), libtcod.red)})
        
        return results