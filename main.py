from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.game import (create_user, create_sequence,
                      create_game, reset_game_data, get_display_sequences)
from app.scores import calculate_score, store_score
from app.sequences import add_sequences, add_input_sequences

from app import database, schemas, scores, game

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
@app.post("/users/{game_id}", response_model=schemas.UserBase)
def add_user(game_id: int, db: Session = Depends(get_db)):
    return create_user(db, game_id)


# submit input sequence
@app.post("/input", response_model=schemas.InputSequence)
def add_sequence(input_sequence: schemas.InputSequenceCreate, user_id: int, display_sequence_id: int, db: Session = Depends(get_db)):
    try:
        print(
            f"Received request with input_sequence={input_sequence}, user_id={user_id}, display_sequence_id={display_sequence_id}")
        new_input_sequence = create_sequence(
            db, input_sequence, user_id, display_sequence_id)
        round_score = calculate_score(db, new_input_sequence)
        store_score(db, round_score, user_id,
                    display_sequence_id, new_input_sequence.id)
        return new_input_sequence
    except Exception as e:
        print(f"Error processing request: {e}")
        return JSONResponse(status_code=422, content={"detail": "Validation error"})

# Get first active game


@app.get("/game/active", response_model=schemas.GameBase)
def read_active_game(db: Session = Depends(get_db)):
    active_game = game.get_active_game(db)
    if active_game is None:
        raise HTTPException(status_code=404, detail="No active game")
    else:
        return active_game

# Create a game


@app.post("/game", response_model=schemas.NewGame)
def create_new_game(db: Session = Depends(get_db)):
    new_game = create_game(db=db)
    new_user = create_user(db=db, game_id=new_game.id)
    new_sequences = add_sequences(db=db, game_id=new_game.id)
    return {"game_id": new_game.id, "user_id": new_user.id, "player_name": new_user.player_name, "sequences": new_sequences}


# Get score for 1 round

@app.get("/scores/round/{display_sequence_id}", response_model=schemas.RoundScores)
def read_scores_by_round(display_sequence_id: int, db: Session = Depends(get_db)):
    scores_data = scores.get_all_scores_by_round(
        db, display_sequence_id=display_sequence_id)
    all_scores = [schemas.UserScore(user_id=score.user_id, correct_guesses=score.correct_guesses,
                                    incorrect_guesses=score.incorrect_guesses) for score in scores_data]
    return schemas.RoundScores(round_id=display_sequence_id, scores=all_scores)

# Get score for all rounds of a game


@app.get("/scores/total/{game_id}", response_model=List[schemas.TotalScore])
def read_scores_by_game(game_id: int, db: Session = Depends(get_db)):
    return scores.calculate_total_scores(db, game_id=game_id)

# Get users for lobby


@app.get("/game/{game_id}/users", response_model=list[schemas.LobbyUser])
def read_users_for_game_id(game_id: int, db: Session = Depends(get_db)):
    users = game.get_users_in_game(db, game_id=game_id)
    return [
        schemas.LobbyUser(user_id=user.id, player_name=user.player_name)
        for user in users
    ]

# Delete entries / reset game (by ID)


@app.delete("/game-over/{game_id}")
def game_over_reset(game_id: int, db: Session = Depends(get_db)):
    reset_game_data(db, game_id)
    return {"message": "Game reset successfully"}


# Get display sequences
@app.get("/display-sequences", response_model=List[schemas.DisplaySequence])
def read_display_sequences(game_id: int, db: Session = Depends(get_db)):
    return get_display_sequences(db, game_id)


@app.get("/healthz", response_model=schemas.Healthz)
def healthz():
    return {"status": "ok"}


# Create single-player game
@app.post("/single", response_model=schemas.NewSingleGame)
def create_new_game(db: Session = Depends(get_db)):
    new_game = create_game(db=db)
    new_game.single = True
    new_display_sequences = add_sequences(db=db, game_id=new_game.id)
    users = []
    for _ in range(3):
        user = create_user(db=db, game_id=new_game.id)
        users.append(user)
    input_sequences = []
    for user in users[-2:]:
        new_sequences = add_input_sequences(db=db, user_id=user.id, display_sequences=new_display_sequences)
        input_sequences.extend(new_sequences)
    for sequence in input_sequences:
            round_score = calculate_score(db, sequence)
            store_score(db, round_score, user_id=sequence.user_id,
                    display_sequence_id=sequence.display_sequence_id, input_sequence_id=sequence.id)
    return {
        "game_id": new_game.id,
        "single": new_game.single,
        "display_sequences": new_display_sequences,
        "users": [{
            "user_id": user.id,
            "player_name": user.player_name,
            "sequences": input_sequences[i] if i < 2 else [] 
        } for i, user in enumerate(users)]
    }