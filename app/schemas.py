from typing import Union
from pydantic import BaseModel

class UserBase(BaseModel):
    player_name: str 
    # game_id: int
    
class UserCreate(UserBase):
    pass