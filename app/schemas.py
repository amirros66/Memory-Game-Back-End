from typing import Union
from pydantic import BaseModel

class UserBase(BaseModel):
    player_name: str 
    
class UserCreate(UserBase):
    pass