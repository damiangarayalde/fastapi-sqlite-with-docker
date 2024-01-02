from pydantic import BaseModel, Field
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


class Character(BaseModel):
    """ Every being in the galaxy has these attributes and their values comply to these restrictions: """
    id:         int = Field(1, gt=0)
    name:       str = Field('Yoda', min_length=1)
    height:     int = Field(45, gt=0)
    mass:       int = Field(40, gt=0)
    hair_color: str = Field('None', min_length=3, max_length=30)
    skin_color: str = Field('Green', min_length=3, max_length=30)
    eye_color:  str = Field('Green', min_length=3, max_length=30)
    birth_year: int = Field(900, gt=0)


class Character_subset_of_fields(BaseModel):
    """ When queryng for all characters we will only return these fields: """
    id:         int = Field(1, gt=0)
    name:       str = Field('Yoda', min_length=1)
    height:     int = Field(45, gt=0)
    mass:       int = Field(40, gt=0)
    skin_color: str = Field('Green', min_length=3, max_length=30)
    eye_color:  str = Field('Green', min_length=3, max_length=30)
    birth_year: int = Field(900, gt=0)
