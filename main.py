from database import engine, Session, Base
from models import CharactersTable
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Depends
from typing import List
import json


app = FastAPI(
    title="API to manage a StarWars' characters db",
    description="This is a simple API to execute CRUD operations on a characters db",
    docs_url='/'
)


Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


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


def init_db_with_main_characters():
    db = Session()
    try:
        # Check if there are already records in the CharactersTable
        if db.query(CharactersTable).count() == 0:

            with open('sw_main_characters_data.json', 'r') as json_file:

                # Read the contents of the file and store them in a variable
                initial_characters = json.load(json_file)

                for x in initial_characters:
                    char = Character(**x)
                    character_to_be_added = CharactersTable()
                    character_to_be_added.name = char.name
                    character_to_be_added.mass = char.mass
                    character_to_be_added.birth_year = char.birth_year
                    character_to_be_added.skin_color = char.skin_color
                    character_to_be_added.eye_color = char.eye_color
                    character_to_be_added.hair_color = char.hair_color
                    character_to_be_added.height = char.height

                    db.add(character_to_be_added)
                    db.commit()

    finally:
        db.close()


@app.on_event("startup")
async def pre_load_db_with_records(db: Session = Depends(get_db)):

    init_db_with_main_characters()


@app.get("/character/getAll", response_model=List[Character_subset_of_fields])
def get_all_characters(db: Session = Depends(get_db)):

    character_list = db.query(CharactersTable.id,
                              CharactersTable.name,
                              CharactersTable.height,
                              CharactersTable.mass,
                              CharactersTable.birth_year,
                              CharactersTable.eye_color
                              ).all()

    return character_list


@app.get("/character/get/{id}", response_model=Character)
def get_character_by_id(id: int, db: Session = Depends(get_db)):

    requested_character = db.query(CharactersTable).filter(
        CharactersTable.id == id).first()

    if requested_character is None:
        raise HTTPException(
            status_code=400,  detail=f"There is no record with ID: {id}")

    return requested_character


@app.post("/character/add", response_model=Character)
def add_new_character(character: Character, db: Session = Depends(get_db)):

    existing_character_with_that_id = db.query(CharactersTable).filter(
        CharactersTable.id == character.id).first()

    if existing_character_with_that_id is None:

        character_to_be_added = CharactersTable()

        character_to_be_added.name = character.name
        character_to_be_added.mass = character.mass
        character_to_be_added.birth_year = character.birth_year
        character_to_be_added.skin_color = character.skin_color
        character_to_be_added.eye_color = character.eye_color
        character_to_be_added.hair_color = character.hair_color
        character_to_be_added.height = character.height

        db.add(character_to_be_added)
        db.commit()

        return character

    else:
        raise HTTPException(
            status_code=400,  detail=f"There is already a character with ID: {character.id}. Please use other value")


@app.put("/character/update/", response_model=Character)
def update_character_by_id(character: Character, db: Session = Depends(get_db)):

    character_to_update = db.query(CharactersTable).filter(
        CharactersTable.id == character.id).first()

    if character_to_update is None:
        raise HTTPException(
            status_code=400,
            detail=f"There is no record with ID: {character.id}"
        )

    character_to_update.name = character.name
    character_to_update.mass = character.mass
    character_to_update.birth_year = character.birth_year
    character_to_update.skin_color = character.skin_color
    character_to_update.eye_color = character.eye_color
    character_to_update.hair_color = character.hair_color
    character_to_update.height = character.height

    db.add(character_to_update)
    db.commit()

    return character


@app.delete("/character/delete/{id}")
def delete_character_by_id(id: int, db: Session = Depends(get_db)):

    character_to_be_deleted = db.query(CharactersTable).filter(
        CharactersTable.id == id).first()

    if character_to_be_deleted is None:
        raise HTTPException(
            status_code=400, detail=f"There is no record with ID: {id}")

    db.query(CharactersTable).filter(
        CharactersTable.id == id).delete()

    db.commit()
