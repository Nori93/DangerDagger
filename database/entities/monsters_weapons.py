from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.db_entity_collection import BaseModel


class MonstersWeapons(BaseModel):
    __tablename__ = 'monsters_weapons'
    id_monsters_weapons = Column(Integer, primary_key=True, unique =True)
    id_monsters = Column(Integer, ForeignKey('monsters.id_monsters'))
    id_weapons = Column(Integer, ForeignKey('weapons.id_weapons'))