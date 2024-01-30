from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.game import create_user, create_sequence

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
    return create_user(db, user)



# submit input sequence 
@app.post("/input_sequence/", response_model=schemas.InputSequenceBase)
def add_sequence(input_sequence: schemas.InputSequenceCreate, db: Session = Depends(get_db)):
    return create_sequence(db, input_sequence)