from pydantic import BaseModel
from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import adjspecies 

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    player_name = Column(String, unique=True)
    correct_guesses = Column(Integer)
    incorrect_guesses = Column(Integer)
    
    game_id = Column(Integer, ForeignKey("games.id"))
    
class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    active = Column(Boolean)
    
    
class DisplaySequence(Base):
    __tablename__ = "display_sequences"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    value= Column(String)
    
class InputSequence(Base):
    __tablename__ = "input_sequences"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    value = Column(String)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    display_sequence_id = Column(Integer, ForeignKey("display_sequences.id"))   
    
