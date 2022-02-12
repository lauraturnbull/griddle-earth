import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types

from .helpers import get_component, move_item_to_inventory


def try_capture_item(weight):
    return random.randrange(100) < weight


def handle_command(
    session: Session, game: types.Game, command: types.Command
) -> None:  # todo - add return type

    """
    input looks like:
    set trap in <component> with <inventory item>
    """
    if game.location is None:
        raise HTTPException(
            status_code=422,
            detail=("No location - game not started"),
        )
    component_delimiter = "from"
    item_delimiter = "with"
    try:
        component_start_index = command.context.index(component_delimiter)
        item_start_index = command.context.index(item_delimiter)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=(
                "You must provide the location and bait item when setting a"
                " trap: `set trap in [location] with [item]`"
            ),
        )

    component_name = " ".join(
        command.context[component_start_index + 1 : item_start_index]
    )
    bait_name = " ".join(command.context[item_start_index + 1 :])

    component = get_component(
        components=game.location.components, component_name=component_name
    )

    hunted_items = next(
        (
            i
            for i in component.items
            if i.item.collection_method is types.ItemCollectionMethod.hunt
        ),
        None,
    )
    if hunted_items is None:
        raise HTTPException(
            status_code=422,
            detail=f"Nothing available to hunt in {component_name}",
        )

    # always delete bait from inventory - todo raise on no bait
    bait_items = next(
        (i for i in game.inventory.items if i.item.name == bait_name), None
    )
    if bait_items is None:
        raise HTTPException(
            status_code=422,
            detail=(f"No {bait_name} found in inventory"),
        )
    bait_items.quantity -= 1
    persister.update_game(session, game.id, game)

    item_captured = try_capture_item(50 + hunted_items.item.health_points / 10)

    if item_captured:
        move_item_to_inventory(
            session,
            game=game,
            item_name=hunted_items.item.name,
            component_name=component_name,
        )

    # return failed trap type
    return None
