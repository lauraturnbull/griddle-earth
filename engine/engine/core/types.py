from datetime import datetime
from enum import Enum
from typing import Callable, List, Optional, Union

from aenum import MultiValueEnum
from humps import camelize
from pydantic import BaseModel

# enums


class Ordinal(MultiValueEnum):
    north = "north", "n"
    east = "east", "e"
    south = "south", "s"
    west = "west", "w"


class ItemType(str, Enum):
    fruit = "fruits"
    vegetable = "vegetables"
    protein = "proteins"
    grain = "grains"
    herb = "herbs"
    meal = "meals"


class ItemCollectionMethod(str, Enum):
    hunt = "hunt"
    forage = "forage"
    cook = "cook"


class Region(str, Enum):
    wetlands = "wetlands"
    mountains = "mountains"
    forest = "forest"
    desert = "desert"
    grasslands = "grasslands"


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
    z_coordinate: int


class Component(BaseModel):
    """A small part of a location that can be interacted with"""

    id: int
    name: str  # animal tracks
    description: str  # frequently used, perfect for setting traps
    items: List[Items] = []
    transports_to: Optional[Coordinates] = None


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
    transports_to: Optional[Coordinates] = None


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
def to_camel(string):
    return camelize(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class DiscoveredLocationsByRegion(CamelModel):
    region: Region
    discovered: int = 0
    discoverable: int


class DiscoveredItemsByType(CamelModel):
    item_type: ItemType
    discovered: int = 0
    discoverable: int


class AdventureLogResponse(CamelModel):
    """Formatted locations and items discovered"""

    locations_discovered: List[DiscoveredLocationsByRegion]
    items_discovered: List[DiscoveredItemsByType]


class LocationOut(CamelModel):
    name: str
    description: str
    region: Region


class NewGameResponse(CamelModel):
    id: int
    message: str


class Response(CamelModel):
    health_points: Optional[int]
    location: Optional[LocationOut]
    message: str


class ActionOut(CamelModel):
    name: str
    aliases: List[str]
    description: str
    examples: List[str] = []


class HelpResponse(CamelModel):
    actions: List[ActionOut]


class ItemsOut(CamelModel):
    name: str
    health_points: int
    quantity: int


class GroupedInventory(CamelModel):
    item_type: ItemType
    items: List[ItemsOut]


class InventoryResponse(CamelModel):
    inventory: List[GroupedInventory]


class RecipeOut(CamelModel):
    name: str
    description: str
    boost: int


class RecipeBookResponse(CamelModel):
    recipes: List[RecipeOut]


# purely internal


class Recipe(BaseModel):
    name: str
    description: str
    required_types: List[ItemType] = []
    boost: int


class RecipeBook(BaseModel):
    recipes: List[Recipe] = []


class Action(BaseModel):
    name: str
    aliases: List[str]
    handler: Callable[
        ...,
        Union[
            Response,
            HelpResponse,
            InventoryResponse,
            AdventureLogResponse,
            RecipeBookResponse,
        ],
    ]
    description: str
    examples: Optional[List[str]] = []


class Actions(BaseModel):
    actions: List[Action]


class CommandResponse(BaseModel):
    __root__: Union[
        Response,
        HelpResponse,
        InventoryResponse,
        AdventureLogResponse,
        RecipeBookResponse,
    ]
