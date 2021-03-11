from components import Playable, BasicMonster, Ability, Inventory, Equipment
from factories.weapon_factory import WeaponFactory
from database import get_transaction, Monsters
from game.render_function import RenderOrder
from game.entity import Entity
from game.color import DESATURED_GREEN
from random import randint

class MonsterFactory:
    def __init__(self):
        
        self.weapon_factory = WeaponFactory()
    
    def create_monster(self,monster_name,x,y):
        self.db = get_transaction()
        _monster:Monsters = self.db.query(Monsters).filter(Monsters.monster_name == monster_name).one()
        ai_component = BasicMonster()
        ability_component = Ability(
                        strenght=_monster.strenght,
                        dexterity=_monster.dexterity,
                        constitution=_monster.constitution,
                        intelligence=_monster.intelligence,
                        wisdom=_monster.wisdom,
                        charisma=_monster.charisma
                    )
        playable_component = Playable(hp=_monster.hit_points, ac =_monster.armor_class, xp=_monster.exp)
        inventory_component = Inventory(2)
        equipment_component = Equipment()
        monster = Entity(x, y, DESATURED_GREEN,_monster.monster_name, blocks=True,
                    render_order = RenderOrder.ACTOR ,
                    playable = playable_component,
                    ai = ai_component,
                    inventory= inventory_component,                
                    equipment= equipment_component,
                    ability=ability_component,
                    image_name="{}_right".format(_monster.monster_name.lower()))
        if len(_monster.monsters_weapons) > 0:
            random = randint(0,100)
            _weapon = None
            
            if random > 75:
                _weapon = self.weapon_factory.create_weapon(_monster.monsters_weapons[1])
            else:
                _weapon = self.weapon_factory.create_weapon(_monster.monsters_weapons[0])
            
            if _weapon != None:                   
               monster.inventory.add_item(_weapon)
               monster.inventory.toggle_equip_main_hand(_weapon)

        return monster