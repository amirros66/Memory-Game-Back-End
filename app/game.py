from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, game_id: int):
    db_user = models.User()
    db.add(db_user)
    
    active_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    
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

def get_users_in_game(db: Session, game_id: int):
    return db.query(models.User)\
             .filter(models.User.game_id == game_id)\
             .all()

def reset_game_data(db: Session, game_id: int):
    # Delete Scores
    db.query(models.Score).filter(models.Score.user_id.in_(
        db.query(models.User.id).filter(models.User.game_id == game_id)
    )).delete(synchronize_session='fetch')

    # Delete Input Sequences
    db.query(models.InputSequence).filter(models.InputSequence.display_sequence_id.in_(
        db.query(models.DisplaySequence.id)
    )).delete(synchronize_session='fetch')

    # Delete Display Sequences
    db.query(models.DisplaySequence).delete(synchronize_session='fetch')

    # Delete Users
    db.query(models.User).filter(models.User.game_id == game_id).delete(synchronize_session='fetch')

    # Delete the Game
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if game:
        db.delete(game)
        db.commit()
        return True  
    else:
        db.rollback()  
        return False 


# get display sequences
def get_display_sequences(db: Session, game_id: int):
    return db.query(models.DisplaySequence)\
             .filter(models.DisplaySequence.game_id == game_id)\
             .all()