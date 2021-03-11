from sqlalchemy import Table,Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.db_entity_collection import BaseModel
from database.entities.classes import Classes


class LevelUps(BaseModel):
    __tablename__ = 'level_ups'
    id_level_ups= Column(Integer, primary_key=True, unique =True)
    level = Column(Integer,nullable=False)    
    id_classes =  Column(Integer, ForeignKey('classes.id_classes'))
    ability_increase = Column(Boolean)    
    id_spells = Column(Integer)
    id_class_ability = Column(Integer)
    proficiency_bonus = Column(Boolean)
    classes = relationship("Classes")