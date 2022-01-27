from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class Command(BaseModel):
    action: str
    context: str


class GameState(BaseModel):
    x_coordinate: int
    y_coordinate: int
    health_points: int
    scene: str
    created: datetime


class Game(BaseModel):
    id: int
    game_states: List[GameState] = []
