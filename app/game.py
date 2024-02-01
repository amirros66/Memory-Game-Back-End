from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, game_id: int):
    db_user = models.User()
    db.add(db_user)
    
    active_game = db.query(models.Game).filter(models.Game.active == True).first()
    
    if active_game:
        db_user.game_id = active_game.id
        
    db.commit()
    db.refresh(db_user)
    return db_user


# add input sequence 
def create_sequence(db: Session, sequence: schemas.InputSequenceCreate, user_id: int, display_sequence_id: int):
    db_sequence = models.InputSequence()
    db_sequence.value = sequence.value
    db_sequence.user_id = user_id
    db_sequence.display_sequence_id = display_sequence_id
    db.add(db_sequence)  
    db.commit()
    db.refresh(db_sequence)
    return db_sequence



#Create a new game
def create_game(db: Session):
    db_game = models.Game()
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

#Get first active game
def get_active_game(db: Session):
    return db.query(models.Game).filter(models.Game.active == True).first()


#GET /users endpoint for use in the lobby screen
# Request parameter should be game_id
# No other information required in the request body
# Response should return a list of users containing user_id and player_name

def get_users_in_game(db: Session, game_id: int):
    return db.query(models.User)\
             .filter(models.User.game_id == game_id)\
             .all()
