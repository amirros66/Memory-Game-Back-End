from sqlalchemy.orm import Session
from . import models, schemas
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

#Function to retrieve the results of each round
#Return all of the user's scores for 1 round
#1 round is a display sequence id. Round 1 = display sequence id 1

def get_all_scores_by_round(db: Session, display_sequence_id: int):
    scores = db.query(models.Score)\
               .filter(models.Score.display_sequence_id == display_sequence_id)\
               .all()

    return scores

#Function to retrieve total score of all rounds for each user
def calculate_total_scores(db: Session, display_sequence_id: int):
    total_scores = []
    
    # Get all distinct user_ids for the given display_sequence_id
    user_ids = db.query(models.Score.user_id)\
                 .filter(models.Score.display_sequence_id == display_sequence_id)\
                 .distinct()\
                 .all()
    
    for row in user_ids:
        user_id = row.user_id  # Extract the user_id from the Row object

        # Get the user's name
        user = db.query(models.User)\
                 .filter(models.User.id == user_id)\
                 .first()
        
        # Get the total scores for the user
        scores = db.query(models.Score)\
                   .filter(models.Score.user_id == user_id)\
                   .all()
        
        # Calculate the total incorrect_guesses and correct_guesses
        total_incorrect_guesses = sum(score.incorrect_guesses for score in scores)
        total_correct_guesses = sum(score.correct_guesses for score in scores)
        
        # Append the user's information and total scores to the list
        total_scores.append({
            'user_id': user_id,
            'player_name': user.player_name,
            'total_incorrect_guesses': total_incorrect_guesses,
            'total_correct_guesses': total_correct_guesses
        })
    
    return total_scores

