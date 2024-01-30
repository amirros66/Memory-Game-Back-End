from sqlalchemy.orm import Session
from . import models, schemas
import random
possible_inputs = ["up", "down", "left", "right"]

def generate_sequence(length: int):
    sequence = []
    for i in range(length):
        sequence.append(random.choice(possible_inputs))
    return ','.join(sequence)

def add_sequence(db: Session):
    db_sequence = models.Sequence()
    db.add(db_sequence)
    db.commit()
    db.refresh(db_sequence)
    return db_sequence

sequence = generate_sequence(4)
print(sequence)