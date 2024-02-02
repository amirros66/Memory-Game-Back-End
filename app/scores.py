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

#Function to retrieve total score of all rounds for each user of a given game
def calculate_total_scores(db: Session, game_id: int):
    #get all users in the game
    users = db.query(models.User)\
              .filter(models.User.game_id == game_id)\
              .all()
    #get all scores for all display sequences in the game
    scores = db.query(models.Score)\
               .filter(models.Score.display_sequence_id.in_(
                   db.query(models.DisplaySequence.id)\
                   .filter(models.DisplaySequence.game_id == game_id)
               ))\
               .all()
    #create a dictionary to store the scores
    user_scores = {}
    #initialize the dictionary with 0s
    for user in users:
        user_scores[user.id] = {"correct_guesses": 0, "incorrect_guesses": 0}
    #update the dictionary with the scores
    for score in scores:
        user_scores[score.user_id]["correct_guesses"] += score.correct_guesses
        user_scores[score.user_id]["incorrect_guesses"] += score.incorrect_guesses
    #return the scores
    return [schemas.TotalScore(user_id=user.id, player_name=user.player_name, total_correct_guesses=user_scores[user.id]["correct_guesses"], total_incorrect_guesses=user_scores[user.id]["incorrect_guesses"]) for user in users]

