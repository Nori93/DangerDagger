from enum import Enum
from random import randint
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
    def __init__(
        self,
        weapon_type:WEAPON_TYPE,
        dmg_quantity:int,
        weapon_dmg:int,
        dmg_type:int,
        light:bool=False,
        heavy:bool=False,
        two_hand:bool=False,
        reach:bool=False,
        finesse:bool=False,
        thrown:bool=False,
        ammunition:bool=False,
        range_from:int=None,
        range_to:int=None,
        versatile:bool=False,
        versatile_value:int=None,
        loading:bool=False,
        special:bool=False
        ):
        self.weapon_type = weapon_type
        self.dmg_quantity = dmg_quantity
        self.weapon_dmg = weapon_dmg
        self.dmg_type = dmg_type
        self.light = light
        self.heavy = heavy
        self.two_hand = two_hand
        self.reach = reach
        self.finesse = finesse
        self.thrown = thrown
        self.ammunition = ammunition
        self.range_from = range_from
        self.range_to = range_to
        self.versatile = versatile
        self.versatile_value = versatile_value
        self.loading = loading
        self.special = special