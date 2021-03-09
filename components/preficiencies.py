from weapon import WEAPON_TYPE
class Preficiencies:
    def __init__(self, weapons = None, armors=None, ability= None):
        self.weapons = weapons
        self.armors = armors
        self.ability = ability

    
    def is_proficient_weapon(self, weapon_enum: WEAPON_TYPE):
        for weapon in self.weapons:
            if weapon["enum"] == weapon_enum.value:
                return True
        else:
            return False