from sqlalchemy import Table,Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.db_entity_collection import BaseModel
from database.entities.preficiencies_weapons import PreficienciesWeapons


class Classes(BaseModel):
    __tablename__ = 'classes'
    id_classes= Column(Integer, primary_key=True, unique =True)
    class_name = Column(String(32), nullable=False)
    class_description = Column(String(255))    
    hit_die = Column(Integer,nullable=False, default=8)
    primary_ability_count = Column(Integer, nullable=False, default=1)
    preficiencies_weapons = relationship('Weapons',secondary='preficiencies_weapons')