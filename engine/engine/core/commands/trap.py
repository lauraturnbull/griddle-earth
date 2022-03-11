import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import constants, types

from .helpers import get_component, move_item_to_inventory


def try_capture_item(weight):
    return random.randrange(100) < weight


def handle_command(
    session: Session, game: types.Game, input: str
) -> types.Response:
    """
    input looks like:
    set trap in <component> with <inventory item>
    """
    context = input.split(" ")
    if game.location is None:
        raise HTTPException(
            status_code=422,
            detail=("No location - game not started"),
        )
    component_delimiter = "in"
    item_delimiter = "with"  # todo - or "using"
    try:
        component_start_index = context.index(component_delimiter)
    except ValueError:
        return types.Response(message="Where do you want to set the trap?")
    try:
        item_start_index = context.index(item_delimiter)
    except ValueError:
        return types.Response(
            message="You must provide bait from your inventory to set a trap."
        )

    if (
        sum(i.quantity for i in game.inventory.items)
        == constants.MAX_INVENTORY_SIZE  # noqa W503
    ):
        return types.Response(message=constants.EXCEEDED_MAX_INVENTORY)

    component_name = " ".join(
        context[component_start_index + 1 : item_start_index]
    )
    bait_name = " ".join(context[item_start_index + 1 :])

    component = get_component(
        components=game.location.components, component_name=component_name
    )
    if component is None:
        return types.Response(
            message=constants.MISSING_COMPONENT.format(
                component=component_name
            )
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
        return types.Response(
            message=constants.NOTHING_TO_HUNT.format(component=component_name),
        )

    # always delete bait from inventory
    bait_items = next(
        (i for i in game.inventory.items if i.item.name == bait_name), None
    )
    if bait_items is None:
        return types.Response(
            message=constants.MISSING_INVENTORY_ITEM.format(item=bait_name),
        )
    bait_items.quantity -= 1
    persister.update_game(session, game.id, game)

    item_captured = try_capture_item(40 + bait_items.item.health_points / 10)

    if item_captured:
        move_item_to_inventory(
            session,
            game=game,
            item_name=hunted_items.item.name,
            component_name=component_name,
            collection_method=[types.ItemCollectionMethod.hunt],
        )
        return types.Response(
            message=constants.SUCCESSFUL_TRAP.format(
                component=component_name,
                bait=bait_items.item.name,
                prey=hunted_items.item.name,
            )
        )

    return types.Response(
        message=constants.FAILED_TRAP.format(
            component=component_name, bait=bait_items.item.name
        )
    )
