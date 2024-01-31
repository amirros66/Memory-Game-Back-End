from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.game import create_user, create_sequence, create_game

from app import models, database, schemas

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# add user 
@app.post("/users/", response_model=schemas.UserBase)
def add_user(user: schemas.UserCreate, game_id: int, db: Session = Depends(get_db)):
    return create_user(db, user, game_id)



# submit input sequence 
@app.post("/input_sequence/", response_model=schemas.InputSequenceBase)
def add_sequence(input_sequence: schemas.InputSequenceCreate, user_id: int,  db: Session = Depends(get_db)):
    return create_sequence(db, input_sequence, user_id)


#Create a game
@app.post("/game", response_model=schemas.GameCreate)
def create_new_game(game_create: schemas.GameCreate, db: Session = Depends(get_db)):
    return create_game(db=db, game_create=game_create)