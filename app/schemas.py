from pydantic import BaseModel


class UserBase(BaseModel):
    player_name: str
    id: int


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


# Scores schemas
class UserScore(BaseModel):
    user_id: int
    correct_guesses: int
    incorrect_guesses: int


class RoundScores(BaseModel):
    round_id: int
    scores: list[UserScore]


class ScoreBase(BaseModel):
    correct_guesses: int
    incorrect_guesses: int


class Score(ScoreBase):
    id: int
    user_id: int
    display_sequence_id: int
    input_sequence_id: int


# Lobby user schemas
class LobbyUser(BaseModel):
    user_id: int
    player_name: str


class TotalScore(BaseModel):
    user_id: int
    player_name: str
    total_correct_guesses: int
    total_incorrect_guesses: int


# Display sequence schemas
class DisplaySequence(BaseModel):
    id: int
    value: str


class Healthz(BaseModel):
    status: str
