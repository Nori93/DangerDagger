from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric
from sqlalchemy.orm import relationship
from database.db_entity_collection import BaseModel
from database.entities.weapon_damage_type import Weapon_Damage_Type


class Weapons(BaseModel):
    __tablename__ = 'weapons'
    id_weapons = Column(Integer, primary_key=True, unique =True)
    weapon_enum = Column(Integer, nullable=False)
    id_weapon_rang = Column(Integer, nullable=False)
    weapon_name = Column(String(32), nullable=False)
    weapon_description = Column(String(100))
    weapon_cost = Column(Integer, nullable=False, default=1)
    damage_quantity = Column(Integer, nullable=False, default=1)
    weapon_damage = Column(Integer, nullable=False, default=4)
    id_weapon_damage_type = Column(Integer, ForeignKey('weapon_damage_type.id_weapon_damage_type'))
    weapon_weight = Column(Numeric, nullable=False, default = 0.25)
    light = Column(Boolean, nullable=False, default=False)
    heavy = Column(Boolean, nullable=False, default=False)
    two_hand = Column(Boolean, nullable=False, default=False)
    reach = Column(Boolean, nullable=False, default=False)
    finesse = Column(Boolean, nullable=False, default=False)
    thrown = Column(Boolean, nullable=False, default=False)
    ammunition = Column(Boolean, nullable=False, default=False)
    range_from = Column(Numeric, nullable=False, default=0)
    range_to = Column(Numeric, nullable=False, default=0)
    versatile =  Column(Boolean, nullable=False, default=0)
    versatile_value = Column(Integer)
    loading =  Column(Boolean, nullable=False, default=0)
    special = Column(Boolean, nullable=False, default=0)

    #refs
    weapon_damage_type = relationship("Weapon_Damage_Type", back_populates="weapons")