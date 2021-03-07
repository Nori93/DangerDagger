import os.path
from sqlalchemy import Column,ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

path = 'sqlite:///database/database.db'

db = create_engine(path)

BaseModel = declarative_base()

"""
if os.path.isfile('database.db'):
    print("Database exist")
else: 
    db.create_all()
    print("Create new Database")
"""

def get_transaction():
    session = sessionmaker(bind=db)
    return session()