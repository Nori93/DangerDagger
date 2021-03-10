from components.weapon import WEAPON_TYPE
class Preficiencies:
    def __init__(self, weapons = None, armors=None, ability= None):
        self.weapons = []
        self.armors = []
        self.ability = []
        if weapons != None:
            self.rewrite_weapons(weapons)

    def rewrite_weapons(self,weapons):
        for w in weapons:
            self.weapons.append(w.weapon_enum)

    def is_proficient_weapon(self, weapon_enum: WEAPON_TYPE):
        for weapon in self.weapons:
            if weapon == weapon_enum.weapon_type:
                return True
        else:
            return False