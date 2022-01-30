from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from enum import Enum


class Command(BaseModel):
    action: str
    context: str


class ItemType(str, Enum):
    fruit = "fruit"
    vegetable = "vegetable"
    meat = "meat"
    fish = "fish"
    grain = "grain"
    herb = "herb"


class Item(BaseModel):
    name: str
    item_type: ItemType
    health_points: int


class Items(BaseModel):
    item: Item
    quantity: int


class Region(str, Enum):
    wetlands = "wetlands",
    mountains = "mountains",
    forest = "forest",
    desert = "desert",
    home_plains = "Home Plains"


class Location(BaseModel):
    x_coordinate: int
    y_coordinate: int
    name: str
    description: str
    region: Region
    items: List[Items] = []


class GameState(BaseModel):
    location: Optional[Location] = None
    health_points: int
    created: datetime


class Game(BaseModel):
    id: int
    game_states: List[GameState] = []


class Map(BaseModel):
    locations: List[Location] = []
