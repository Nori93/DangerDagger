from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from database.db_entity_collection import BaseModel

class Armors(BaseModel):
    __tablename__ = 'armors'
    id_armors = Column(Integer, primary_key=True, unique =True)
    armor_enum = Column(Integer, nullable=False)
    armor_rang = Column(Integer, nullable=False, default=0)
    armor_name = Column(String(32), nullable=False)
    armor_description = Column(String(255))
    cost = Column(Integer, nullable=False)
    armor_class = Column(Integer, nullable=False)
    dex_modifier = Column(Integer)
    strenght = Column(Integer, nullable=False, default=0)
    stealth = Column(Integer, nullable=False, default=0)
    weight = Column(Integer, nullable=False, default=0)
