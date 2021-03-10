
from components.ai import BasicMonster
from components.ability import Ability
from components import Playable, BasicMonster, Ability
from database import get_transaction, Monsters


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
        playable_component = Playable(hp=7, ac =15, xp=50)