from sqlalchemy.orm import Session
from . import models, schemas

def calculate_score(db: Session, input_sequence: schemas.InputSequence):
    #get the display sequence
    display_sequence = db.query(models.DisplaySequence).filter(models.DisplaySequence.id == input_sequence.display_sequence_id).first()
    #split the input sequence into a list
    input_sequence_list = input_sequence.value.split(',')
    #split the display sequence into a list
    display_sequence_list = display_sequence.value.split(',')
    #compare the two lists
    correct_guesses = 0
    incorrect_guesses = 0
    for i in range(len(input_sequence_list)):
        if input_sequence_list[i] == display_sequence_list[i]:
            correct_guesses += 1
        else:
            incorrect_guesses += 1
    #return the score
    return schemas.ScoreBase(correct_guesses=correct_guesses, incorrect_guesses=incorrect_guesses)

def store_score(db: Session, score: schemas.ScoreBase, user_id: int, display_sequence_id: int, input_sequence_id: int):
    db_score = models.Score()
    db_score.correct_guesses = score.correct_guesses
    db_score.incorrect_guesses = score.incorrect_guesses
    db_score.user_id = user_id
    db_score.display_sequence_id = display_sequence_id
    db_score.input_sequence_id = input_sequence_id
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score