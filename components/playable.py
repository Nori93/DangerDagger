import tcod as libtcod
from game_message import Message
class Playable:
    def __init__(self, hp, ac,xp):
        self.max_hp = hp
        self.hp = hp
        self.armor_class = ac
        self.xp = xp      
        
    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({"dead": self.owner, "xp":self.xp})

        return results

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def hit(self,target,main_hand=None,off_hand=None):
        results=[]
        return results

    def attack(self, target):
        results = []
        main_hand_weapon = self.owner.equipment.main_hand

        damage = self.power - target.Playable.defense
        
        if damage > 0:
            results.append({
                "message":Message("{} attacks {} for {} hit points.".format(
                    self.owner.name.capitalize(), target.name, damage),libtcod.white)})
            results.extend(target.Playable.take_damage(damage))
        else:
            results.append({"message":
                Message("{} attacks {} but does no damage.".format(self.owner.name.capitalize(), target.name, damage),libtcod.white)})
        
        return results
    
    def get_atk_bonus(self,weapon):
        pass
            