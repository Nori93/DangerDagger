from enum import Enum

class EquipmentSlots(Enum):
    # FACK: googles, lenses, mask, spectacles, thrid eyes
    FACE = 1
    # HEAD: cirlets, crowns, hats, headbands, helmets, phylacteries.
    HEAD = 2
    # NECK/THROAT : amulets, badges, brooches, collars, medals, 
    #   medallions, necklaces, pendants, periapts, scarabs, scarfs, torcs.
    NECK = 3
    # SCHOLDER: capes, cloaks, mantles, shawls.
    SHOULDERS = 4
    # ARMOR/BODY: armor, robes.
    ARMOR = 5
    # BODY/TORSO: shirts, tunics, vests, vestments.
    BODY = 6
    # HANDS: gauntlets, gloves
    HANDS = 7
    # ARMS: armbands , bracelets, bracers.
    BRACELETS = 8
    # WAIST: Belts, girdles, sashes.
    WAIST = 9
    # RINGS: rings, signet, brass knuckles
    RINGS = 10
    # FEET: Boots, sandals, shoes, slippers
    FEET = 11
    # WEAPONS: weapons, staffm rods, wands, shields
    WEAPONS = 12

