from sqlalchemy.orm import Session
from . import models, schemas
import random
possible_inputs = ["up", "down", "left", "right"]

def generate_sequence(length: int):
    sequence = []
    for i in range(length):
        sequence.append(random.choice(possible_inputs))
    return ','.join(sequence)

def add_sequences(db: Session):
    db_sequence1 = models.Sequence(sequence = generate_sequence(4))
    db_sequence2 = models.Sequence(sequence = generate_sequence(6))
    db_sequence3 = models.Sequence(sequence = generate_sequence(8))
    db.add(db_sequence1)
    db.add(db_sequence2)
    db.add(db_sequence3)
    db.commit()

sequence = generate_sequence(4)
print(sequence)