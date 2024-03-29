from sqlalchemy.orm import Session
from . import models, schemas
import random
possible_inputs = ["up", "down", "left", "right"]

def generate_sequence(length: int):
    sequence = []
    for i in range(length):
        sequence.append(random.choice(possible_inputs))
    return ','.join(sequence)

def add_sequences(db: Session, game_id: int):
    for x in range(4,10,2):
        db_sequence = models.DisplaySequence(value = generate_sequence(x), game_id = game_id)
        db.add(db_sequence)
        db.commit()
    return db.query(models.DisplaySequence).all()
