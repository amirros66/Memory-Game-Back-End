from typing import Union
from pydantic import BaseModel

class UserBase(BaseModel):
    player_name: str 
    # game_id: int
    
class UserCreate(UserBase):
    pass


class DisplaySequenceBase(BaseModel):
    id: int
    value: str

class InputSequenceBase(BaseModel):
    value: str

class InputSequence(BaseModel):
    id: int
    value: str
class InputSequenceCreate(InputSequenceBase):
    pass


class GameBase(BaseModel):
    id: int


class Game(BaseModel):
    id: int
    active: bool

class NewGame(BaseModel):
    game_id: int
    user_id: int
    player_name: str
    sequences: list[DisplaySequenceBase]