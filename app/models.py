from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from adjspecies3 import random_adjspecies


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    player_name = Column(String, unique=True, default=random_adjspecies)
    
    game_id = Column(Integer, ForeignKey("games.id"))
    
    game = relationship("Game", back_populates="user")
    input_sequence = relationship("InputSequence", back_populates="user")
    score = relationship("Score", back_populates="user")
    
class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="game")
    
class DisplaySequence(Base):
    __tablename__ = "display_sequences"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    value= Column(String)
    
    input_sequence = relationship("InputSequence", back_populates="display_sequence")
    score = relationship("Score", back_populates="display_sequence")
    
class InputSequence(Base):
    __tablename__ = "input_sequences"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    value = Column(String)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    display_sequence_id = Column(Integer, ForeignKey("display_sequences.id"))   
    
    user = relationship("User", back_populates="input_sequence")
    display_sequence = relationship("DisplaySequence", back_populates="input_sequence")
    score = relationship("Score", back_populates="input_sequence")

#For overall scores at Game over
class Score (Base):
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    correct_guesses = Column(Integer)
    incorrect_guesses = Column(Integer)

    #Foreign Keys
    #user:
    user_id = Column(Integer, ForeignKey("users.id"))
    #round:
    display_sequence_id = Column(Integer, ForeignKey("display_sequences.id"))  
    #Do we need this? 
    input_sequence_id = Column(Integer, ForeignKey("input_sequences.id"))


    #Relationships
    user = relationship("User", back_populates="score")
    display_sequence = relationship("DisplaySequence", back_populates="score")
    input_sequence = relationship("InputSequence", back_populates="score")

