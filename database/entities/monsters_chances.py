from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.db_entity_collection import BaseModel
from database.entities.monsters import Monsters


class MonstersChances(BaseModel):
    __tablename__ = 'monsters_chances'
    id_monsters_chances = Column(Integer, primary_key=True, unique =True)
    id_monsters = Column(Integer, ForeignKey('monsters.id_monsters'))
    id_dungeon_level = Column(Integer,nullable=False, default=1)
    chances = Column(Integer,nullable=False, default=100)
    monster = relationship("Monsters")