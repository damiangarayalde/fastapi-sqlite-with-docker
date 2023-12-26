from sqlalchemy import Column, Integer, String
from database import Base


class CharactersTable(Base):
    __tablename__ = "starwars_characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    height = Column(Integer)
    mass = Column(Integer)
    hair_color = Column(String)
    skin_color = Column(String)
    eye_color = Column(String)
    birth_year = Column(Integer)
