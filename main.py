from database import engine, Session, Base
from db_table_models import CharactersTable
from fastapi import FastAPI, HTTPException, Depends
from typing import List
import json
from models import Character, Character_subset_of_fields

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
    ''' An endpoint to get a list of all the Characters in the table. '''
    character_list = db.query(CharactersTable.id,
                              CharactersTable.name,
                              CharactersTable.height,
                              CharactersTable.mass,
                              CharactersTable.birth_year,
                              CharactersTable.eye_color
                              ).all()

    return character_list

    # An endpoint to update a Character by it's ID


@app.get("/character/get/{id}", response_model=Character)
def get_character_by_id(id: int, db: Session = Depends(get_db)):
    ''' An endpoint to get a Character's info by ID.  
    If it does not exists a HTTP Exception of 400 indicating so will be raised. '''

    requested_character = db.query(CharactersTable).filter(
        CharactersTable.id == id).first()

    if requested_character is None:
        raise HTTPException(
            status_code=400,  detail=f"There is no record with ID: {id}")

    return requested_character


@app.post("/character/add", response_model=Character)
def add_new_character(character: Character, db: Session = Depends(get_db)):
    ''' An endpoint to add a new Character.
    If the ID already exists a HTTP Exception of 400 indicating so will be raised. '''

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
    ''' An endpoint to update a Character by ID.
    If the ID does not exists a HTTP Exception of 400 indicating so will be raised. '''

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
    ''' An endpoint to delete a Character by ID.
    If the ID does not exists a HTTP Exception of 400 indicating so will be raised. '''

    character_to_be_deleted = db.query(CharactersTable).filter(
        CharactersTable.id == id).first()

    if character_to_be_deleted is None:
        raise HTTPException(
            status_code=400, detail=f"There is no record with ID: {id}")

    db.query(CharactersTable).filter(
        CharactersTable.id == id).delete()

    db.commit()
