from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.db_entity_collection import BaseModel


class PreficienciesWeapons(BaseModel):
    __tablename__ = 'preficiencies_weapons'
    id_preficiencies_weapons = Column(Integer, primary_key=True, unique =True)
    id_classes = Column(Integer, ForeignKey('classes.id_classes'))
    id_weapons = Column(Integer, ForeignKey('weapons.id_weapons'))