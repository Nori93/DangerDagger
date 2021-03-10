
from components.ai import BasicMonster


from database.db_entity_collection import get_transaction
from database.entities.monsters import Monsters


class MonsterFactory:
    def __init__(self):
        self.db = get_transaction()
    
    def create_monster(self,monster_name):
        _monster = self.db.query(Monsters).filter(Monsters.monster_name == monster_name).one()
        ai_component = BasicMonster()
        ability_component = Ability(
                        strenght=_monster.strenght,
                        dexterity=_monster.dexterity,
                        constitution=_monster.constitution,
                        intelligence=_monster.intelligence,
                        wisdom=_monster.wisdom,
                        charisma=_monster.charisma
                    )