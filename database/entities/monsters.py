from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from database.db_entity_collection import BaseModel

class Monsters(BaseModel):
    __tablename__='monsters'
    id_monsters = Column(Integer, primary_key=True, unique =True)
    monster_name = Column(String(32), nullable=False)
    monster_description = Column(String(255))
    armor_class = Column(Integer, nullable=False, default=1)
    hit_points = Column(Integer, nullable=False, default=1)
    exp = Column(Integer, nullable=False, default=1)
    strenght = Column(Integer, nullable=False, default=1)
    dexterity = Column(Integer, nullable=False, default=1)
    constitution = Column(Integer, nullable=False, default=1)
    intelligence = Column(Integer, nullable=False, default=1)
    wisdom = Column(Integer, nullable=False, default=1)
    charisma = Column(Integer, nullable=False, default=1)