from typing import Union
from pydantic import BaseModel

class UserBase(BaseModel):
    player_name: str 
    # game_id: int
    
class UserCreate(UserBase):
    pass




class InputSequenceBase(BaseModel):
    value: str
    
class InputSequenceCreate(InputSequenceBase):
    pass


class Game(BaseModel):
    id: int
    active: bool


class GameCreate(BaseModel):
    active: bool
