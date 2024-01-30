from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.game import create_user

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
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = models.User()
    db: Session - Depends(get_db)
    
    # check if game is active, if so add user to game
    # active_game = db.query(models.Game).filter(models.Game.active == True).first()
    
    # if active_game:
    #     user.game_id = active_game.id

    return create_user(db, user)