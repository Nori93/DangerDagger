from enum import Enum
class WEAPON_TYPE(Enum):
    #Simple Melee Weapons
    CLUB = 0                
    DAGGER = 1              #throw
    GREAT_CLUB = 2          #h2
    HANDAXE = 3             #throw
    JAVELIN = 4             #throw
    LIGHT_HAMMER = 5        #throw
    MACE = 6
    STAFF = 7
    SICKLE = 8
    SPEAR = 9               #throw
    #Simple Range Weapons 
    CROSSBOW = 10
    DART = 11               #throw
    SHORTBOW = 12           #h2
    SLING = 13    
    #Martial Melee Weapons
    BATTLEAXE = 14
    FLAIL = 15
    GLAIVE = 16             #h2
    GREATAXE = 17           #h2
    GREATSWORD = 18         #h2
    HALBERD = 19            #h2
    LANCE = 20
    LONGSWORD = 21          
    MAUL = 22               #h2
    MORNINGSTAR = 23
    PIKE = 24               #h2
    RAPIER = 25             
    SCIMITAR = 26           
    SHORTSWORD = 27 
    TRIDNET = 28            #throw
    WAR_PICK = 29
    WARHAMMER = 30
    WHIP = 31
    #Martial Range Weapons
    BLOWGUN = 32
    CROSSBOW_HAND = 33
    CROSSBOW_HEAVY = 34    #h2
    LONGBOW = 35           #h2
    NET = 36               #throw
    #Shield
    SHIELD = 37
    GREATSHIELD = 38


class Weapon:

    two_hand_weapon = [
        WEAPON_TYPE.GREAT_CLUB,
        WEAPON_TYPE.SHORTBOW,
        WEAPON_TYPE.GLAIVE,
        WEAPON_TYPE.GREATAXE,
        WEAPON_TYPE.GREATSWORD,
        WEAPON_TYPE.HALBERD,
        WEAPON_TYPE.MAUL,
        WEAPON_TYPE.PIKE,
        WEAPON_TYPE.CROSSBOW_HEAVY,
        WEAPON_TYPE.LONGBOW
        ]

    throw_weapon = [
        WEAPON_TYPE.HANDAXE,
        WEAPON_TYPE.JAVELIN,
        WEAPON_TYPE.LIGHT_HAMMER,
        WEAPON_TYPE.SPEAR,
        WEAPON_TYPE.DART,
        WEAPON_TYPE.TRIDNET,
        WEAPON_TYPE.NET
    ]

    off_hand = [
        WEAPON_TYPE.SHIELD,
        WEAPON_TYPE.GREATSHIELD

    ]

    def __init__(self, dmg, max_dmg,  crit_rate, w_type, range_use=None):
        self.dmg = dmg,
        self.max_dmg = max_dmg
        self.crit_rate = crit_rate
        self.w_type = w_type,    
        self.range_use = range_use

        if self.range_use:
            self.range_use.owner = self

        self.two_hand = self.w_type in Weapon.two_hand_weapon
        self.throwable = self.w_type in Weapon.throw_weapon
    
    def throw(self):