from datetime import datetime
from typing import List, Optional

from engine.core import types

frozen_now = datetime(2022, 2, 2)


def make_inventory(items: List[types.Items] = []) -> types.Inventory:
    return types.Inventory(items=items)


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


def make_coordinates(
    x_coordinate: int = 0, y_coordinate: int = 0
) -> types.Coordinates:
    return types.Coordinates(
        x_coordinate=x_coordinate, y_coordinate=y_coordinate
    )


def make_item(
    name: str = "apple",
    item_type: types.ItemType = types.ItemType.fruit,
    health_points: int = 50,
    collection_method: types.ItemCollectionMethod = types.ItemCollectionMethod.forage,
) -> types.Item:
    return types.Item(
        name=name,
        item_type=item_type,
        health_points=health_points,
        collection_method=collection_method,
    )


def make_items(
    quantity: int = 1,
    item: Optional[types.Item] = None,
) -> types.Items:
    if not item:
        item = make_item()
    return types.Items(item=item, quantity=quantity)


def make_component(
    name: str = "trees",
    description: str = "some trees full of apples",
    items: List[types.Items] = [],
) -> types.Component:
    if not items:
        items = [make_items()]
    return types.Component(
        name=name,
        description=description,
        items=items,
    )


def make_location(
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
        coordinates=coordinates,
        name=name,
        description=description,
        region=region,
        components=components,
    )


def make_map(locations: List[types.Location] = []) -> types.Map:
    if not locations:
        locations = [make_location()]

    return types.Map(locations=locations)


def make_adventure_log(
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
        discoverable_locations=discoverable_locations,
        discovered_locations=discovered_locations,
        discoverable_items=discoverable_items,
        discovered_items=discovered_items,
    )
