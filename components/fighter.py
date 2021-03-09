import tcod as libtcod
from game_message import Message
class Fighter:
    def __init__(self, hp, ac, power, xp=0):
        self.max_hp = hp
        self.hp = hp
        self.armor_class = ac
        self.power = power
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

    def hit(self,target):
        enemy_ac = target.fighter.armor_class
        main_hand_weapon = self.owner.equipment.main_hand
        off_hand_weapon = self.owner.equipment.off_hand
        pref = self.owner.preficiencies
        bonus = 
        if main_hand_weapon != None:
        bonus += pref.is_proficient_weapon()

    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense
        
        if damage > 0:
            results.append({
                "message":Message("{} attacks {} for {} hit points.".format(
                    self.owner.name.capitalize(), target.name, damage),libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({"message":
                Message("{} attacks {} but does no damage.".format(self.owner.name.capitalize(), target.name, damage),libtcod.white)})
        
        return results
            