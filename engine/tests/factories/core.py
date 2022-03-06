from datetime import datetime
from typing import List, Optional

from engine.core import types

frozen_now = datetime(2022, 2, 2)


def make_new_inventory(items: List[types.NewItems] = []) -> types.NewInventory:
    return types.NewInventory(items=items)


def make_coordinates(
    x_coordinate: int = 0, y_coordinate: int = 0
) -> types.Coordinates:
    return types.Coordinates(
        x_coordinate=x_coordinate, y_coordinate=y_coordinate
    )


def make_new_item(
    name: str = "apple",
    item_type: types.ItemType = types.ItemType.fruit,
    health_points: int = 50,
    collection_method: types.ItemCollectionMethod = types.ItemCollectionMethod.forage,  # noqa E501
) -> types.NewItem:
    return types.NewItem(
        name=name,
        item_type=item_type,
        health_points=health_points,
        collection_method=collection_method,
    )


def make_new_items(
    quantity: int = 1,
    item: Optional[types.NewItem] = None,
) -> types.NewItems:
    if not item:
        item = make_new_item()
    return types.NewItems(item=item, quantity=quantity)


def make_new_component(
    name: str = "trees",
    description: str = "some trees full of apples",
    items: List[types.NewItems] = [],
) -> types.NewComponent:
    if not items:
        items = [make_new_items()]
    return types.NewComponent(
        name=name,
        description=description,
        items=items,
    )


def make_new_location(
    coordinates: Optional[types.Coordinates] = None,
    name: str = "A sample location",
    description: str = "A descriptive description",
    region: types.Region = types.Region.forest,
    components: List[types.NewComponent] = [],
) -> types.NewLocation:
    if not coordinates:
        coordinates = make_coordinates()
    if not components:
        components = [make_new_component()]

    return types.NewLocation(
        coordinates=coordinates,
        name=name,
        description=description,
        region=region,
        components=components,
    )


def make_new_map(locations: List[types.NewLocation] = []) -> types.NewMap:
    if not locations:
        locations = [make_new_location()]

    return types.NewMap(locations=locations)


def make_new_adventure_log(
    discoverable_locations: List[types.NewLocation] = [],
    discovered_locations: List[types.NewLocation] = [],
    discoverable_items: List[types.NewItem] = [],
    discovered_items: List[types.NewItem] = [],
) -> types.NewAdventureLog:
    if not discoverable_locations:
        discoverable_locations = [make_new_location()]
    if not discoverable_items:
        discoverable_items = [make_new_item()]

    return types.NewAdventureLog(
        discoverable_locations=discoverable_locations,
        discovered_locations=discovered_locations,
        discoverable_items=discoverable_items,
        discovered_items=discovered_items,
    )


def make_new_game(
    health_points: int = 1000,
    inventory: Optional[types.NewInventory] = None,
    created: datetime = frozen_now,
) -> types.NewGame:
    if inventory is None:
        inventory = make_new_inventory()

    return types.NewGame(
        health_points=health_points,
        inventory=inventory,
        created=created,
    )


def make_inventory(
    id: int = 1, items: List[types.Items] = []
) -> types.Inventory:
    return types.Inventory(id=id, items=items)


def make_game(
    id: int = 1,
    created: datetime = frozen_now,
    health_points: int = 1000,
    inventory: Optional[types.Inventory] = None,
    location: Optional[types.Location] = None,
) -> types.Game:
    if inventory is None:
        inventory = make_inventory()
    return types.Game(
        id=id,
        created=created,
        health_points=health_points,
        inventory=inventory,
        location=location,
    )


def make_item(
    id: int = 1,
    name: str = "apple",
    item_type: types.ItemType = types.ItemType.fruit,
    health_points: int = 50,
    collection_method: types.ItemCollectionMethod = types.ItemCollectionMethod.forage,  # noqa E501
) -> types.Item:
    return types.Item(
        id=id,
        name=name,
        item_type=item_type,
        health_points=health_points,
        collection_method=collection_method,
    )


def make_items(
    id: int = 1,
    quantity: int = 1,
    item: Optional[types.Item] = None,
) -> types.Items:
    if not item:
        item = make_item()
    return types.Items(id=id, item=item, quantity=quantity)


def make_component(
    id: int = 1,
    name: str = "trees",
    description: str = "some trees full of apples",
    items: List[types.Items] = [],
) -> types.Component:
    if not items:
        items = [make_items()]
    return types.Component(
        id=id,
        name=name,
        description=description,
        items=items,
    )


def make_location(
    id: int = 1,
    coordinates: Optional[types.Coordinates] = None,
    name: str = "A sample location",
    description: str = "A descriptive description",
    region: types.Region = types.Region.forest,
    components: List[types.Component] = [],
) -> types.Location:
    if not coordinates:
        coordinates = make_coordinates()
    if not components:
        components = [make_component()]

    return types.Location(
        id=id,
        coordinates=coordinates,
        name=name,
        description=description,
        region=region,
        components=components,
    )


def make_map(id: int = 1, locations: List[types.Location] = []) -> types.Map:
    if not locations:
        locations = [make_location()]

    return types.Map(id=id, locations=locations)


def make_adventure_log(
    id: int = 1,
    discoverable_locations: List[types.Location] = [],
    discovered_locations: List[types.Location] = [],
    discoverable_items: List[types.Item] = [],
    discovered_items: List[types.Item] = [],
) -> types.AdventureLog:
    if not discoverable_locations:
        discoverable_locations = [make_location()]
    if not discoverable_items:
        discoverable_items = [make_item()]

    return types.AdventureLog(
        id=id,
        discoverable_locations=discoverable_locations,
        discovered_locations=discovered_locations,
        discoverable_items=discoverable_items,
        discovered_items=discovered_items,
    )


def make_location_out(
    description: str = "A descriptive description",
    name: str = "A sample location",
    region: types.Region = types.Region.forest,
) -> types.LocationOut:
    return types.LocationOut(
        description=description,
        name=name,
        region=region,
    )


def make_response(
    message: str,
    health_points: Optional[int] = None,
    location: Optional[types.LocationOut] = None,
) -> types.Response:
    return types.Response(
        health_points=health_points, location=location, message=message
    )
