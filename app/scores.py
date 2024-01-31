from sqlalchemy.orm import Session
from . import models, schemas


#Function to retrieve the results of each round
#Return all of the user's scores for 1 round
#1 round is a display sequence id. Round 1 = display sequence id 1

def get_all_scores_by_round(db: Session, display_sequence_id: int):
    scores = db.query(models.Score)\
               .filter(models.Score.display_sequence_id == display_sequence_id)\
               .all()

    return scores