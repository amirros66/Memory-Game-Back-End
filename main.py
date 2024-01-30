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
    db_user = models.User()
    
    # check if game is active, if so add user to game
    # active_game = db.query(models.Game).filter(models.Game.active == True).first()
    
    # if active_game:
    #     db_user.game_id = active_game.id
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return create_user(db, user)