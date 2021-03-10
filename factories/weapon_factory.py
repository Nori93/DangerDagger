from components import Equippable, Weapon
from equipment_slots import EQUIPMENT_SLOTS
from database import get_transaction, Weapons
from entity import Entity
from color import SKY

class WeaponFactory:
    def __init__(self):
        pass       
   
    def create_weapon_from_db(self,weapon_name:str):
        _weapon = db.query(Weapons).filter(Weapons.weapon_name == weapon_name).one()
        return self.create_weapon(_weapon)

    def create_weapon(self,weapon:Weapons):
        self.db = get_transaction()
        equippable_component = Equippable(EQUIPMENT_SLOTS.WEAPONS)
        weapon_component = Weapon(
            weapon_type=weapon.weapon_enum,
            dmg_quantity=weapon.damage_quantity,
            weapon_dmg=weapon.weapon_damage,
            dmg_type=weapon.id_weapon_damage_type,
            light=weapon.light,
            heavy=weapon.heavy,
            two_hand=weapon.two_hand,
            reach=weapon.reach,
            finesse=weapon.finesse,
            thrown=weapon.thrown,
            ammunition=weapon.ammunition,
            range_from=weapon.range_from,
            range_to=weapon.range_to,
            versatile=weapon.versatile,
            versatile_value=weapon.versatile_value,
            loading=weapon.loading
        )
        return Entity(0,0, SKY, weapon.weapon_name, equippable= equippable_component, weapon= weapon_component)
    