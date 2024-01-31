from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.game import create_user, create_sequence, create_game
from app.sequences import add_sequences
from app.scores import get_all_scores_by_round

from app import models, database, schemas, scores

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
def add_user(game_id: int, db: Session = Depends(get_db)):
    return create_user(db, game_id)



# submit input sequence 
@app.post("/input_sequence/", response_model=schemas.InputSequenceBase)
def add_sequence(input_sequence: schemas.InputSequenceCreate, user_id: int,  display_sequence_id: int, db: Session = Depends(get_db)):
    return create_sequence(db, input_sequence, user_id, display_sequence_id)


#Create a game
@app.post("/game", response_model=schemas.NewGame)
def create_new_game(db: Session = Depends(get_db)):
    new_game = create_game(db=db)
    new_user = create_user(db=db, game_id=new_game.id)
    new_sequences = add_sequences(db=db)
    return {"game_id": new_game.id, "user_id": new_user.id, "player_name": new_user.player_name, "sequences": new_sequences}



#Get score for 1 round

@app.get("/scores/round/{display_sequence_id}", response_model=schemas.RoundScores)
def read_scores_by_round(display_sequence_id: int, db: Session = Depends(get_db)):
    scores_data = scores.get_all_scores_by_round(db, display_sequence_id=display_sequence_id)
    all_scores = [schemas.UserScore(user_id=score.user_id, correct_guesses=score.correct_guesses, incorrect_guesses=score.incorrect_guesses) for score in scores_data]
    return schemas.RoundScores(round_id=display_sequence_id, scores=all_scores)