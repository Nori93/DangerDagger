from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.db_entity_collection import BaseModel


class Weapon_Damage_Type(BaseModel):
    __tablename__ = 'weapon_damage_type'
    id_weapon_damage_type = Column(Integer, primary_key=True, unique =True)
    weapon_damage_type_name = Column(String(32), nullable=False, unique= True)   
    #backref
    weapons = relationship('Weapons', back_populates='weapon_damage_type')