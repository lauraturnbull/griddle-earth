from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from enum import Enum


class Command(BaseModel):
    action: str
    context: List[str]


class ItemType(str, Enum):
    fruit = "fruit"
    vegetable = "vegetable"
    protein = "protein"
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


class Coordinates(BaseModel):
    x_coordinate: int
    y_coordinate: int


class Component(BaseModel):
    """A small part of a location that can be interacted with"""
    name: str  # animal tracks
    description: str  # frequently used, perfect for setting traps
    items: List[Items] = []


class Location(BaseModel):
    coordinates: Coordinates
    name: str
    description: str
    region: Region
    components: List[Component] = []


class Inventory(BaseModel):
    items: List[Items] = []


class NewGame(BaseModel):
    location: Optional[Location] = None
    health_points: int
    created: datetime
    inventory: Inventory


class Game(BaseModel):
    id: int
    location: Optional[Location] = None
    health_points: int
    created: datetime
    inventory: Inventory


class Map(BaseModel):
    locations: List[Location] = []


# command return types

class ComponentNameList(BaseModel):
    names: List[str]


class ComponentDescription(BaseModel):
    description: str
