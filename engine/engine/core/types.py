from datetime import datetime
from enum import Enum
from typing import List, Optional

from aenum import MultiValueEnum
from pydantic import BaseModel

# enums


class Action(MultiValueEnum):
    take = "take", "grab", "t"
    look = "look", "l"
    move = "move", "go", "m"
    start = "start"
    set_trap = "set trap"
    cook = "cook", "c"
    eat = "eat", "e"

    @classmethod
    def values(cls):
        return [function.value for function in list(cls)]


class Ordinal(MultiValueEnum):
    north = "north", "n"
    east = "east", "e"
    south = "south", "s"
    west = "west", "w"


class ItemType(str, Enum):
    fruit = "fruit"
    vegetable = "vegetable"
    protein = "protein"
    grain = "grain"
    herb = "herb"
    meal = "meal"


class ItemCollectionMethod(str, Enum):
    hunt = "hunt"
    forage = "forage"
    cook = "cook"


class Region(str, Enum):
    wetlands = "wetlands"
    mountains = "mountains"
    forest = "forest"
    desert = "desert"
    home_plains = "Home Plains"


# input types


class Command(BaseModel):
    action: Action
    context: List[str]


# "core" types - returned from db


class Item(BaseModel):
    id: int
    name: str
    item_type: ItemType
    health_points: int
    collection_method: ItemCollectionMethod


class Items(BaseModel):
    id: int
    item: Item
    quantity: int


class Coordinates(BaseModel):
    x_coordinate: int
    y_coordinate: int


class Component(BaseModel):
    """A small part of a location that can be interacted with"""

    id: int
    name: str  # animal tracks
    description: str  # frequently used, perfect for setting traps
    items: List[Items] = []


class Location(BaseModel):
    id: int
    coordinates: Coordinates
    name: str
    description: str
    region: Region
    components: List[Component] = []


class Inventory(BaseModel):
    id: int
    items: List[Items] = []


class Game(BaseModel):
    id: int
    location: Optional[Location] = None
    health_points: int
    created: datetime
    inventory: Inventory


class Map(BaseModel):
    id: int
    locations: List[Location] = []


class AdventureLog(BaseModel):
    """Raw locations/items discovered - for db"""

    id: int
    discovered_locations: List[Location] = []
    discoverable_locations: List[Location]
    discovered_items: List[Item] = []
    discoverable_items: List[Item]
    # inventory ?
    # discovered_meals ?


# "new" types, without an id. For typing before adding to db.


class NewItem(BaseModel):
    name: str
    item_type: ItemType
    health_points: int
    collection_method: ItemCollectionMethod


class NewItems(BaseModel):
    item: NewItem
    quantity: int


class NewComponent(BaseModel):
    """A small part of a location that can be interacted with"""

    name: str  # animal tracks
    description: str  # frequently used, perfect for setting traps
    items: List[NewItems] = []


class NewLocation(BaseModel):
    coordinates: Coordinates
    name: str
    description: str
    region: Region
    components: List[NewComponent] = []


class NewMap(BaseModel):
    locations: List[NewLocation] = []


class NewAdventureLog(BaseModel):
    """Raw locations/items discovered - for db"""

    discovered_locations: List[NewLocation] = []
    discoverable_locations: List[NewLocation]
    discovered_items: List[NewItem] = []
    discoverable_items: List[NewItem]


class NewInventory(BaseModel):
    items: List[NewItems] = []


class NewGame(BaseModel):
    health_points: int
    created: datetime
    inventory: NewInventory


# command return types


class DiscoveredLocationsByRegion(BaseModel):
    region: Region
    discovered: int = 0
    discoverable: int


class DiscoveredItemsByType(BaseModel):
    item_type: ItemType
    discovered: int = 0
    discoverable: int


class AdventureLogOut(BaseModel):
    """Formatted locations and items discovered"""

    locations_discovered: List[DiscoveredLocationsByRegion]
    items_discovered: List[DiscoveredItemsByType]


class LocationOut(BaseModel):
    name: str
    description: str
    region: Region


class ItemsOut(BaseModel):
    quantity: int
    name: str
    health_points: int


class MoveResponse(BaseModel):
    health_points: int
    location: LocationOut


class EatResponse(BaseModel):
    health_points: int
    consumed_item: ItemsOut


class LookAroundResponse(BaseModel):
    names: List[str]


class LookAtResponse(BaseModel):
    description: str
    visible_items: List[ItemsOut]


# purely internal


class Recipe(BaseModel):
    name: str
    description: str
    required_items: List[NewItem] = []
    required_types: List[ItemType] = []
    boost: int


class RecipeBook(BaseModel):
    recipes: List[Recipe] = []
