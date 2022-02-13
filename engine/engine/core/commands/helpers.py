from typing import List, Optional, Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types


def get_noun_variants(noun: str) -> List[str]:
    return [noun, noun + "s", noun[:-1]]


def get_component(
    components: List[types.Component], component_name: str
) -> types.Component:
    component_name_variants = get_noun_variants(component_name)

    component = next(
        (c for c in components if c.name.lower() in component_name_variants),
        None,
    )

    if component is None:
        raise HTTPException(
            status_code=422, detail=f"Cannot find location {component_name}"
        )

    return component


def get_items(items_list: List[types.Items], item_name: str) -> types.Items:
    items_name_variants = get_noun_variants(item_name)

    items = next(
        (i for i in items_list if i.item.name.lower() in items_name_variants),
        None,
    )

    if items is None:
        raise HTTPException(
            status_code=422, detail=f"Cannot find any {item_name} to take"
        )
    return items


def move_item_to_inventory(
    session: Session,
    game: types.Game,
    component_name: str,
    item_name: str,
    take_all: bool = False,
) -> types.ItemsOut:

    if game.location is None:
        raise HTTPException(
            status_code=422,
            detail=("No location - game not started"),
        )
    map_location = persister.get_map_location_by_coordinates(
        session=session, game_id=game.id, coordinates=game.location.coordinates
    )
    if map_location is None:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Could not find location at "
                f"x={game.location.coordinates.x_coordinate}, "
                f"y={game.location.coordinates.y_coordinate}"
            ),
        )

    map_component = get_component(
        components=map_location.components, component_name=component_name
    )
    map_items = get_items(items_list=map_component.items, item_name=item_name)

    inventory_items: Optional[Union[types.Items, types.NewItems]]
    inventory_items = next(
        (
            i
            for i in game.inventory.items
            if i.item.name == map_items.item.name
        ),
        None,
    )

    if inventory_items is None:
        inventory_items = types.NewItems(
            quantity=0, item=types.NewItem(**map_items.item.dict())
        )
        # shouts when adding for the first time
        game.inventory.items.append(inventory_items)  # type: ignore

    if take_all:
        inventory_items.quantity += map_items.quantity
        map_items.quantity = 0
    else:
        inventory_items.quantity += 1
        map_items.quantity -= 1

    if map_items.quantity == 0:
        map_component.items.remove(map_items)

    game.location = map_location

    persister.update_map_location(
        session, game_id=game.id, new_location_state=map_location
    )
    persister.update_game(session, game_id=game.id, new_game_state=game)

    persister.update_adventure_log_discovered_items(
        session, game_id=game.id, item=inventory_items.item
    )
    return types.ItemsOut(
        quantity=inventory_items.quantity,
        name=inventory_items.item.name,
        health_points=inventory_items.item.health_points,
    )
